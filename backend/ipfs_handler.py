# backend/ipfs_handler.py
import requests

API_URL = "http://127.0.0.1:5001/api/v0"

def upload_to_ipfs(content):
    files = {'file': content}
    response = requests.post(f"{API_URL}/add", files=files)
    response.raise_for_status()
    return response.json()['Hash']  # Returns the IPFS hash

def download_from_ipfs(ipfs_hash):
    response = requests.get(f"http://127.0.0.1:8080/ipfs/{ipfs_hash}")
    response.raise_for_status()
    return response.text  # Returns the content
