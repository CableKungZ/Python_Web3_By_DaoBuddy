from multiprocessing import Process, Value
import time
from web3 import Web3
from eth_account import Account
import ctypes
import os
import json
from web3.middleware import geth_poa_middleware


BaseGas = '2'

# Initialize Web3
web3 = Web3(Web3.HTTPProvider('http://49.13.16.167:8545'))
w3 = web3

def sign_and_send_transaction(transaction, private_key):
    signed_txn = web3.eth.account.sign_transaction(transaction, private_key)
    tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    return web3.to_hex(tx_hash)

contractABI = [
    {
        "constant": True,
        "inputs": [{"name": "_owner", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "balance", "type": "uint256"}],
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [
            {"name": "_to", "type": "address"},
            {"name": "_value", "type": "uint256"}
        ],
        "name": "transfer",
        "outputs": [{"name": "", "type": "bool"}],
        "type": "function"
    }
]
def send_erc20_tokens(sender_address, private_key, recipient_address, token_contract_address, token_symbol):
    # Load the ERC20 token contract ABI
    token_contract = w3.eth.contract(address=token_contract_address, abi=contractABI)

    # Get the token balance of the sender
    balance = token_contract.functions.balanceOf(sender_address).call()

    # Check if balance is greater than zero
    if balance > 0:
        # Encode the transfer function
        data = token_contract.encodeABI(fn_name='transfer', args=[recipient_address, balance])

        # Build the transaction
        transaction = {
            'to': token_contract_address,
            'value': 0,
            'gas': 100000,
            'gasPrice': w3.to_wei('5', 'gwei'),
            'nonce': w3.eth.get_transaction_count(sender_address),
            'chainId': w3.eth.chain_id,
            'data': data,
        }

        # Sign the transaction
        signed_txn = w3.eth.account.sign_transaction(transaction, private_key)

        # Send the transaction
        tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)

        # Wait for the transaction to be mined
        w3.eth.wait_for_transaction_receipt(tx_hash)

        print(f'Successfully sent {balance} {token_symbol} to {recipient_address}.')


def Balance(BotAddress,BotPrivatekey):
    # Define ERC20 contracts
    contracts = [
        {'address': '0xdbCCc9F8920e7274eeC62e695084D3bCe443c3dd', 'symbol': 'JTAO'},
        {'address': '0x0E2610730A3c42fd721B289BEe092D9AD1C76890', 'symbol': 'Gear'},
        {'address': '0x523AA3aB2371A6360BeC4fEea7bE1293adb32241', 'symbol': 'II'}
    ]

    # Load your wallet private key
    private_key = BotPrivatekey

    # Iterate over ERC20 contracts
    for contract in contracts:
        # Get the contract address and symbol
        token_contract_address = contract['address']
        token_symbol = contract['symbol']

        # Send ERC20 tokens
        send_erc20_tokens(BotAddress, private_key, '#input reciever Address', token_contract_address, token_symbol)

    
def worker(BotAddress, BotPrivateKey):
    Balance(BotAddress,BotPrivateKey)
    
def get_address_from_private_key(private_key):
    w3 = Web3()
    account = w3.eth.account.from_key(private_key)
    return account.address


# BOT เริ่มทำงานพร้อมกัน ทุกๆ ไอดี 

if __name__ == '__main__':
    private_keys = [
    #'PrivateKey',#1
    #'PrivateKey',#2

]

    IDcount = 0
    addresses = [get_address_from_private_key(pk) for pk in private_keys]

    processes = []

    for address, private_key in zip(addresses, private_keys):
        process = Process(target=worker, args=(address, private_key))
        processes.append(process)
        IDcount += 1
        print("[ID: ",IDcount,"]","Run : ",address)
        process.start()


    for process in processes:
        process.join()
