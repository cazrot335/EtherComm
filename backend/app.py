# backend/app.py
from flask import Flask, request, jsonify
from web3 import Web3
import json, os
import ipfs_handler
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

# Connect to Sepolia via Infura
infura_url = f"https://sepolia.infura.io/v3/{os.getenv('WEB3_INFURA_PROJECT_ID')}"
web3 = Web3(Web3.HTTPProvider(infura_url))
private_key = os.getenv('PRIVATE_KEY')
account = web3.eth.account.from_key(private_key)
address = account.address

# Load compiled contract ABI
with open('./build/contracts/DiscordServer.json') as f:
    contract_json = json.load(f)
    abi = contract_json['abi']
    contract_address = Web3.to_checksum_address('0x7048a0EFB59F7b3A7515A6a7Ff6971224f9d07cf')
    contract = web3.eth.contract(address=contract_address, abi=abi)

@app.route('/create_channel', methods=['POST'])
def create_channel():
    data = request.json
    name = data['name']
    tx = contract.functions.createChannel(name).build_transaction({
        'from': address,
        'nonce': web3.eth.get_transaction_count(address),
        'gas': 2000000,
        'gasPrice': web3.to_wei('10', 'gwei')
    })
    signed = web3.eth.account.sign_transaction(tx, private_key)
    tx_hash = web3.eth.send_raw_transaction(signed.rawTransaction)
    return jsonify({'tx_hash': tx_hash.hex()})

@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.json
    channel_id = data['channel_id']
    message = data['message']
    ipfs_hash = ipfs_handler.upload_to_ipfs(message)

    tx = contract.functions.sendMessage(channel_id, ipfs_hash).build_transaction({
        'from': address,
        'nonce': web3.eth.get_transaction_count(address),
        'gas': 2000000,
        'gasPrice': web3.to_wei('10', 'gwei')
    })
    signed = web3.eth.account.sign_transaction(tx, private_key)
    tx_hash = web3.eth.send_raw_transaction(signed.rawTransaction)
    return jsonify({'tx_hash': tx_hash.hex(), 'ipfs_hash': ipfs_hash})

@app.route('/get_messages', methods=['GET'])
def get_messages():
    channel_id = int(request.args.get('channel_id'))
    count = contract.functions.getMessageCount(channel_id).call()
    messages = []
    for i in range(count):
        ipfs_hash = contract.functions.getMessage(channel_id, i).call()
        msg = ipfs_handler.download_from_ipfs(ipfs_hash)
        messages.append(msg)
    return jsonify({'messages': messages})

if __name__ == '__main__':
    app.run(port=5000)
