var dotenv = require('dotenv').config();

const Web3 = require('web3');
//const web3 = new Web3(Web3.givenProvider || "HTTP://127.0.0.1:7545") //local instance
const web3 = new Web3(Web3.givenProvider || process.env.Goerli) //rpc from env variable
console.log(web3)
