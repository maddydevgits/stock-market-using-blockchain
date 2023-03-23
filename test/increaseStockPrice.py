import json
from web3 import Web3,HTTPProvider

def connect_with_trades_blockchain(acc):
    server='http://127.0.0.1:7545'
    web3=Web3(HTTPProvider(server))
    if acc==0:
        acc=web3.eth.accounts[0]
    web3.eth.defaultAccount=acc
    artifact_path='../build/contracts/trades.json'
    with open(artifact_path) as f:
        contract_json=json.load(f)
        contract_abi=contract_json['abi']
        contract_address=contract_json['networks']['5777']['address']
    contract=web3.eth.contract(abi=contract_abi,address=contract_address)
    return (contract,web3)

contract,web3=connect_with_trades_blockchain(0)
tx_hash=contract.functions.increaseSharePrice('',100).transact()
web3.eth.waitForTransactionReceipt(tx_hash)