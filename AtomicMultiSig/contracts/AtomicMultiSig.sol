// SPDX-License-Identifier: GPL-3.0-only
pragma solidity >=0.8.0 <0.9.0;

import "ReentrancyGuard.sol";

contract AtomicMultiSig is ReentrancyGuard
{
	event Deposit(address indexed sender, uint amount, uint balance);
	address payable public sender;
	address payable public receiver;
	uint private constant DURATION = 100;
	uint public lockHeight;
	bytes32 public hashedPreImage;

	receive() external payable
	{
		emit Deposit(msg.sender, msg.value, address(this).balance);
	}

	constructor(address payable rec, bytes32 HPI) payable
	{
		require(rec != address(0), "reciever is a null addr!");
		sender = payable(msg.sender);
                receiver = rec;
		lockHeight = block.timestamp + DURATION;
		hashedPreImage = HPI;
	}

	function receiverWithdraw(bytes32 preImage) external nonReentrant
	{
		require(msg.sender == receiver);
		require(keccak256(abi.encode(preImage)) == hashedPreImage);
		(bool sent, ) = receiver.call{value: address(this).balance}("");
		require(sent, "Failed to send !");
	}

	function senderReclaim() external
	{
		require(msg.sender == sender);
		require(block.timestamp >= lockHeight, "timelock has not expired!");
		selfdestruct(sender); //this selfdestruct makes some sense but will replace if its bad practice
	}
}
