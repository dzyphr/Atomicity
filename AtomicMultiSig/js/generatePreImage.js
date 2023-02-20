require('dotenv').config(); 
const Web3 = require('web3');
var web3 = new Web3(process.env.Goerli);
async function getHeight()
{
    await web3.eth.getBlockNumber().then(function(result)
    {
            res = result
    });
    return res;
}
async function main()
{
	const {
	  randomBytes,
	} = await import('node:crypto');
	
	randomBytes(32, (err, buf) => {
	  if (err) throw err;
		blindingFactor = buf.toString('hex')
	});
	height = await getHeight()
	preImageScript = height.toString() +  new Date().getTime().toString() + blindingFactor
	const { createHash } = require('crypto')
	console.log(createHash('sha256').update(preImageScript).digest('hex'))
}
main()
