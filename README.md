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

#### **GoerliSenderAddr="YourPublicAddress"**
#### **GoerliPrivKey="YourPrivateKey"** 
#### **Goerli="YourRPCEndpoint"** _alchemy, infura, quiknode, etc..._
#### **GoerliID=5** _chainID_
#### **GoerliScan="https://api-goerli.etherscan.io/api"** _block explorer api link for goerli_
#### **EtherscanAPIKey="YourAPIKey"** _generic API key for any etherscan based block explorer_
#### **CurrentChain="Goerli"**
#### **VerifyBlockExplorer="True"** _set whether or not to verify the contract_
#### **SolidityCompilerVersion="0.8.0"** 

###### Verifying contracts only works on Goerli atm due to logic that selects the chain, will extend to all available chains

## Basic Usage:

#### After .env variables are set up, run `new_frame ContractName` and replace `ContractName` with the name of your contract.

#### `cd` to the newly created folder named after the `ContractName` argument you just chose.

#### After this the only thing you should need to modify is the `constructorParamVals` around line ~102 of deploy.py, if you have parameters/arguments in your constructor. Set the values you would like to use in the constructor in this list if so and make sure constructorArgs is True on line 18. This will enable the framework to enter the arguments into the constructor when you launch the contract, then use the entered values to verify the contract on the block explorer (if desired) with the entered values. The types don't have to be specified as they will be interpreted from the contract abi via the help of w3js. 

#### Write your contract in the `/contracts` folder. Note that we have not tested contracts using libraries yet only single page.

#### Finally run `deploy.sh` (`python3 py/deploy.py`) 

#### If your rpc gives gas estimation issues it's because were calling `rpc.eth.gas_price` and sometimes this can be innacurate enough to revert the transaction. Increase the `gasMod` variable on line 19 of deploy.py to multiply the gas price by the desired amount. Feel free to change the equation to raise gas for your own needs, and ONLY use any real-live-mainnet gas tokens AT YOUR OWN RISK! Testnet First!
