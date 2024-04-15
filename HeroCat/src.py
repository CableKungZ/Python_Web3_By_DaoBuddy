import os, requests, json , time
from web3 import Web3, AsyncWeb3
from multiprocessing import Process
from web3.exceptions import TransactionNotFound
from eth_account import Account
import tkinter as tk
from tkinter import messagebox
import getpass


global w3
w3 = Web3(Web3.HTTPProvider('https://bbqchain-rpc.commudao.xyz', request_kwargs={'timeout': 90}))

PROVIDER_URLS = [
    'https://bbqchain-rpc.commudao.xyz',
]

def switch_provider():
    for url in PROVIDER_URLS:
        try:
            w3 = Web3(Web3.HTTPProvider(url, request_kwargs={'timeout': 90}))
            if w3.is_connected():
                print(f"Connected to {url}")
                return w3  # Return the Web3 instance connected to the working provider
        except Exception as e:
            print(f"Failed to connect to {url}: {str(e)}")
    raise Exception("All providers failed. Check network connection or provider URLs.")

def sendTransaction(txData, BotAddress, BotPrivateKey, gasSet=False):
    txData['nonce'] = w3.eth.get_transaction_count(BotAddress)
    if gasSet and 'gas' not in txData:
        txData['gas'] = w3.eth.estimate_gas(txData)
    if gasSet and 'gasPrice' not in txData:
        txData['gasPrice'] = Web3.to_wei(5, 'gwei')
    signedTx = w3.eth.account.sign_transaction(txData, private_key=BotPrivateKey)
    tx_hash = w3.eth.send_raw_transaction(signedTx.rawTransaction)
    print('\ttx_hash: ' + str(tx_hash.hex()))
    print("\ttransaction confirm.", end='')
    while True:
        time.sleep(1)
        try:
            tx_receipt = w3.eth.get_transaction_receipt(tx_hash)
            if tx_receipt is not None:
                current_block_number = w3.eth.block_number
                block_number = tx_receipt['blockNumber']
                confirmations = current_block_number - block_number + 1
                if confirmations >= 1:
                    print(confirmations)
                    break
                else:
                    print('.', end='')
        except TransactionNotFound:
            print('#', end='')  
            continue
    return tx_hash

def sendNativeToken(account,toAddress,value):
    txRaw = {
        'from': account.address,
        'to': toAddress,
        'value': Web3.to_wei(value, 'ether'),
        'chainId': 190
    }
    hashTx = sendTransaction(txRaw,account,True)


web3 = w3

