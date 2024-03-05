from multiprocessing import Process, Value
import time
from web3 import Web3
from eth_account import Account


BaseGas = '2'

# Initialize Web3
web3 = Web3(Web3.HTTPProvider('https://rpc-l1.jbc.aomwara.in.th'))


def sign_and_send_transaction(transaction, private_key):
    signed_txn = web3.eth.account.sign_transaction(transaction, private_key)
    tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    return web3.to_hex(tx_hash)


def ApproveJtao(address, privatekey):
    print("Approve JTAO")
    # Load the ABI for the contract
    global stage
    stage = 1
    contractABI = [{"type":"constructor","stateMutability":"nonpayable","inputs":[]},{"type":"event","name":"Approval","inputs":[{"type":"address","name":"owner","internalType":"address","indexed":True},{"type":"address","name":"spender","internalType":"address","indexed":True},{"type":"uint256","name":"value","internalType":"uint256","indexed":False}],"anonymous":False},{"type":"event","name":"OwnershipTransferred","inputs":[{"type":"address","name":"previousOwner","internalType":"address","indexed":True},{"type":"address","name":"newOwner","internalType":"address","indexed":True}],"anonymous":False},{"type":"event","name":"Transfer","inputs":[{"type":"address","name":"from","internalType":"address","indexed":True},{"type":"address","name":"to","internalType":"address","indexed":True},{"type":"uint256","name":"value","internalType":"uint256","indexed":False}],"anonymous":False},{"type":"function","stateMutability":"view","outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"allowance","inputs":[{"type":"address","name":"owner","internalType":"address"},{"type":"address","name":"spender","internalType":"address"}]},{"type":"function","stateMutability":"nonpayable","outputs":[{"type":"bool","name":"","internalType":"bool"}],"name":"approve","inputs":[{"type":"address","name":"spender","internalType":"address"},{"type":"uint256","name":"amount","internalType":"uint256"}]},{"type":"function","stateMutability":"view","outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"balanceOf","inputs":[{"type":"address","name":"account","internalType":"address"}]},{"type":"function","stateMutability":"view","outputs":[{"type":"uint8","name":"","internalType":"uint8"}],"name":"decimals","inputs":[]},{"type":"function","stateMutability":"nonpayable","outputs":[{"type":"bool","name":"","internalType":"bool"}],"name":"decreaseAllowance","inputs":[{"type":"address","name":"spender","internalType":"address"},{"type":"uint256","name":"subtractedValue","internalType":"uint256"}]},{"type":"function","stateMutability":"nonpayable","outputs":[{"type":"bool","name":"","internalType":"bool"}],"name":"increaseAllowance","inputs":[{"type":"address","name":"spender","internalType":"address"},{"type":"uint256","name":"addedValue","internalType":"uint256"}]},{"type":"function","stateMutability":"nonpayable","outputs":[],"name":"mint","inputs":[{"type":"address","name":"to","internalType":"address"},{"type":"uint256","name":"amount","internalType":"uint256"}]},{"type":"function","stateMutability":"view","outputs":[{"type":"string","name":"","internalType":"string"}],"name":"name","inputs":[]},{"type":"function","stateMutability":"view","outputs":[{"type":"address","name":"","internalType":"address"}],"name":"owner","inputs":[]},{"type":"function","stateMutability":"nonpayable","outputs":[],"name":"renounceOwnership","inputs":[]},{"type":"function","stateMutability":"view","outputs":[{"type":"string","name":"","internalType":"string"}],"name":"symbol","inputs":[]},{"type":"function","stateMutability":"view","outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"totalSupply","inputs":[]},{"type":"function","stateMutability":"nonpayable","outputs":[{"type":"bool","name":"","internalType":"bool"}],"name":"transfer","inputs":[{"type":"address","name":"to","internalType":"address"},{"type":"uint256","name":"amount","internalType":"uint256"}]},{"type":"function","stateMutability":"nonpayable","outputs":[{"type":"bool","name":"","internalType":"bool"}],"name":"transferFrom","inputs":[{"type":"address","name":"from","internalType":"address"},{"type":"address","name":"to","internalType":"address"},{"type":"uint256","name":"amount","internalType":"uint256"}]},{"type":"function","stateMutability":"nonpayable","outputs":[],"name":"transferOwnership","inputs":[{"type":"address","name":"newOwner","internalType":"address"}]}]
    JtaoContract = web3.eth.contract(address='0xdbCCc9F8920e7274eeC62e695084D3bCe443c3dd', abi=contractABI)
    # Add the method call to claim
    checksummed_spender_address = Web3.to_checksum_address('0x523aa3ab2371a6360bec4feea7be1293adb32241')
    claim_txn = JtaoContract.functions.approve(checksummed_spender_address,100000000000000004764729344).build_transaction({
        'chainId': 8899,
        'gas': 210000,
        'gasPrice': web3.to_wei(BaseGas, 'gwei'),
        'nonce': web3.eth.get_transaction_count(address),
    })
    # Sign and send the transaction
    print("Sending TX")
    tx_hash = sign_and_send_transaction(claim_txn, privatekey)
    while True:
        try:
            receipt = web3.eth.get_transaction_receipt(tx_hash)
            if receipt is not None:
                print("Transaction confirmed in block:", receipt['blockNumber'])
                break
            else:
                # Sleep for a few seconds before checking again
                time.sleep(2)
        except Exception as e:
            # Sleep for a few seconds before checking again
            time.sleep(0.1)

def ApproveGear(address, privatekey):
    print("Approve Gear")
    # Load the ABI for the contract
    global stage
    stage = 2
    contractABI =  [{"type":"constructor","stateMutability":"nonpayable","inputs":[{"type":"address","name":"_tdNft","internalType":"address"},{"type":"address","name":"_tmToken","internalType":"address"}]},{"type":"error","name":"ERC20InsufficientAllowance","inputs":[{"type":"address","name":"spender","internalType":"address"},{"type":"uint256","name":"allowance","internalType":"uint256"},{"type":"uint256","name":"needed","internalType":"uint256"}]},{"type":"error","name":"ERC20InsufficientBalance","inputs":[{"type":"address","name":"sender","internalType":"address"},{"type":"uint256","name":"balance","internalType":"uint256"},{"type":"uint256","name":"needed","internalType":"uint256"}]},{"type":"error","name":"ERC20InvalidApprover","inputs":[{"type":"address","name":"approver","internalType":"address"}]},{"type":"error","name":"ERC20InvalidReceiver","inputs":[{"type":"address","name":"receiver","internalType":"address"}]},{"type":"error","name":"ERC20InvalidSender","inputs":[{"type":"address","name":"sender","internalType":"address"}]},{"type":"error","name":"ERC20InvalidSpender","inputs":[{"type":"address","name":"spender","internalType":"address"}]},{"type":"error","name":"ReentrancyGuardReentrantCall","inputs":[]},{"type":"event","name":"Approval","inputs":[{"type":"address","name":"owner","internalType":"address","indexed":True},{"type":"address","name":"spender","internalType":"address","indexed":True},{"type":"uint256","name":"value","internalType":"uint256","indexed":False}],"anonymous":False},{"type":"event","name":"Claimed","inputs":[{"type":"uint256","name":"reward","internalType":"uint256","indexed":False},{"type":"bool","name":"isNft","internalType":"bool","indexed":True},{"type":"uint256","name":"tokenOrNftId","internalType":"uint256","indexed":True},{"type":"address","name":"owner","internalType":"address","indexed":True},{"type":"uint256","name":"timestamp","internalType":"uint256","indexed":False}],"anonymous":False},{"type":"event","name":"ItemStaked","inputs":[{"type":"bool","name":"isNft","internalType":"bool","indexed":True},{"type":"uint256","name":"tokenOrNftId","internalType":"uint256","indexed":True},{"type":"address","name":"owner","internalType":"address","indexed":True},{"type":"uint256","name":"timestamp","internalType":"uint256","indexed":False}],"anonymous":False},{"type":"event","name":"ItemUnstaked","inputs":[{"type":"bool","name":"isNft","internalType":"bool","indexed":True},{"type":"uint256","name":"tokenOrNftId","internalType":"uint256","indexed":True},{"type":"address","name":"owner","internalType":"address","indexed":True},{"type":"uint256","name":"timestamp","internalType":"uint256","indexed":False}],"anonymous":False},{"type":"event","name":"Transfer","inputs":[{"type":"address","name":"from","internalType":"address","indexed":True},{"type":"address","name":"to","internalType":"address","indexed":True},{"type":"uint256","name":"value","internalType":"uint256","indexed":False}],"anonymous":False},{"type":"function","stateMutability":"view","outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"allowance","inputs":[{"type":"address","name":"owner","internalType":"address"},{"type":"address","name":"spender","internalType":"address"}]},{"type":"function","stateMutability":"nonpayable","outputs":[{"type":"bool","name":"","internalType":"bool"}],"name":"approve","inputs":[{"type":"address","name":"spender","internalType":"address"},{"type":"uint256","name":"value","internalType":"uint256"}]},{"type":"function","stateMutability":"view","outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"balanceOf","inputs":[{"type":"address","name":"account","internalType":"address"}]},{"type":"function","stateMutability":"view","outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"calculateRewards","inputs":[{"type":"uint256","name":"_tokenIdorAmount","internalType":"uint256"},{"type":"address","name":"_addr","internalType":"address"},{"type":"bool","name":"_isNft","internalType":"bool"}]},{"type":"function","stateMutability":"view","outputs":[{"type":"uint8","name":"","internalType":"uint8"}],"name":"decimals","inputs":[]},{"type":"function","stateMutability":"view","outputs":[{"type":"string","name":"","internalType":"string"}],"name":"name","inputs":[]},{"type":"function","stateMutability":"view","outputs":[{"type":"address","name":"tokenOwnerOf","internalType":"address"},{"type":"uint256","name":"tokenStakedAt","internalType":"uint256"},{"type":"uint256","name":"power","internalType":"uint256"}],"name":"nftStake","inputs":[{"type":"uint256","name":"","internalType":"uint256"}]},{"type":"function","stateMutability":"nonpayable","outputs":[{"type":"bytes4","name":"","internalType":"bytes4"}],"name":"onERC721Received","inputs":[{"type":"address","name":"","internalType":"address"},{"type":"address","name":"","internalType":"address"},{"type":"uint256","name":"","internalType":"uint256"},{"type":"bytes","name":"","internalType":"bytes"}]},{"type":"function","stateMutability":"view","outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"power","inputs":[{"type":"uint256","name":"","internalType":"uint256"}]},{"type":"function","stateMutability":"nonpayable","outputs":[],"name":"stake","inputs":[{"type":"uint256","name":"_tokenIdorAmount","internalType":"uint256"},{"type":"bool","name":"_isNft","internalType":"bool"}]},{"type":"function","stateMutability":"view","outputs":[{"type":"string","name":"","internalType":"string"}],"name":"symbol","inputs":[]},{"type":"function","stateMutability":"view","outputs":[{"type":"address","name":"","internalType":"address"}],"name":"tdNft","inputs":[]},{"type":"function","stateMutability":"view","outputs":[{"type":"address","name":"","internalType":"address"}],"name":"tmToken","inputs":[]},{"type":"function","stateMutability":"view","outputs":[{"type":"uint256","name":"tokenAmount","internalType":"uint256"},{"type":"uint256","name":"tokenStakedAt","internalType":"uint256"},{"type":"uint256","name":"power","internalType":"uint256"}],"name":"tokenStake","inputs":[{"type":"address","name":"","internalType":"address"}]},{"type":"function","stateMutability":"view","outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"totalSupply","inputs":[]},{"type":"function","stateMutability":"nonpayable","outputs":[{"type":"bool","name":"","internalType":"bool"}],"name":"transfer","inputs":[{"type":"address","name":"to","internalType":"address"},{"type":"uint256","name":"value","internalType":"uint256"}]},{"type":"function","stateMutability":"nonpayable","outputs":[{"type":"bool","name":"","internalType":"bool"}],"name":"transferFrom","inputs":[{"type":"address","name":"from","internalType":"address"},{"type":"address","name":"to","internalType":"address"},{"type":"uint256","name":"value","internalType":"uint256"}]},{"type":"function","stateMutability":"nonpayable","outputs":[],"name":"unstake","inputs":[{"type":"uint256","name":"_tokenIdorAmount","internalType":"uint256"},{"type":"bool","name":"_isNft","internalType":"bool"},{"type":"bool","name":"_unstake","internalType":"bool"}]}]
    GearContract = web3.eth.contract(address='0x0E2610730A3c42fd721B289BEe092D9AD1C76890', abi=contractABI)
    # Add the method call to claim
    checksummed_spender_address = Web3.to_checksum_address('0x523aa3ab2371a6360bec4feea7be1293adb32241')
    claim_txn = GearContract.functions.approve(checksummed_spender_address,100000000000000004764729344).build_transaction({
        'chainId': 8899,
        'gas': 210000,
        'gasPrice': web3.to_wei(BaseGas, 'gwei'),
        'nonce': web3.eth.get_transaction_count(address),
    })
    # Sign and send the transaction
    print("Sending TX")
    tx_hash = sign_and_send_transaction(claim_txn, privatekey)
    while True:
        try:
            receipt = web3.eth.get_transaction_receipt(tx_hash)
            if receipt is not None:
                print("Transaction confirmed in block:", receipt['blockNumber'])
                break
            else:
                # Sleep for a few seconds before checking again
                time.sleep(2)
        except Exception as e:
            # Sleep for a few seconds before checking again
            time.sleep(0.1)

def CraftII(address,privatekey):
    print("Crafting II")
    global stage 
    stage = 4
    contractABI = [{"type":"constructor","stateMutability":"nonpayable","inputs":[{"type":"string","name":"_rewardName","internalType":"string"},{"type":"string","name":"_rewardSymbol","internalType":"string"},{"type":"address","name":"_resource1","internalType":"address"},{"type":"address","name":"_resource2","internalType":"address"},{"type":"address","name":"_currency","internalType":"address"},{"type":"address","name":"_labsOwner","internalType":"address"},{"type":"uint256","name":"_premintAmount","internalType":"uint256"}]},{"type":"error","name":"ERC20InsufficientAllowance","inputs":[{"type":"address","name":"spender","internalType":"address"},{"type":"uint256","name":"allowance","internalType":"uint256"},{"type":"uint256","name":"needed","internalType":"uint256"}]},{"type":"error","name":"ERC20InsufficientBalance","inputs":[{"type":"address","name":"sender","internalType":"address"},{"type":"uint256","name":"balance","internalType":"uint256"},{"type":"uint256","name":"needed","internalType":"uint256"}]},{"type":"error","name":"ERC20InvalidApprover","inputs":[{"type":"address","name":"approver","internalType":"address"}]},{"type":"error","name":"ERC20InvalidReceiver","inputs":[{"type":"address","name":"receiver","internalType":"address"}]},{"type":"error","name":"ERC20InvalidSender","inputs":[{"type":"address","name":"sender","internalType":"address"}]},{"type":"error","name":"ERC20InvalidSpender","inputs":[{"type":"address","name":"spender","internalType":"address"}]},{"type":"error","name":"OwnableInvalidOwner","inputs":[{"type":"address","name":"owner","internalType":"address"}]},{"type":"error","name":"OwnableUnauthorizedAccount","inputs":[{"type":"address","name":"account","internalType":"address"}]},{"type":"event","name":"Approval","inputs":[{"type":"address","name":"owner","internalType":"address","indexed":True},{"type":"address","name":"spender","internalType":"address","indexed":True},{"type":"uint256","name":"value","internalType":"uint256","indexed":False}],"anonymous":False},{"type":"event","name":"OwnershipTransferred","inputs":[{"type":"address","name":"previousOwner","internalType":"address","indexed":True},{"type":"address","name":"newOwner","internalType":"address","indexed":True}],"anonymous":False},{"type":"event","name":"Transfer","inputs":[{"type":"address","name":"from","internalType":"address","indexed":True},{"type":"address","name":"to","internalType":"address","indexed":True},{"type":"uint256","name":"value","internalType":"uint256","indexed":False}],"anonymous":False},{"type":"function","stateMutability":"view","outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"allowance","inputs":[{"type":"address","name":"owner","internalType":"address"},{"type":"address","name":"spender","internalType":"address"}]},{"type":"function","stateMutability":"nonpayable","outputs":[{"type":"bool","name":"","internalType":"bool"}],"name":"approve","inputs":[{"type":"address","name":"spender","internalType":"address"},{"type":"uint256","name":"value","internalType":"uint256"}]},{"type":"function","stateMutability":"view","outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"balanceOf","inputs":[{"type":"address","name":"account","internalType":"address"}]},{"type":"function","stateMutability":"nonpayable","outputs":[],"name":"cmdao20Burn","inputs":[{"type":"address","name":"_from","internalType":"address"},{"type":"uint256","name":"_amount","internalType":"uint256"}]},{"type":"function","stateMutability":"nonpayable","outputs":[],"name":"cmdao20Mint","inputs":[{"type":"uint256","name":"_callIndex","internalType":"uint256"},{"type":"address","name":"_to","internalType":"address"},{"type":"uint256","name":"_amount","internalType":"uint256"}]},{"type":"function","stateMutability":"nonpayable","outputs":[],"name":"craft","inputs":[{"type":"uint256","name":"_index","internalType":"uint256"}]},{"type":"function","stateMutability":"view","outputs":[{"type":"address","name":"","internalType":"address"}],"name":"currency","inputs":[]},{"type":"function","stateMutability":"view","outputs":[{"type":"uint8","name":"","internalType":"uint8"}],"name":"decimals","inputs":[]},{"type":"function","stateMutability":"view","outputs":[{"type":"uint256","name":"duration","internalType":"uint256"},{"type":"uint256","name":"res1Cost","internalType":"uint256"},{"type":"uint256","name":"res2Cost","internalType":"uint256"},{"type":"uint256","name":"currCost","internalType":"uint256"},{"type":"uint256","name":"rewardAmount","internalType":"uint256"}],"name":"machine","inputs":[{"type":"uint256","name":"","internalType":"uint256"}]},{"type":"function","stateMutability":"view","outputs":[{"type":"string","name":"","internalType":"string"}],"name":"name","inputs":[]},{"type":"function","stateMutability":"nonpayable","outputs":[],"name":"obtain","inputs":[]},{"type":"function","stateMutability":"view","outputs":[{"type":"address","name":"","internalType":"address"}],"name":"owner","inputs":[]},{"type":"function","stateMutability":"view","outputs":[{"type":"address","name":"","internalType":"address"}],"name":"programCall","inputs":[{"type":"uint256","name":"","internalType":"uint256"}]},{"type":"function","stateMutability":"nonpayable","outputs":[],"name":"renounceOwnership","inputs":[]},{"type":"function","stateMutability":"view","outputs":[{"type":"address","name":"","internalType":"address"}],"name":"resource1","inputs":[]},{"type":"function","stateMutability":"view","outputs":[{"type":"address","name":"","internalType":"address"}],"name":"resource2","inputs":[]},{"type":"function","stateMutability":"nonpayable","outputs":[],"name":"setMachine","inputs":[{"type":"uint256","name":"_index","internalType":"uint256"},{"type":"uint256","name":"_durationInMin","internalType":"uint256"},{"type":"uint256","name":"_res1Cost","internalType":"uint256"},{"type":"uint256","name":"_res2Cost","internalType":"uint256"},{"type":"uint256","name":"_currCost","internalType":"uint256"},{"type":"uint256","name":"_rewardAmount","internalType":"uint256"}]},{"type":"function","stateMutability":"nonpayable","outputs":[],"name":"setProgramCall","inputs":[{"type":"uint256","name":"_index","internalType":"uint256"},{"type":"address","name":"_addr","internalType":"address"}]},{"type":"function","stateMutability":"view","outputs":[{"type":"uint256","name":"machineRun","internalType":"uint256"},{"type":"uint256","name":"laststamp","internalType":"uint256"}],"name":"supplier","inputs":[{"type":"address","name":"","internalType":"address"}]},{"type":"function","stateMutability":"view","outputs":[{"type":"string","name":"","internalType":"string"}],"name":"symbol","inputs":[]},{"type":"function","stateMutability":"view","outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"totalSupply","inputs":[]},{"type":"function","stateMutability":"nonpayable","outputs":[{"type":"bool","name":"","internalType":"bool"}],"name":"transfer","inputs":[{"type":"address","name":"to","internalType":"address"},{"type":"uint256","name":"value","internalType":"uint256"}]},{"type":"function","stateMutability":"nonpayable","outputs":[{"type":"bool","name":"","internalType":"bool"}],"name":"transferFrom","inputs":[{"type":"address","name":"from","internalType":"address"},{"type":"address","name":"to","internalType":"address"},{"type":"uint256","name":"value","internalType":"uint256"}]},{"type":"function","stateMutability":"nonpayable","outputs":[],"name":"transferOwnership","inputs":[{"type":"address","name":"newOwner","internalType":"address"}]},{"type":"function","stateMutability":"nonpayable","outputs":[],"name":"withdrawCurrency","inputs":[{"type":"uint256","name":"_amount","internalType":"uint256"},{"type":"address","name":"_to","internalType":"address"}]}]
    Craftcontract = web3.eth.contract(address='0x523AA3aB2371A6360BeC4fEea7bE1293adb32241', abi=contractABI)
    claim_txn = Craftcontract.functions.craft(1).build_transaction({
        'chainId': 8899,
        'gas': 210000,
        'gasPrice': web3.to_wei(BaseGas, 'gwei'),
        'nonce': web3.eth.get_transaction_count(address),
    })
    # Sign and send the transaction
    print("Sending TX")
    tx_hash = sign_and_send_transaction(claim_txn, privatekey)
    while True:
        try:
            receipt = web3.eth.get_transaction_receipt(tx_hash)
            if receipt is not None:
                print("Transaction confirmed in block:", receipt['blockNumber'])
                break
            else:
                # Sleep for a few seconds before checking again
                time.sleep(2)
        except Exception as e:
            # Sleep for a few seconds before checking again
            time.sleep(0.1)

def ObtainII(address,privatekey):
    print("Obtain II")
    global stage 
    stage = 3
    contractABI = [{"type":"constructor","stateMutability":"nonpayable","inputs":[{"type":"string","name":"_rewardName","internalType":"string"},{"type":"string","name":"_rewardSymbol","internalType":"string"},{"type":"address","name":"_resource1","internalType":"address"},{"type":"address","name":"_resource2","internalType":"address"},{"type":"address","name":"_currency","internalType":"address"},{"type":"address","name":"_labsOwner","internalType":"address"},{"type":"uint256","name":"_premintAmount","internalType":"uint256"}]},{"type":"error","name":"ERC20InsufficientAllowance","inputs":[{"type":"address","name":"spender","internalType":"address"},{"type":"uint256","name":"allowance","internalType":"uint256"},{"type":"uint256","name":"needed","internalType":"uint256"}]},{"type":"error","name":"ERC20InsufficientBalance","inputs":[{"type":"address","name":"sender","internalType":"address"},{"type":"uint256","name":"balance","internalType":"uint256"},{"type":"uint256","name":"needed","internalType":"uint256"}]},{"type":"error","name":"ERC20InvalidApprover","inputs":[{"type":"address","name":"approver","internalType":"address"}]},{"type":"error","name":"ERC20InvalidReceiver","inputs":[{"type":"address","name":"receiver","internalType":"address"}]},{"type":"error","name":"ERC20InvalidSender","inputs":[{"type":"address","name":"sender","internalType":"address"}]},{"type":"error","name":"ERC20InvalidSpender","inputs":[{"type":"address","name":"spender","internalType":"address"}]},{"type":"error","name":"OwnableInvalidOwner","inputs":[{"type":"address","name":"owner","internalType":"address"}]},{"type":"error","name":"OwnableUnauthorizedAccount","inputs":[{"type":"address","name":"account","internalType":"address"}]},{"type":"event","name":"Approval","inputs":[{"type":"address","name":"owner","internalType":"address","indexed":True},{"type":"address","name":"spender","internalType":"address","indexed":True},{"type":"uint256","name":"value","internalType":"uint256","indexed":False}],"anonymous":False},{"type":"event","name":"OwnershipTransferred","inputs":[{"type":"address","name":"previousOwner","internalType":"address","indexed":True},{"type":"address","name":"newOwner","internalType":"address","indexed":True}],"anonymous":False},{"type":"event","name":"Transfer","inputs":[{"type":"address","name":"from","internalType":"address","indexed":True},{"type":"address","name":"to","internalType":"address","indexed":True},{"type":"uint256","name":"value","internalType":"uint256","indexed":False}],"anonymous":False},{"type":"function","stateMutability":"view","outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"allowance","inputs":[{"type":"address","name":"owner","internalType":"address"},{"type":"address","name":"spender","internalType":"address"}]},{"type":"function","stateMutability":"nonpayable","outputs":[{"type":"bool","name":"","internalType":"bool"}],"name":"approve","inputs":[{"type":"address","name":"spender","internalType":"address"},{"type":"uint256","name":"value","internalType":"uint256"}]},{"type":"function","stateMutability":"view","outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"balanceOf","inputs":[{"type":"address","name":"account","internalType":"address"}]},{"type":"function","stateMutability":"nonpayable","outputs":[],"name":"cmdao20Burn","inputs":[{"type":"address","name":"_from","internalType":"address"},{"type":"uint256","name":"_amount","internalType":"uint256"}]},{"type":"function","stateMutability":"nonpayable","outputs":[],"name":"cmdao20Mint","inputs":[{"type":"uint256","name":"_callIndex","internalType":"uint256"},{"type":"address","name":"_to","internalType":"address"},{"type":"uint256","name":"_amount","internalType":"uint256"}]},{"type":"function","stateMutability":"nonpayable","outputs":[],"name":"craft","inputs":[{"type":"uint256","name":"_index","internalType":"uint256"}]},{"type":"function","stateMutability":"view","outputs":[{"type":"address","name":"","internalType":"address"}],"name":"currency","inputs":[]},{"type":"function","stateMutability":"view","outputs":[{"type":"uint8","name":"","internalType":"uint8"}],"name":"decimals","inputs":[]},{"type":"function","stateMutability":"view","outputs":[{"type":"uint256","name":"duration","internalType":"uint256"},{"type":"uint256","name":"res1Cost","internalType":"uint256"},{"type":"uint256","name":"res2Cost","internalType":"uint256"},{"type":"uint256","name":"currCost","internalType":"uint256"},{"type":"uint256","name":"rewardAmount","internalType":"uint256"}],"name":"machine","inputs":[{"type":"uint256","name":"","internalType":"uint256"}]},{"type":"function","stateMutability":"view","outputs":[{"type":"string","name":"","internalType":"string"}],"name":"name","inputs":[]},{"type":"function","stateMutability":"nonpayable","outputs":[],"name":"obtain","inputs":[]},{"type":"function","stateMutability":"view","outputs":[{"type":"address","name":"","internalType":"address"}],"name":"owner","inputs":[]},{"type":"function","stateMutability":"view","outputs":[{"type":"address","name":"","internalType":"address"}],"name":"programCall","inputs":[{"type":"uint256","name":"","internalType":"uint256"}]},{"type":"function","stateMutability":"nonpayable","outputs":[],"name":"renounceOwnership","inputs":[]},{"type":"function","stateMutability":"view","outputs":[{"type":"address","name":"","internalType":"address"}],"name":"resource1","inputs":[]},{"type":"function","stateMutability":"view","outputs":[{"type":"address","name":"","internalType":"address"}],"name":"resource2","inputs":[]},{"type":"function","stateMutability":"nonpayable","outputs":[],"name":"setMachine","inputs":[{"type":"uint256","name":"_index","internalType":"uint256"},{"type":"uint256","name":"_durationInMin","internalType":"uint256"},{"type":"uint256","name":"_res1Cost","internalType":"uint256"},{"type":"uint256","name":"_res2Cost","internalType":"uint256"},{"type":"uint256","name":"_currCost","internalType":"uint256"},{"type":"uint256","name":"_rewardAmount","internalType":"uint256"}]},{"type":"function","stateMutability":"nonpayable","outputs":[],"name":"setProgramCall","inputs":[{"type":"uint256","name":"_index","internalType":"uint256"},{"type":"address","name":"_addr","internalType":"address"}]},{"type":"function","stateMutability":"view","outputs":[{"type":"uint256","name":"machineRun","internalType":"uint256"},{"type":"uint256","name":"laststamp","internalType":"uint256"}],"name":"supplier","inputs":[{"type":"address","name":"","internalType":"address"}]},{"type":"function","stateMutability":"view","outputs":[{"type":"string","name":"","internalType":"string"}],"name":"symbol","inputs":[]},{"type":"function","stateMutability":"view","outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"totalSupply","inputs":[]},{"type":"function","stateMutability":"nonpayable","outputs":[{"type":"bool","name":"","internalType":"bool"}],"name":"transfer","inputs":[{"type":"address","name":"to","internalType":"address"},{"type":"uint256","name":"value","internalType":"uint256"}]},{"type":"function","stateMutability":"nonpayable","outputs":[{"type":"bool","name":"","internalType":"bool"}],"name":"transferFrom","inputs":[{"type":"address","name":"from","internalType":"address"},{"type":"address","name":"to","internalType":"address"},{"type":"uint256","name":"value","internalType":"uint256"}]},{"type":"function","stateMutability":"nonpayable","outputs":[],"name":"transferOwnership","inputs":[{"type":"address","name":"newOwner","internalType":"address"}]},{"type":"function","stateMutability":"nonpayable","outputs":[],"name":"withdrawCurrency","inputs":[{"type":"uint256","name":"_amount","internalType":"uint256"},{"type":"address","name":"_to","internalType":"address"}]}]
    Craftcontract = web3.eth.contract(address='0x523AA3aB2371A6360BeC4fEea7bE1293adb32241', abi=contractABI)
    claim_txn = Craftcontract.functions.obtain().build_transaction({
        'chainId': 8899,
        'gas': 210000,
        'gasPrice': web3.to_wei(BaseGas, 'gwei'),
        'nonce': web3.eth.get_transaction_count(address),
    })
    # Sign and send the transaction
    print("Sending TX")
    tx_hash = sign_and_send_transaction(claim_txn, privatekey)
    while True:
        try:
            receipt = web3.eth.get_transaction_receipt(tx_hash)
            if receipt is not None:
                print("Transaction confirmed in block:", receipt['blockNumber'])
                break
            else:
                # Sleep for a few seconds before checking again
                time.sleep(2)
        except Exception as e:
            # Sleep for a few seconds before checking again
            time.sleep(0.1)



def worker(BotAddress, BotPrivateKey):
    stage = 1  # Initialize the stage for each bot
    attempt = 0  # Initialize the attempt counter

    while True:
        try:
            if stage == 1:
                ApproveJtao(BotAddress, BotPrivateKey)
                stage = 2  # Proceed to the next stage
            elif stage == 2:
                ApproveGear(BotAddress, BotPrivateKey)
                stage = 3  # Proceed to the next stage
            elif stage == 3:
                ObtainII(BotAddress, BotPrivateKey)
                stage = 4  # Proceed to the next stage
                
            elif stage == 4:
                CraftII(BotAddress, BotPrivateKey)
                stage = 3  # Proceed to the next stage
                print("Sleep For 30 Minutes")
                time.sleep(1805) #Sleep for 30 minutes
        except Exception as e:
            attempt += 1
            if attempt > 20:
                stage = 3  # Reset the stage after too many attempts
                print(f"Attempts : {attempt}")
                attempt = 0  # Reset the attempt counter
            time.sleep(2)  # Wait before retrying

def get_address_from_private_key(private_key):
    w3 = Web3()
    account = w3.eth.account.from_key(private_key)
    return account.address


# BOT เริ่มทำงานพร้อมกัน ทุกๆ ไอดี 

if __name__ == '__main__':
    private_keys = [
    'PrivateKey_01',
    'PrivateKey_02',
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
