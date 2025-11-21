from web3 import Web3
from solcx import compile_standard, install_solc
import json
import os
from pathlib import Path

def compile_contract():
    """Compile the Solidity contract"""
    print("📦 Compiling contract...")
    
    # Install specific Solidity version
    install_solc("0.8.0")
    
    # Read the contract file
    with open("Contract.sol", "r") as file:
        contract_source_code = file.read()
    
    # Compile the contract
    compiled_sol = compile_standard(
        {
            "language": "Solidity",
            "sources": {"Contract.sol": {"content": contract_source_code}},
            "settings": {
                "outputSelection": {
                    "*": {
                        "*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]
                    }
                }
            },
        },
        solc_version="0.8.0",
    )
    
    # Save compiled contract
    with open("compiled_contract.json", "w") as file:
        json.dump(compiled_sol, file, indent=4)
    
    print("✅ Contract compiled successfully!")
    return compiled_sol

def deploy_contract(w3, account, private_key, compiled_sol):
    """Deploy the contract to the blockchain"""
    print("\n🚀 Deploying contract...")
    
    # Get contract data
    contract_interface = compiled_sol["contracts"]["Contract.sol"]["GreetingContract"]
    bytecode = contract_interface["evm"]["bytecode"]["object"]
    abi = contract_interface["abi"]
    
    # Save ABI for later use
    with open("contract_abi.json", "w") as file:
        json.dump(abi, file, indent=4)
    
    # Create contract instance
    GreetingContract = w3.eth.contract(abi=abi, bytecode=bytecode)
    
    # Get nonce
    nonce = w3.eth.get_transaction_count(account)
    
    # Build transaction
    initial_greeting = "Hello, Blockchain World!"
    transaction = GreetingContract.constructor(initial_greeting).build_transaction({
        "chainId": 1337,  # Ganache default chain ID
        "from": account,
        "nonce": nonce,
        "gas": 2000000,
        "gasPrice": w3.eth.gas_price,
    })
    
    # Sign transaction
    signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
    
    # Send transaction
    print("📤 Sending transaction...")
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    
    # Wait for transaction receipt
    print("⏳ Waiting for transaction receipt...")
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    
    print(f"✅ Contract deployed successfully!")
    print(f"📍 Contract Address: {tx_receipt.contractAddress}")
    print(f"⛽ Gas Used: {tx_receipt.gasUsed}")
    print(f"📝 Transaction Hash: {tx_hash.hex()}")
    
    # Save deployment info
    deployment_info = {
        "contract_address": tx_receipt.contractAddress,
        "transaction_hash": tx_hash.hex(),
        "deployer_address": account,
        "initial_greeting": initial_greeting,
        "gas_used": tx_receipt.gasUsed
    }
    
    with open("deployment_info.json", "w") as file:
        json.dump(deployment_info, file, indent=4)
    
    return tx_receipt.contractAddress, abi

def main():
    """Main deployment function"""
    print("=" * 60)
    print("🎯 GREETING CONTRACT DEPLOYMENT")
    print("=" * 60)
    
    # Connect to Ganache
    print("\n🔗 Connecting to Ganache...")
    ganache_url = "http://127.0.0.1:7545"
    w3 = Web3(Web3.HTTPProvider(ganache_url))
    
    if not w3.is_connected():
        print("❌ Failed to connect to Ganache!")
        print("💡 Make sure Ganache is running on http://127.0.0.1:7545")
        return
    
    print("✅ Connected to Ganache!")
    print(f"📊 Chain ID: {w3.eth.chain_id}")
    print(f"⛓️  Block Number: {w3.eth.block_number}")
    
    # Get account from Ganache
    # Replace with your Ganache account and private key
    account = w3.eth.accounts[0]
    
    # NOTE: In production, NEVER hardcode private keys!
    # Get private key from Ganache for the first account
    private_key = "0x691101e28684e29cb3846276021e2d45feab0f4031f98c0c72e89f48d637a6fa" # Replace with your Ganache private key
    
    print(f"\n👤 Deployer Account: {account}")
    print(f"💰 Balance: {w3.from_wei(w3.eth.get_balance(account), 'ether')} ETH")
    
    try:
        # Compile contract
        compiled_sol = compile_contract()
        
        # Deploy contract
        contract_address, abi = deploy_contract(w3, account, private_key, compiled_sol)
        
        print("\n" + "=" * 60)
        print("✨ DEPLOYMENT COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        print(f"\n📋 Next steps:")
        print(f"   1. Use contract address: {contract_address}")
        print(f"   2. Run 'python interact.py' to interact with the contract")
        print(f"   3. Run 'python test_contract.py' to run tests")
        
    except Exception as e:
        print(f"\n❌ Error during deployment: {str(e)}")
        raise

if __name__ == "__main__":
    main()