var dotenv = require('dotenv').config(); 
var contractAddr = ""
var lastindex = 0
process.argv.forEach(function (val, index) {
	if (index == 2 )
	{
		contractAddr = val
	}
	lastindex = index
})
if (lastindex < 2)
{
	throw 'please provide the contract address as a command line argument'
}

var Contract = require('web3-eth-contract')
const fs = require('fs');

var jsonABI = fs.readFileSync('SimpleStorage-abi.json', 'utf8')

console.log(jsonABI)
Contract.setProvider(process.env.Goerli)
var contract = new Contract(JSON.parse(jsonABI), contractAddr)
console.log(contract.methods)
//use the methods to grab the constructor arguments contract.method.constructor.encodeABI()


