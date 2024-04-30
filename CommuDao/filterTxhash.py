from web3 import Web3

def get_token_transfers(from_address, to_address, token_address):
    web3 = Web3(Web3.HTTPProvider('http://49.13.16.167:8545'))  

    event_filter = {
        'fromBlock': 0,  # Start Block number
        'toBlock': 'latest',
        'address': web3.to_checksum_address(token_address),
        'topics': [
            web3.keccak(text='Transfer(address,address,uint256)').hex(),
            '0x000000000000000000000000' + from_address[2:].lower(),
            '0x000000000000000000000000' + to_address[2:].lower()
        ]
    }
    return web3.eth.get_logs(event_filter)

fieldInfo = [
    {"name": "Eastern Front", "nftAddress": "0x526A70be985EB234c3f2c4933aCB59F6EB595Ed7", "fieldAddress": "0x495d66c9Fd7c63807114d06802A48BdAA60a0426"},
    {"name": "Mech Harvest Zone", "nftAddress": "0x2036186F6d5287FcB05C56C38374AC5236d8A61d", "fieldAddress": "0x0E2610730A3c42fd721B289BEe092D9AD1C76890"},
]


from_address = "0x98e5CFBC115b01017Ed19101357Ab0a7664f38f1"
transfers = []

for info in fieldInfo:
    transfer = get_token_transfers(from_address, info["fieldAddress"], info["nftAddress"])
    if transfer:
        transfers.extend(transfer)
        print(info["name"])
        for tx in transfer:
            print("  Transaction Hash:", tx['transactionHash'].hex()) 

if not transfers:
    print("No ERC721 transfers found matching the criteria.")