############################################################################################
############################### 
print('Loading All Contract ABI') ##########################
############################################################################################
Hero_ContractABI = [{"inputs":[{"internalType":"address","name":"_charContract","type":"address"},{"internalType":"address","name":"_equipContract","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[],"name":"ReentrancyGuardReentrantCall","type":"error"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"uint256","name":"tokenId","type":"uint256"},{"indexed":True,"internalType":"uint256","name":"charId","type":"uint256"},{"indexed":True,"internalType":"address","name":"delegator","type":"address"}],"name":"Equiped","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"holder","type":"address"},{"indexed":True,"internalType":"uint256","name":"charId","type":"uint256"},{"indexed":True,"internalType":"address","name":"characterOwner","type":"address"},{"indexed":False,"internalType":"uint256","name":"timestamp","type":"uint256"}],"name":"InstallHolder","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"holder","type":"address"},{"indexed":True,"internalType":"uint256","name":"charId","type":"uint256"},{"indexed":True,"internalType":"address","name":"characterOwner","type":"address"},{"indexed":False,"internalType":"uint256","name":"timestamp","type":"uint256"}],"name":"ReleaseHolder","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"uint256","name":"tokenId","type":"uint256"},{"indexed":True,"internalType":"uint256","name":"charId","type":"uint256"},{"indexed":True,"internalType":"address","name":"delegator","type":"address"}],"name":"Unequiped","type":"event"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"allowCharacter","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"charContract","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_delegator","type":"address"},{"internalType":"uint256","name":"_index","type":"uint256"}],"name":"characterOfOwnerByIndex","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_delegator","type":"address"}],"name":"characterOwnerBalanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_charId","type":"uint256"},{"internalType":"uint256","name":"_tokenId","type":"uint256"}],"name":"equip","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"equipContract","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_charOwner","type":"address"},{"internalType":"uint256","name":"_charId","type":"uint256"},{"internalType":"bool","name":"check","type":"bool"}],"name":"installHolder","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"uint256","name":"","type":"uint256"}],"name":"nftEquip","outputs":[{"internalType":"uint256","name":"charId","type":"uint256"},{"internalType":"uint256","name":"power","type":"uint256"},{"internalType":"address","name":"holder","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_delegator","type":"address"},{"internalType":"uint256","name":"_charId","type":"uint256"}],"name":"nftEquipHolder","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_delegator","type":"address"},{"internalType":"uint256","name":"_charId","type":"uint256"}],"name":"nftEquipInfo","outputs":[{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_delegator","type":"address"},{"internalType":"uint256","name":"_charId","type":"uint256"}],"name":"nftEquipItemsInfo","outputs":[{"internalType":"uint256[]","name":"","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_delegator","type":"address"},{"internalType":"uint256","name":"_charId","type":"uint256"}],"name":"nftEquipPower","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"address","name":"","type":"address"},{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"bytes","name":"","type":"bytes"}],"name":"onERC721Received","outputs":[{"internalType":"bytes4","name":"","type":"bytes4"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"projectAdmin","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"proxies","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_charOwner","type":"address"},{"internalType":"uint256","name":"_charId","type":"uint256"}],"name":"releaseHolder","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"itemId","type":"uint256"},{"internalType":"bool","name":"permission","type":"bool"}],"name":"setAllowCharacter","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"bool","name":"permission","type":"bool"}],"name":"setPermission","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_address","type":"address"}],"name":"setProjectAdmin","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_charOwner","type":"address"},{"internalType":"address","name":"_newOwner","type":"address"},{"internalType":"uint256","name":"_charId","type":"uint256"}],"name":"transferCharacter","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_charId","type":"uint256"},{"internalType":"uint256","name":"_slot","type":"uint256"}],"name":"unEquip","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_charOwner","type":"address"},{"internalType":"uint256","name":"_charId","type":"uint256"},{"internalType":"uint256","name":"_newTokenId","type":"uint256"}],"name":"upgradeCharacter","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_charOwner","type":"address"},{"internalType":"uint256","name":"_charId","type":"uint256"},{"internalType":"uint256","name":"_newTokenId","type":"uint256"}],"name":"upgradeItem","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"}]
apple_farmABI = [{"inputs":[{"internalType":"address","name":"_rewardContract","type":"address"},{"internalType":"address","name":"_platformerContract","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[],"name":"ReentrancyGuardReentrantCall","type":"error"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"delegator","type":"address"},{"indexed":True,"internalType":"uint256","name":"charId","type":"uint256"}],"name":"Farmed","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"delegator","type":"address"},{"indexed":True,"internalType":"uint256","name":"charId","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"RewardClaimed","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"delegator","type":"address"},{"indexed":True,"internalType":"uint256","name":"charId","type":"uint256"}],"name":"Unfarmd","type":"event"},{"inputs":[],"name":"REWARD_DAY","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"REWARD_EXPIRE","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"allowFarm","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"delegator","type":"address"},{"internalType":"uint256","name":"charId","type":"uint256"}],"name":"calculateRewards","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_delegator","type":"address"},{"internalType":"uint256","name":"_index","type":"uint256"}],"name":"characterOfOwnerByIndex","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_delegator","type":"address"}],"name":"characterOwnerBalanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_charId","type":"uint256"}],"name":"claimReward","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"claimRewardAll","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_charId","type":"uint256"}],"name":"farm","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_delegator","type":"address"},{"internalType":"uint256","name":"_charId","type":"uint256"}],"name":"farmInfo","outputs":[{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"uint256","name":"","type":"uint256"}],"name":"farms","outputs":[{"internalType":"uint256","name":"charId","type":"uint256"},{"internalType":"uint256","name":"power","type":"uint256"},{"internalType":"uint256","name":"lastUpdateTime","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_charId","type":"uint256"}],"name":"forceUnFarm","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"platformerContract","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"projectAdmin","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"rewardContract","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"rewardMax","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"rewardMultiply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"itemId","type":"uint256"},{"internalType":"bool","name":"permission","type":"bool"}],"name":"setAllowFarm","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_address","type":"address"}],"name":"setProjectAdmin","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"uint256","name":"day","type":"uint256"}],"name":"setRewardMax","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"rate","type":"uint256"}],"name":"setRewardMultiply","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"totalFarmed","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalPower","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_charId","type":"uint256"}],"name":"unFarm","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"}]



