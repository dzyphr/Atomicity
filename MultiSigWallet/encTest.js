const Web3 = require('web3')

const web3 = new Web3;
console.log(web3.eth.abi.encodeParameters(
  ['address[]', 'uint256'],
  [['0xFe4cc19ea6472582028641B2633d3adBB7685C69', '0x01225869F695b4b7F0af5d75381Fe340A4d27593'], 2]
))
