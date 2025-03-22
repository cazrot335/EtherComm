from eth_account import Account
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get the private key
private_key = os.getenv("PRIVATE_KEY")

# Debugging: Print the private key
print(f"Loaded PRIVATE_KEY: '{private_key}'")
print(f"Length of PRIVATE_KEY: {len(private_key)}")

# Validate the private key
try:
    account = Account.from_key(private_key)
    print(f"Valid private key. Address: {account.address}")
except Exception as e:
    print(f"Invalid private key: {e}")