Hero_Contract = w3.eth.contract(address=Web3.to_checksum_address('0xb172a2b8d9839f751a64b63dba47bc60bf9e76fe'),abi=Hero_ContractABI)
appl_farm = w3.eth.contract(address=Web3.to_checksum_address('0x73162b2D5138DC3e9Ac69C43C5CAfb0992CA1FFC'),abi=apple_farmABI)

############################################################################################
############################################################################################
############################################################################################

def get_address_from_private_key(private_key):
    w3 = Web3()
    account = w3.eth.account.from_key(private_key)
    return account.address

def eqiupHero(address, privatekey):
    amountOfHero = Hero_Contract.functions.characterOwnerBalanceOf(address).call()
    print(f"Hero in camp : {amountOfHero}")
    
    for index in range(amountOfHero):
        Indexcall = int(index)
        HeroID = Hero_Contract.functions.characterOfOwnerByIndex(address, Indexcall).call()
        HeroPow = Hero_Contract.functions.nftEquipPower(address, HeroID).call()
        PendingReward = appl_farm.functions.calculateRewards(address, HeroID).call()
        if PendingReward != 0:
            print(f"HERO ID: {HeroID} Pow : {HeroPow} *Appl Farm")
        else:
            print(f"HERO ID: {HeroID} Pow : {HeroPow} *Free")
    
    print("=============================================")
    charID = input("Eqiup Hero into Appl Farm (* to Exit): ")
    if charID != "*":
        txRaw = appl_farm.functions.farm(int(charID)).build_transaction({"from": address})
        hashTx = sendTransaction(txRaw, address, privatekey)
        print("Eqiup Hero Success")


def unEquipHero(address, privatekey):
    amountOfHero = appl_farm.functions.characterOwnerBalanceOf(address).call()
    print(f"Hero in camp : {amountOfHero}")
    for index in range(amountOfHero):
        HeroID = appl_farm.functions.characterOfOwnerByIndex(address,int(index)).call()
        PendingReward = appl_farm.functions.calculateRewards(address,HeroID).call()
        print(f"HERO ID: {HeroID} Pending : {PendingReward*(10**-18)} ")
    print("=============================================")
    charID = input("Enter unEqiup Hero ID (* to Exit): ")
    if charID != "*":
        txRaw = appl_farm.functions.unFarm(int(charID)).build_transaction({"from": address})
        hashTx = sendTransaction(txRaw, address, privatekey)
        print("unEqiup Hero Success")


def claimAll(address, privatekey):
    txRaw = appl_farm.functions.claimRewardAll().build_transaction({"from": address})
    hashTx = sendTransaction(txRaw, address, privatekey)
    print("Claim All Success")


def farmDetail(address):
    print("\tFarm Details")
    print("=============================================")
    amountOfHero = appl_farm.functions.characterOwnerBalanceOf(address).call()
    for index in range(amountOfHero):
        HeroID = appl_farm.functions.characterOfOwnerByIndex(address, index).call()
        PendingReward = appl_farm.functions.calculateRewards(address, HeroID).call()
        print(f"HERO ID: {HeroID} Pending : {PendingReward*(10**-18)} ")


def worker():
    private_key = getpass.getpass(prompt="Enter PrivateKey (Don't Show PVK): ")
    address = get_address_from_private_key(private_key)
    while True:
        print(f"address ; {address}")
        print("=========== DAOBUDDY WELCOME ===============")
        print("Select Functions")
        print("\t1. Equip HERO NFT into Apple Farm")
        print("\t2. UnEquip HERO NFT into Apple Farm")
        print("\t3. Claim All")
        print("\t4. Farm Details")
        print("\t5. Exit")
        select = input("\t Select : ")
        print("============================================")
        if select == "1":
            eqiupHero(address, private_key)
        elif select == "2":
            unEquipHero(address, private_key)
        elif select == "3":
            claimAll(address, private_key)
        elif select == "4":
            farmDetail(address)
        elif select == "5":
            print("Exiting program...")
            break
        else:
            print("Invalid selection")

worker()
