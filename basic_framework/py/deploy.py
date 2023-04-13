constructorParamVals = ["0xFe4cc19ea6472582028641B2633d3adBB7685C69",69185539472004657639438318632082842238567383911850335774954207083492588994491,6728324303547297943133068617677977708565341909676784154631845952408332882505]
import pathlib
from pathlib import Path
import requests
import os
import time
from dotenv import load_dotenv
load_dotenv()
from web3 import Web3
from solcx import compile_standard, install_solc, compile_files
import json
import sys


solcV = os.getenv('SolidityCompilerVersion') #solidity compiler version
contractName = os.getenv('ContractName') #this variable is set when creating a new_frame
if contractName == None:
    contractName = "NOCONTRACTNAMECHOSEN" #for testing purposes to get rid of debug warning
xsol = ".sol"
xjson = ".json"
xtxt = ".txt"
xabi = "-abi"
xcomp = "-comp"
xbyte = "-bytecode"
contractDir = "./contracts/"
contractFile = contractName + xsol
constructorArgs = bool(os.getenv('ConstructorArgs'))
gasMod = 2
chain = os.getenv('CurrentChain') #set the current chain in .env


def getAccount():
    if chain == "Goerli":
        sys.stdout.write(os.getenv('GoerliSenderAddr'))
    elif chain == "Sepolia":
        sys.stdout.write(os.getenv("SepoliaSenderAddr"))


args_n = len(sys.argv)
if args_n > 1:
    if sys.argv[1] == "getAccount":
        getAccount()
        exit()


with open(contractDir + contractFile, "r") as file:
    contract = file.read()


if bool(os.getenv('VerifyBlockExplorer')) == True:
    verifyBlockExplorer = True
else:
    verifyBlockExplorer = False

if os.getenv('MultiFile') == "True": #flatten based on multifile arg
#changes the flattener config based on current contract expects flattener in base directory / prev directory / `../solidity-flattener`
    change_conf = "echo \'{\"inputFilePath\": \"../" + \
                contractName  + "/contracts/" + \
                contractName  + ".sol\",\"outputDir\": \"../" + \
                contractName  + "/contracts/\"}\' > ../solidity-flattener/config.json"
    c = os.popen(change_conf).read()
    print(c)
    flatOutput = os.popen("cd ../solidity-flattener/ && npm start").read()
    print(flatOutput)
    if "Success!" in flatOutput:
        print("flattened contract!")
        flat = open("contracts/" + contractName + "_flat.sol", "r")
    else:
        print("failed to flatten multi-file contract, verification wont succeed automatically!")
        if verifyBlockExplorer == True:
            exit(1)

install_solc(solcV)
#NOTE: Theoretically we can just default to compile_files later right now its convinient to use working impls
if os.getenv('MultiFile') == "False":
    compilation = compile_standard(
    {
        "language": "Solidity",
        "sources": {contractFile: {"content": contract}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                }
            }
        },
    },
        solc_version=solcV,
    )
else:
    contractsList = os.listdir('contracts')
    i = 0
    absPaths = []
    remapDict = {}
    for contract in contractsList:
        absPaths.append("./contracts/" + contract)
        remapDict[contract] = "./contracts/" + contract
    compilation = compile_files(
        absPaths,
        import_remappings=remapDict,
        solc_version=solcV,
    )




                            #set whether to verify on block explorer
                            #turn off when using ganache or anything else without one
#NOTE: Theoretically we can just default to compile_files later right now its convinient to use working impls
if os.getenv('MultiFile') == "False":
    #write contract compilation to json file
    #with open(contractName + xcomp + xjson, "w") as file:
    #    json.dump(compilation, file) #this tends to produce relatively large ~1mb files which are not used so we will keep this optional
    #get contract bytecode
    bytecode = compilation["contracts"][contractFile][contractName]["evm"]["bytecode"]["object"]
    #write bytecode to txt file
    with open(contractName + xbyte + xtxt, "w") as file:
        file.write(bytecode)
    #get abi
    abi = compilation["contracts"][contractFile][contractName]["abi"]
    #write abi to file
    with open(contractName + xabi + xjson, "w") as file:
        json.dump(abi, file)
else:
    #write contract compilation to json file
    #with open(contractName + xcomp + xjson, "w") as file:
    #    json.dump(compilation, file) ##this tends to produce relatively large ~1mb files which are not used so we will keep this optional
    #get contract bytecode
    bytecode = compilation[contractDir + contractName + xsol + ":" + contractName]['bin']
    #write bytecode to txt file
    with open(contractName + xbyte + xtxt, "w") as file:
        file.write(bytecode)
    #get abi
    abi = compilation[contractDir + contractName + xsol + ":" + contractName]['abi']
    #write abi to file
    with open(contractName + xabi + xjson, "w") as file:
        json.dump(abi, file)

#PICK THE CHAIN HERE #fills all chain specific args with env variables
if chain == "Goerli":
    rpc = Web3(Web3.HTTPProvider(os.getenv('Goerli')))
    chain_id = int(os.getenv('GoerliID')) #use int so it doesnt interpret env variable as string values
    senderAddr = os.getenv('GoerliSenderAddr')
    senderPrivKey = os.getenv('GoerliPrivKey')
    url = os.getenv('GoerliScan')
