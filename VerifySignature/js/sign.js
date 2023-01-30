var dotenv = require('dotenv').config()
const Web3 = require('web3')
var web3
switch(process.env.CurrentChain)
{
        case "Goerli":
                web3 = new Web3(Web3.givenProvider || process.env.Goerli)
                break
        case "Ganache":
                web3 = new Web3(Web3.givenProvider || process.env.LocalGanache)
                break
        default:
                throw'Please specify the current chainrpc to get encoding from!\n Use .env variable CurrentChain !'
}
console.log(web3.eth.accounts.sign("0xfc7c3df6e3ef43476efab4e51a0ed700b6041e3178be3190830233b3a5d335b0", process.env.GoerliPrivKey));
