import requests

def get_transactions(filter_address,filter_token):
    # Define the API endpoint
    api_url = f"https://exp-l1-ng.jibchain.net/api/v2/addresses/{filter_address}/token-transfers?type=ERC-20&filter=to%20%7C%20from&token={filter_token}"
    
    # Make a request to the API
    response = requests.get(api_url)
    
    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        items = data.get("items", [])
        
        # Iterate over each item in the response
        for item in items:
            tx_hash = item.get("tx_hash")
            
            # Call the token-transfers API for the specific transaction hash
            transaction_url = f"https://exp-l1-ng.jibchain.net/api/v2/transactions/{tx_hash}/token-transfers?type=ERC-20%2CERC-721%2CERC-1155"
            transaction_response = requests.get(transaction_url)
            
            # Check if the transaction request was successful
            if transaction_response.status_code == 200:
                transaction_data = transaction_response.json()
                process_token_transfers(transaction_data,tx_hash)
            else:
                print("Error fetching transaction data:", transaction_response.status_code)
    else:
        print("Error fetching data from API:", response.status_code)

def process_token_transfers(data,tx_hash):
    for item in data["items"]:
        if item["type"] == "token_transfer":
            if item["token"]["type"] == "ERC-721":
                itemName = item['token']['name']
                itemID = item['total'].get('token_id', 'Unknown')
                print(f"\tคุณซื้อ {itemName} #{itemID}",end="")
                for item in data["items"]:
                    if item["token"]["type"] == "ERC-20":
                        value = int(item["total"]["value"])
                        decimals = int(item["token"]["decimals"])
                        value /= 10 ** decimals  # Convert value to the actual amount
                        print(f" ในจำนวน {value} {item['token']['symbol']} TxHash {tx_hash}")

# Define the filter address
filter_address = "0x98e5CFBC115b01017Ed19101357Ab0a7664f38f1"
filter_token = '0x24599b658b57f91E7643f4F154B16bcd2884f9ac' #JUSDT
# Call the function to get transactions
get_transactions(filter_address,filter_token)