elif chain == "Sepolia":
    rpc = Web3(Web3.HTTPProvider(os.getenv('Sepolia')))
    chain_id = int(os.getenv('SepoliaID'))
    senderAddr = os.getenv('SepoliaSenderAddr')
    senderPrivKey = os.getenv('SepoliaPrivKey')
    url = os.getenv('SepoliaScan')


InitContract = rpc.eth.contract(abi=abi, bytecode=bytecode)

print("current gas price :", rpc.eth.gas_price );

if constructorArgs == True:

    tx = InitContract.constructor(*constructorParamVals).buildTransaction( #if we have constructor parameters we unwrap the array of their arguments into the constructor()
        {
            "chainId": chain_id, 
            "from": senderAddr, 
            "nonce": rpc.eth.getTransactionCount(senderAddr), 
            "gasPrice": rpc.eth.gas_price * gasMod
        }
    )
else:
    tx = InitContract.constructor().buildTransaction( 
        {
            "chainId": chain_id,
            "from": senderAddr,
            "nonce": rpc.eth.getTransactionCount(senderAddr),
            "gasPrice": rpc.eth.gas_price * gasMod
        }
    )

signedTx = rpc.eth.account.sign_transaction(tx, private_key=senderPrivKey)

tx_hash = rpc.eth.send_raw_transaction(signedTx.rawTransaction)
tx_receipt = rpc.eth.wait_for_transaction_receipt(tx_hash)
print(contractName, "Deployed!\n")
uploadedContract = rpc.eth.contract(address=tx_receipt.contractAddress, abi=abi)

APIsolcV = "v0.8.18-nightly.2023.1.25+commit.fd9ac9ab" #latest nightly as default
match solcV: #match solidity compiler version to API accepted verification version name
    case '0.6.0':
        APIsolcV = 'v0.6.0+commit.26b70077'
    case '0.6.12':
        APIsolcV = 'v0.6.12+commit.27d51765'
    case '0.7.5':
        APIsolcV = 'v0.7.5+commit.eb77ed08'
    case '0.7.6':
        APIsolcV = 'v0.7.6+commit.7338295f'
    case '0.8.0':                           #gets confusing at 8.0 need to make sure we arent skipping a generation
        APIsolcV = 'v0.8.0+commit.c7dfd78e'
    case '0.8.1':
        APIsolcV = 'v0.8.1+commit.df193b15'
    case '0.8.17':
        APIsolcV = 'v0.8.17+commit.8df45f5f'

#verifying the code on a block explorer
if verifyBlockExplorer == True: #https://docs.etherscan.io/tutorials/verifying-contracts-programmatically
    time.sleep(60)#give the explorer some time to register the transaction
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    if constructorArgs == False:
        if os.getenv('MultiFile') == "True":
            contract = flat
        content = { 
                'apikey': os.getenv('EtherscanAPIKey'),
                'module': 'contract',
                'action': 'verifysourcecode',
                'sourceCode': contract, #if failing make sure to flatten the contract https://github.com/BlockCatIO/solidity-flattener
                'contractaddress': tx_receipt.contractAddress,
                'codeformat': 'solidity-single-file',
                'contractname': contractName,
                'compilerversion': APIsolcV,
                'optimizationUsed': 0, #0 or 1
                'runs': 200,
                'evmversion': '',
                'licenseType': 5 #GPL 3
        }
    else:
        cmd = "node js/abiEnc.js " + contractName + " " + str(len(constructorParamVals)) #we will call the abiEnc.js program followed by contractname and constructor args
                                                                                        #to get the abi encoded constructor arguments
        for val in constructorParamVals:
            #loop through param val types if array convert it to pipe-able array
            if type(val) == list:
                strlist = "\"["
                for i in range(len(val)):
                    if i < len(val)-1:
                        strlist = strlist + "\\\"" + val[i] + "\\\","
                    else:
                        strlist = strlist + "\\\"" + val[i] + "\\\""
                strlist = strlist + "]\""
                val = strlist
            cmd = cmd + " " + str(val)
        encoding = os.popen(cmd).read()
        if os.getenv('MultiFile') == "True":
            contract = flat
#        print(encoding.replace(" ", "").replace("\n", "")) if auto-verify fails you can print the encoding and manually verify
        content = {
                'apikey': os.getenv('EtherscanAPIKey'),
                'module': 'contract',
                'action': 'verifysourcecode',
                'sourceCode': contract, #if failing make sure to flatten the contract https://github.com/BlockCatIO/solidity-flattener
                'contractaddress': tx_receipt.contractAddress,
                'codeformat': 'solidity-single-file',
                'contractname': contractName,
                'compilerversion': APIsolcV,
                'optimizationUsed': 0, #0 or 1
                'runs': 200,
                'constructorArguements': encoding.replace(" ", "").replace("\n", ""), #popen leaves empty space remove w replace()
                'evmversion': '',
                'licenseType': 5 #GPL 3
        }
    response = requests.post(url, headers=headers, data=content) #not sure how to properly check for response working though
    print(response.text)
