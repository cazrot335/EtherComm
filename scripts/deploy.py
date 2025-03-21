import os
from brownie import accounts, config, network, DiscordServer
from dotenv import load_dotenv
from eth_account import Account

load_dotenv()

def main():
    # Load environment variables from .env
    load_dotenv()

    # Load private key securely from .env
    private_key = os.getenv("PRIVATE_KEY")

    # Validate private key
    try:
        account = Account.from_key(private_key)
        print(f"Valid private key. Address: {account.address}")
    except Exception as e:
        print(f"Invalid private key: {e}")
        return

    # Connect to Sepolia network
    print(f"\n📡 Active network: {network.show_active()}")

    # Add account from private key
    deployer_account = accounts.add(private_key)
    print(f"🔑 Deployer address: {deployer_account.address}")

    # Deploy the smart contract
    print("🚀 Deploying DiscordServer contract to Sepolia...")
    contract = DiscordServer.deploy({"from": deployer_account})
    print(f"✅ Contract deployed at: {contract.address}")
    print(f"Loaded PRIVATE_KEY: '{private_key}'")

    # Verify contract on Etherscan (optional if Etherscan API key is set in config)
    if config.get("verify", False):
        print("🔍 Verifying contract on Etherscan...")
        DiscordServer.publish_source(contract)

    print("\n🎉 Deployment complete!")
