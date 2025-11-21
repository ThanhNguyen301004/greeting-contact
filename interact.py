from web3 import Web3
import json
from datetime import datetime

def load_contract(w3):
    """Load the deployed contract"""
    # Load deployment info
    with open("deployment_info.json", "r") as file:
        deployment_info = json.load(file)
    
    # Load ABI
    with open("contract_abi.json", "r") as file:
        abi = json.load(file)
    
    contract_address = deployment_info["contract_address"]
    contract = w3.eth.contract(address=contract_address, abi=abi)
    
    return contract, contract_address

def get_greeting(contract):
    """Get current greeting"""
    try:
        greeting = contract.functions.getGreeting().call()
        print(f"\n💬 Current Greeting: '{greeting}'")
        return greeting
    except Exception as e:
        print(f"❌ Error getting greeting: {str(e)}")
        return None

def set_greeting(contract, w3, account, private_key, new_greeting):
    """Set a new greeting"""
    try:
        print(f"\n📝 Setting new greeting: '{new_greeting}'")
        
        # Build transaction
        nonce = w3.eth.get_transaction_count(account)
        transaction = contract.functions.setGreeting(new_greeting).build_transaction({
            "chainId": 1337,
            "from": account,
            "nonce": nonce,
            "gas": 200000,
            "gasPrice": w3.eth.gas_price,
        })
        
        # Sign and send transaction
        signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
        tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        
        print("⏳ Waiting for transaction confirmation...")
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        
        if tx_receipt.status == 1:
            print("✅ Greeting updated successfully!")
            print(f"📝 Transaction Hash: {tx_hash.hex()}")
            print(f"⛽ Gas Used: {tx_receipt.gasUsed}")
            
            # Get event logs
            logs = contract.events.GreetingUpdated().process_receipt(tx_receipt)
            if logs:
                event = logs[0]['args']
                print(f"\n📢 Event Emitted:")
                print(f"   Old Greeting: '{event['oldGreeting']}'")
                print(f"   New Greeting: '{event['newGreeting']}'")
                print(f"   Updated By: {event['updatedBy']}")
                print(f"   Timestamp: {datetime.fromtimestamp(event['timestamp'])}")
        else:
            print("❌ Transaction failed!")
            
        return tx_receipt
        
    except Exception as e:
        print(f"❌ Error setting greeting: {str(e)}")
        return None

def get_contract_info(contract):
    """Get contract information"""
    try:
        info = contract.functions.getContractInfo().call()
        print(f"\n📊 Contract Information:")
        print(f"   Current Greeting: '{info[0]}'")
        print(f"   Owner: {info[1]}")
        print(f"   Total Greetings: {info[2]}")
        print(f"   History Length: {info[3]}")
        return info
    except Exception as e:
        print(f"❌ Error getting contract info: {str(e)}")
        return None

def get_greeting_history(contract):
    """Get greeting history"""
    try:
        history_count = contract.functions.getHistoryCount().call()
        print(f"\n📜 Greeting History ({history_count} entries):")
        print("=" * 80)
        
        for i in range(history_count):
            history = contract.functions.getGreetingFromHistory(i).call()
            timestamp = datetime.fromtimestamp(history[2])
            print(f"\n{i + 1}. Message: '{history[0]}'")
            print(f"   Updated By: {history[1]}")
            print(f"   Timestamp: {timestamp}")
        
        print("=" * 80)
        return history_count
        
    except Exception as e:
        print(f"❌ Error getting history: {str(e)}")
        return None

def interactive_menu(contract, w3, account, private_key):
    """Interactive menu for contract interaction"""
    while True:
        print("\n" + "=" * 60)
        print("🎯 GREETING CONTRACT INTERACTION MENU")
        print("=" * 60)
        print("1. Get Current Greeting")
        print("2. Set New Greeting")
        print("3. View Contract Info")
        print("4. View Greeting History")
        print("5. Exit")
        print("=" * 60)
        
        choice = input("\n👉 Enter your choice (1-5): ").strip()
        
        if choice == "1":
            get_greeting(contract)
            
        elif choice == "2":
            new_greeting = input("\n💬 Enter new greeting: ").strip()
            if new_greeting:
                set_greeting(contract, w3, account, private_key, new_greeting)
            else:
                print("❌ Greeting cannot be empty!")
                
        elif choice == "3":
            get_contract_info(contract)
            
        elif choice == "4":
            get_greeting_history(contract)
            
        elif choice == "5":
            print("\n👋 Goodbye!")
            break
            
        else:
            print("❌ Invalid choice! Please enter 1-5.")

def main():
    """Main interaction function"""
    print("=" * 60)
    print("🎯 GREETING CONTRACT INTERACTION")
    print("=" * 60)
    
    # Connect to Ganache
    print("\n🔗 Connecting to Ganache...")
    ganache_url = "http://127.0.0.1:7545"
    w3 = Web3(Web3.HTTPProvider(ganache_url))
    
    if not w3.is_connected():
        print("❌ Failed to connect to Ganache!")
        return
    
    print("✅ Connected to Ganache!")
    
    # Load contract
    try:
        contract, contract_address = load_contract(w3)
        print(f"📍 Contract loaded at: {contract_address}")
        
        # Get account
        account = w3.eth.accounts[0]
        private_key = "0x691101e28684e29cb3846276021e2d45feab0f4031f98c0c72e89f48d637a6fa"  # Replace with your Ganache private key
        
        print(f"👤 Using Account: {account}")
        
        # Start interactive menu
        interactive_menu(contract, w3, account, private_key)
        
    except FileNotFoundError:
        print("❌ Contract not deployed! Please run 'python deploy.py' first.")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    main()