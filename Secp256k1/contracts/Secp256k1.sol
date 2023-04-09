// SPDX-License-Identifier: GPL-3.0-only
pragma solidity >=0.8.0 <0.9.0;

import "EllipticCurve.sol";

contract Secp256k1
{
	uint256 public constant GX = 
	0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798;
	uint256 public constant GY = 
	0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8;
	uint256 public constant AA = 0;
	uint256 public constant BB = 7;
	uint256 public constant PP = 
	0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F;	
	constructor(uint256 _GX, uint256 _GY, uint256 _AA, uint256 _BB, uint256 _PP)
	{
		require(GX == _GX);
		require(GY == _GY);
		require(AA == _AA);
		require(BB == _BB);
		require(PP == _PP);
	}

	function ecMulSecp256k1( uint256 k) pure public returns (uint256, uint256)
	{
		return EllipticCurve.ecMul(k, GX, GY,AA,PP);
	}
	
	function onCurve(uint256 x, uint256 y) pure public returns (bool)
	{
	    return EllipticCurve.isOnCurve(x,y,AA,BB,PP);
	}
}
