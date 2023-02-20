from web3 import Web3
import os
from dotenv import load_dotenv
load_dotenv()
print(Web3.keccak(int(os.getenv('preImage'), base=16)).hex())
