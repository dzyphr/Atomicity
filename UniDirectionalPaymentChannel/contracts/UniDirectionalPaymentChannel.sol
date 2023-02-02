// SPDX-License-Identifier: GPL-3.0-only
pragma solidity >=0.8.0 <0.9.0;

import "ECDSA.sol";
import "ReentrancyGuard.sol";

contract UniDirectionalPaymentChannel is ReentrancyGuard
{
	using ECDSA for bytes32;
	address payable public sender;
	address payable public reciever;
	uint private constant DURATION = 604800;
	uint public expireTime;

	constructor(address payable rec) payable
	{
		require(rec != address(0), "reciever is a null addr!");
		sender = payable(msg.sender);
		reciever = rec;
		expireTime = block.timestamp + DURATION;
	}

	function internalGetHash(uint amt) private view returns (bytes32)
	{
		return keccak256(abi.encodePacked(address(this), amt));
	}

	function externalGetHash(uint amt) external view returns (bytes32)
	{
		return internalGetHash(amt);
	}

	function internalGetSignedHash(uint amt) private view returns (bytes32)
	{
		return internalGetHash(amt).toEthSignedMessageHash();
	}

	function externalGetSignedHash(uint amt) external view returns (bytes32)
	{
		return internalGetSignedHash(amt);
	}

	function internalVerify(uint amt, bytes memory sig) private view returns (bool)
	{
		return internalGetSignedHash(amt).recover(sig) == sender;
	}

	function externalVerify(uint amt, bytes memory sig) external view returns (bool)
	{
		return internalVerify(amt, sig);
	}

	function close(uint amt, bytes memory sig) external nonReentrant
	{
		require(msg.sender == reciever, "addr other than reciever attempting to close!");
		require(internalVerify(amt, sig), "invalid signature!");
		(bool sent, ) = reciever.call{value: amt}("");
		require(sent, "Failed to send !");
		selfdestruct(sender);
	}

	function cancel() external
	{
		require(msg.sender == sender, "addr other than sender tried to cancel the contract!");
		require(block.timestamp >= expireTime, "timelock has not expired!");
		selfdestruct(sender);
	}

}
