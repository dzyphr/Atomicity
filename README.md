**In Development**
# Atomicity WIP Stage: Alpha
###### Small, Abstract, Modular, and Modifiable EVM-Solidity scripting framework. 
###### Aiming to support cross chain consensus code through building external compatible frameworks.
**Current Project Status**:
  * Testnet contracts on Goerli
  * Modular via .env files
  * Using node w3js w3py and a little bit of cpp for basic framework generation commands.
[![Atomicity Picture](https://www.thoughtco.com/thmb/D_uEiv8l3SYKvWtKkAkN_O5zB7U=/3825x2574/filters:fill(auto,1)/GettyImages-141483984-56a133b65f9b58b7d0bcfdb1.jpg)](https://github.com/dzyphr/Atomicity)

# Currently using linux filesystem calls by default

## Set up your .env Variables (go to `basic_framework` and make a .env file)

###### Note: If you encounter a bug while using python-dotenv you can upgrade to the latest python currently 3.11

###### If you get another bug related web3 package https://github.com/ethereum/web3.py/issues/2704 you can follow these steps: `vim ~/.local/lib/python3.11/site-packages/parsimonious/expressions.py` and change getargspec import line to say: `from inspect import getfullargspec` These two bugs are like a sandwich between python versions placing our framework in the middle of it, so far so good though.

#### **GoerliSenderAddr="YourPublicAddress"**
#### **GoerliPrivKey="YourPrivateKey"** 
#### **Goerli="YourRPCEndpoint"** 
###### _alchemy, infura, quicknode, etc..._
#### **GoerliID=5** 
###### _chainID_
#### **GoerliScan="https://api-goerli.etherscan.io/api"** 
###### _block explorer api link for goerli_
#### **EtherscanAPIKey="YourAPIKey"** 
###### _generic API key for any etherscan based block explorer_
#### **CurrentChain="Goerli"**
#### **VerifyBlockExplorer="True"** 
###### _set whether or not to verify the contract_
#### **SolidityCompilerVersion="0.8.0"** 

###### Verifying contracts only works on Goerli atm due to logic that selects the chain, will extend to all available chains

## Basic Usage:

### After .env variables are set up, run `new_frame ContractName` and replace `ContractName` with the name of your contract.

#### NOTE: If you have constructor parameters use the flag `-CA` followed by the number of parameters, and then one argument for each parameter.

#### NOTE: If you have multiple contract files that you need to compile all together, use the `-M` flag. You can use `-M` or `-CA` iterchangably provided you give all the correct follow-up parameters if using `-CA` this format should follow for future arguments. #WARN this is an unstable update, we are about to implement the flattening involved in verifying these contracts programatically, to verify from unstable you need to manually flatten

#### `cd` to the newly created folder named after the `ContractName` argument you just chose.

#### Write your contract in the `/contracts` folder. Note that we have not tested contracts using libraries yet only single page.

#### Finally run `deploy.sh` (`python3 py/deploy.py`) 

#### If your rpc gives gas estimation issues it's because were calling `rpc.eth.gas_price` and sometimes this can be innacurate enough to revert the transaction. Increase the `gasMod` variable on line 19 of deploy.py to multiply the gas price by the desired amount. Feel free to change the equation to raise gas for your own needs, and ONLY use any real-live-mainnet gas tokens AT YOUR OWN RISK! Testnet First!
