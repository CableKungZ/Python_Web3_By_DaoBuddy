# คำเตือน โค้ดนี้เป็นการดึงข้อมูลธุรกรรมที่เกิดขึ้น ทุก Account ที่เกิดขึ้นบน CHAIN โดยมีการดึงข้อมูลและเซฟเป็นไฟล์ .csv โปรดระมัดระวังเรื่องพื้นที่เต็ม ขนาดไฟล์ขึ้นอยู่กับปริมาณธุรกรรมที่เกิดขึ้น

import os
from web3 import Web3
import time
import csv
from concurrent.futures import ThreadPoolExecutor, as_completed
from queue import Queue
import threading
import json
import random


# ✅ RPC 4 ตัว (แต่ละ Worker จะใช้ตัวแยกกัน)
RPC_URLS = [
    "https://rpc-l1.jbc.xpool.pw",
    "https://rpc2-l1.jbc.xpool.pw",
    "https://rpc-l1.inan.in.th",
    "https://rpc-l1.jibchain.net"
]

NUM_WORKERS = 4  # เพิ่มจำนวน Worker เพื่อให้สามารถประมวลผลได้เร็วขึ้น
latest_block = 4857320
start_block = 25000
blocks_per_worker = (latest_block - start_block) // NUM_WORKERS
batch_size = 1000
saveLog = 10000
max_retries = 5


progress_lock = threading.Lock()
processed_blocks = 0
total_blocks = latest_block - start_block

wallet_data = {}
wallet_first_block = {}
wallet_transactions = {}
processed_tx_hashes = set()  # ✅ ป้องกันธุรกรรมซ้ำ

# ✅ สร้างโฟลเดอร์ logs ถ้ายังไม่มี
os.makedirs("logs", exist_ok=True)

# ✅ ฟังก์ชันบันทึกธุรกรรมของแต่ละกระเป๋าเป็น CSV
def save_wallet_logs(wallet_address):
    file_path = f"logs/{wallet_address}.csv"
    is_new_file = not os.path.exists(file_path)

    with open(file_path, "a", newline="") as csvfile:
        writer = csv.writer(csvfile)

        if is_new_file:
            writer.writerow(["BlockNumber", "Gas Price", "Gas Used", "Transaction Fee","Tx Hash"])

        for tx in wallet_transactions.get(wallet_address, []):
            writer.writerow(tx)

    wallet_transactions[wallet_address] = []

def switch_rpc(worker_id):
    """ เปลี่ยน RPC URL ใหม่แบบสุ่มเมื่อ RPC เดิมใช้ไม่ได้ """
    new_rpc = random.choice(RPC_URLS)
    print(f"🔄 Worker {worker_id} เปลี่ยน RPC ไปที่ {new_rpc}")
    return Web3(Web3.HTTPProvider(new_rpc, request_kwargs={"timeout": 60}))

def log_progress(worker_id, start_block, current_block):
    """ บันทึกความคืบหน้าลงไฟล์ log """
    log_data = {"worker": worker_id, "start_block": start_block, "current_block": current_block}
    with open(f"worker_{worker_id}.log", "w") as log_file:
        json.dump(log_data, log_file)

