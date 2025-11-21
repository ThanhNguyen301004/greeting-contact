import unittest
from web3 import Web3
import json
import time

class TestGreetingContract(unittest.TestCase):
    """Test cases for Greeting Contract"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test environment"""
        print("\n" + "=" * 60)
        print("🧪 GREETING CONTRACT TEST SUITE")
        print("=" * 60)
        
        # Connect to Ganache
        cls.w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))
        
        if not cls.w3.is_connected():
            raise Exception("Failed to connect to Ganache!")
        
        print("✅ Connected to Ganache")
        
        # Load contract
        try:
            with open("deployment_info.json", "r") as file:
                deployment_info = json.load(file)
            
            with open("contract_abi.json", "r") as file:
                abi = json.load(file)
            
            cls.contract_address = deployment_info["contract_address"]
            cls.contract = cls.w3.eth.contract(address=cls.contract_address, abi=abi)
            cls.account = cls.w3.eth.accounts[0]
            cls.private_key = "0x691101e28684e29cb3846276021e2d45feab0f4031f98c0c72e89f48d637a6fa"  # Replace with your Ganache private key
            
            print(f"📍 Testing contract at: {cls.contract_address}")
            print(f"👤 Using account: {cls.account}\n")
            
        except FileNotFoundError:
            raise Exception("Contract not deployed! Run 'python deploy.py' first.")
    
    def test_01_get_initial_greeting(self):
        """Test 1: Get initial greeting"""
        print("🧪 Test 1: Get initial greeting")
        greeting = self.contract.functions.getGreeting().call()
        self.assertIsNotNone(greeting)
        self.assertIsInstance(greeting, str)
        self.assertTrue(len(greeting) > 0)
        print(f"   ✅ Initial greeting: '{greeting}'")
    
    def test_02_set_greeting(self):
        """Test 2: Set new greeting"""
        print("\n🧪 Test 2: Set new greeting")
        new_greeting = "Test Greeting - Hello World!"
        
        nonce = self.w3.eth.get_transaction_count(self.account)
        transaction = self.contract.functions.setGreeting(new_greeting).build_transaction({
            "chainId": 1337,
            "from": self.account,
            "nonce": nonce,
            "gas": 200000,
            "gasPrice": self.w3.eth.gas_price,
        })
        
        signed_txn = self.w3.eth.account.sign_transaction(transaction, private_key=self.private_key)
        tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        
        self.assertEqual(tx_receipt.status, 1)
        
        # Verify greeting was updated
        current_greeting = self.contract.functions.getGreeting().call()
        self.assertEqual(current_greeting, new_greeting)
        print(f"   ✅ Greeting updated to: '{new_greeting}'")
    
    def test_03_event_emission(self):
        """Test 3: Verify event emission"""
        print("\n🧪 Test 3: Verify event emission")
        new_greeting = "Testing Event Emission"
        
        nonce = self.w3.eth.get_transaction_count(self.account)
        transaction = self.contract.functions.setGreeting(new_greeting).build_transaction({
            "chainId": 1337,
            "from": self.account,
            "nonce": nonce,
            "gas": 200000,
            "gasPrice": self.w3.eth.gas_price,
        })
        
        signed_txn = self.w3.eth.account.sign_transaction(transaction, private_key=self.private_key)
        tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        
        # Check event logs
        logs = self.contract.events.GreetingUpdated().process_receipt(tx_receipt)
        self.assertTrue(len(logs) > 0)
        
        event = logs[0]['args']
        self.assertEqual(event['newGreeting'], new_greeting)
        self.assertEqual(event['updatedBy'], self.account)
        print(f"   ✅ Event emitted successfully")
        print(f"      New Greeting: '{event['newGreeting']}'")
        print(f"      Updated By: {event['updatedBy']}")
    
    def test_04_greeting_count(self):
        """Test 4: Verify greeting count increments"""
        print("\n🧪 Test 4: Verify greeting count")
        
        info_before = self.contract.functions.getContractInfo().call()
        count_before = info_before[2]
        
        # Set new greeting
        new_greeting = "Counting Test"
        nonce = self.w3.eth.get_transaction_count(self.account)
        transaction = self.contract.functions.setGreeting(new_greeting).build_transaction({
            "chainId": 1337,
            "from": self.account,
            "nonce": nonce,
            "gas": 200000,
            "gasPrice": self.w3.eth.gas_price,
        })
        
        signed_txn = self.w3.eth.account.sign_transaction(transaction, private_key=self.private_key)
        tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        self.w3.eth.wait_for_transaction_receipt(tx_hash)
        
        info_after = self.contract.functions.getContractInfo().call()
        count_after = info_after[2]
        
        self.assertEqual(count_after, count_before + 1)
        print(f"   ✅ Count increased from {count_before} to {count_after}")
    
    def test_05_greeting_history(self):
        """Test 5: Verify greeting history tracking"""
        print("\n🧪 Test 5: Verify greeting history")
        
        history_count = self.contract.functions.getHistoryCount().call()
        self.assertTrue(history_count > 0)
        
        # Get first history entry
        history = self.contract.functions.getGreetingFromHistory(0).call()
        self.assertIsNotNone(history[0])  # message
        self.assertIsNotNone(history[1])  # updatedBy
        self.assertTrue(history[2] > 0)   # timestamp
        
        print(f"   ✅ History count: {history_count}")
        print(f"      First entry: '{history[0]}'")
    
    def test_06_empty_greeting_validation(self):
        """Test 6: Test empty greeting validation"""
        print("\n🧪 Test 6: Test empty greeting validation")
        
        with self.assertRaises(Exception) as context:
            nonce = self.w3.eth.get_transaction_count(self.account)
            transaction = self.contract.functions.setGreeting("").build_transaction({
                "chainId": 1337,
                "from": self.account,
                "nonce": nonce,
                "gas": 200000,
                "gasPrice": self.w3.eth.gas_price,
            })
            
            signed_txn = self.w3.eth.account.sign_transaction(transaction, private_key=self.private_key)
            tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
            self.w3.eth.wait_for_transaction_receipt(tx_hash)
        
        print(f"   ✅ Empty greeting correctly rejected")
    
    def test_07_long_greeting_validation(self):
        """Test 7: Test long greeting validation"""
        print("\n🧪 Test 7: Test long greeting validation")
        
        long_greeting = "A" * 201  # More than 200 characters
        
        with self.assertRaises(Exception) as context:
            nonce = self.w3.eth.get_transaction_count(self.account)
            transaction = self.contract.functions.setGreeting(long_greeting).build_transaction({
                "chainId": 1337,
                "from": self.account,
                "nonce": nonce,
                "gas": 200000,
                "gasPrice": self.w3.eth.gas_price,
            })
            
            signed_txn = self.w3.eth.account.sign_transaction(transaction, private_key=self.private_key)
            tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
            self.w3.eth.wait_for_transaction_receipt(tx_hash)
        
        print(f"   ✅ Long greeting correctly rejected")
    
    def test_08_owner_verification(self):
        """Test 8: Verify owner is set correctly"""
        print("\n🧪 Test 8: Verify owner")
        
        owner = self.contract.functions.owner().call()
        self.assertEqual(owner, self.w3.eth.accounts[0])
        print(f"   ✅ Owner verified: {owner}")
    
    def test_09_multiple_updates(self):
        """Test 9: Test multiple greeting updates"""
        print("\n🧪 Test 9: Test multiple updates")
        
        greetings = ["Update 1", "Update 2", "Update 3"]
        
        for greeting in greetings:
            nonce = self.w3.eth.get_transaction_count(self.account)
            transaction = self.contract.functions.setGreeting(greeting).build_transaction({
                "chainId": 1337,
                "from": self.account,
                "nonce": nonce,
                "gas": 200000,
                "gasPrice": self.w3.eth.gas_price,
            })
            
            signed_txn = self.w3.eth.account.sign_transaction(transaction, private_key=self.private_key)
            tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
            self.w3.eth.wait_for_transaction_receipt(tx_hash)
            
            current = self.contract.functions.getGreeting().call()
            self.assertEqual(current, greeting)
        
        print(f"   ✅ All {len(greetings)} updates successful")
    
    def test_10_contract_info(self):
        """Test 10: Test getContractInfo function"""
        print("\n🧪 Test 10: Test contract info")
        
        info = self.contract.functions.getContractInfo().call()
        
        self.assertIsNotNone(info[0])  # current greeting
        self.assertIsNotNone(info[1])  # owner
        self.assertTrue(info[2] > 0)    # total greetings
        self.assertTrue(info[3] > 0)    # history length
        
        print(f"   ✅ Contract info retrieved successfully")
        print(f"      Total Greetings: {info[2]}")
        print(f"      History Length: {info[3]}")

def run_tests():
    """Run all tests"""
    # Create test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestGreetingContract)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    print(f"Tests Run: {result.testsRun}")
    print(f"✅ Passed: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"❌ Failed: {len(result.failures)}")
    print(f"⚠️  Errors: {len(result.errors)}")
    print("=" * 60)
    
    return result.wasSuccessful()

if __name__ == "__main__":
    success = run_tests()
    exit(0 if success else 1)