def process_log_worker(worker_id, rpc_url, start, end):
    w3 = Web3(Web3.HTTPProvider(rpc_url, request_kwargs={"timeout": 60}))
    print(f"🚀 Worker {worker_id} ใช้ RPC: {rpc_url} | ค้นหา Block {start}-{end}")

    local_wallets = {}

    for block_num in range(start, end, -batch_size):  
        retry_count = 0
        while retry_count < max_retries:
            try:
                logs = w3.eth.get_logs({"fromBlock": block_num - (batch_size-1), "toBlock": block_num})
                break  # สำเร็จ ออกจาก loop retry
            except Exception as e:
                print(f"❌ Worker {worker_id} RPC Error at Block {block_num}: {e}")
                retry_count += 1
                if retry_count < max_retries:
                    w3 = switch_rpc(worker_id)  # เปลี่ยน RPC แล้วลองใหม่
                    time.sleep(3)  # หน่วงเวลาเล็กน้อยก่อน retry
                else:
                    print(f"🚨 Worker {worker_id} ล้มเหลวที่ Block {block_num} หลังจาก retry {max_retries} ครั้ง")
                    return  # หยุด Worker ถ้าทดลองทุก RPC แล้วยังไม่ได้

        print(f"{worker_id} | Processing: {len(logs)} logs from blocks {block_num - (batch_size-1)} to {block_num}")
        start_time = time.time()

        for log in logs:
            try:
                tx_hash = log["transactionHash"].hex()
                if tx_hash in processed_tx_hashes:
                    continue  
                processed_tx_hashes.add(tx_hash)  

                tx = w3.eth.get_transaction(tx_hash)
                receipt = w3.eth.get_transaction_receipt(tx_hash)

                sender = tx["from"].lower()
                gas_used = receipt["gasUsed"]
                gas_price = tx["gasPrice"]
                gas_fee = gas_used * gas_price
                block_number = log["blockNumber"]

                if sender not in wallet_transactions:
                    wallet_transactions[sender] = []
                wallet_transactions[sender].append([
                    block_number, Web3.from_wei(gas_price, "gwei"), gas_used, Web3.from_wei(gas_fee, "ether"), tx_hash
                ])

                if sender not in local_wallets:
                    local_wallets[sender] = {"gas_fee": 0, "first_block": block_number}
                local_wallets[sender]["gas_fee"] += gas_fee
                local_wallets[sender]["first_block"] = min(local_wallets[sender]["first_block"], block_number)

            except Exception:
                pass

        print(f"{worker_id} | Save Log {len(local_wallets)} Wallets Finish Process in {format(time.time()-start_time)} seconds")
        for addr, data in local_wallets.items():
            if addr not in wallet_data:
                wallet_data[addr] = 0
                wallet_first_block[addr] = data["first_block"]
            else:
                wallet_first_block[addr] = min(wallet_first_block[addr], data["first_block"])
            wallet_data[addr] += data["gas_fee"]

        for addr in local_wallets:
            save_wallet_logs(addr)

        log_progress(worker_id, start, block_num)  # 📝 บันทึก log

    print(f"✅ Worker {worker_id} เสร็จสิ้น (Block {end} - {start})")
# ✅ ฟังก์ชันบันทึกยอดรวม Gas Fee
def save_to_csv():
    csv_filename = "wallet_gas_fee.csv"
    with open(csv_filename, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Address", "First Transaction Block", "Spend ETH"])
        for addr, fee in wallet_data.items():
            first_block = wallet_first_block.get(addr, "N/A")
            writer.writerow([addr, first_block, Web3.from_wei(fee, "ether")])
    print(f"📂 ข้อมูลถูกบันทึกลงไฟล์: wallet_gas_fee.csv")

# ✅ ฟังก์ชันหลักเพื่อรอผลลัพธ์จาก Worker
def main():
    start_time = time.time()


    with ThreadPoolExecutor(max_workers=NUM_WORKERS) as executor:
        futures = []
        for i in range(NUM_WORKERS):
            worker_start = latest_block - (i * blocks_per_worker)  # เริ่มจาก latest_block
            worker_end = latest_block - ((i + 1) * blocks_per_worker) + 1  # ไปถึง start_block
            if worker_end < start_block:
                worker_end = start_block  # ไม่ให้ worker ไปเกิน start_block
            rpc_url = RPC_URLS[i]
            futures.append(executor.submit(process_log_worker, i + 1, rpc_url, worker_start, worker_end))

        for future in as_completed(futures):
            future.result()

    # ✅ แสดงผลลัพธ์
    execution_time = time.time() - start_time
    print(f"latest_block: {latest_block}")
    print(f"\n✅ พบ {len(wallet_data)} กระเป๋าที่ทำธุรกรรม")
    print(f"⏳ เวลาที่ใช้: {execution_time:.2f} วินาที")

if __name__ == "__main__":
    main()
