        let web3;
        let contract;
        let account;

        // Contract Configuration - UPDATE THESE!
        const CONTRACT_ADDRESS = '0x893490A3E30a31D927B745Df6131Ff29CD99a835'; // Replace with your deployed contract address
        const CONTRACT_ABI = [
    {
        "inputs": [
            {
                "internalType": "string",
                "name": "_initialGreeting",
                "type": "string"
            }
        ],
        "stateMutability": "nonpayable",
        "type": "constructor"
    },
    {
        "anonymous": false,
        "inputs": [
            {
                "indexed": false,
                "internalType": "string",
                "name": "greeting",
                "type": "string"
            },
            {
                "indexed": true,
                "internalType": "address",
                "name": "setBy",
                "type": "address"
            },
            {
                "indexed": false,
                "internalType": "uint256",
                "name": "timestamp",
                "type": "uint256"
            }
        ],
        "name": "GreetingSet",
        "type": "event"
    },
    {
        "anonymous": false,
        "inputs": [
            {
                "indexed": false,
                "internalType": "string",
                "name": "oldGreeting",
                "type": "string"
            },
            {
                "indexed": false,
                "internalType": "string",
                "name": "newGreeting",
                "type": "string"
            },
            {
                "indexed": true,
                "internalType": "address",
                "name": "updatedBy",
                "type": "address"
            },
            {
                "indexed": false,
                "internalType": "uint256",
                "name": "timestamp",
                "type": "uint256"
            }
        ],
        "name": "GreetingUpdated",
        "type": "event"
    },
    {
        "inputs": [],
        "name": "getAllHistory",
        "outputs": [
            {
                "components": [
                    {
                        "internalType": "string",
                        "name": "message",
                        "type": "string"
                    },
                    {
                        "internalType": "address",
                        "name": "updatedBy",
                        "type": "address"
                    },
                    {
                        "internalType": "uint256",
                        "name": "timestamp",
                        "type": "uint256"
                    }
                ],
                "internalType": "struct GreetingContract.GreetingHistory[]",
                "name": "",
                "type": "tuple[]"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "getContractInfo",
        "outputs": [
            {
                "internalType": "string",
                "name": "currentGreeting",
                "type": "string"
            },
            {
                "internalType": "address",
                "name": "contractOwner",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "totalGreetings",
                "type": "uint256"
            },
            {
                "internalType": "uint256",
                "name": "historyLength",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "getGreeting",
        "outputs": [
            {
                "internalType": "string",
                "name": "",
                "type": "string"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "index",
                "type": "uint256"
            }
        ],
        "name": "getGreetingFromHistory",
        "outputs": [
            {
                "internalType": "string",
                "name": "message",
                "type": "string"
            },
            {
                "internalType": "address",
                "name": "updatedBy",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "timestamp",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "getHistoryCount",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "greetingCount",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "name": "greetingHistories",
        "outputs": [
            {
                "internalType": "string",
                "name": "message",
                "type": "string"
            },
            {
                "internalType": "address",
                "name": "updatedBy",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "timestamp",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "owner",
        "outputs": [
            {
                "internalType": "address",
                "name": "",
                "type": "address"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "string",
                "name": "_newGreeting",
                "type": "string"
            }
        ],
        "name": "setGreeting",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    }
]; // Replace with your contract ABI

        // Character counter
        document.getElementById('newGreeting')?.addEventListener('input', function() {
            document.getElementById('charCount').textContent = this.value.length;
        });

        async function connectWallet() {
            try {
                const connectBtn = document.getElementById('connectBtn');
                connectBtn.disabled = true;
                connectBtn.textContent = 'Connecting...';

                // Connect to Ganache
                web3 = new Web3('http://127.0.0.1:7545');
                
                // Get accounts
                const accounts = await web3.eth.getAccounts();
                if (accounts.length === 0) {
                    throw new Error('No accounts found in Ganache');
                }
                account = accounts[0];

                // Initialize contract
                contract = new web3.eth.Contract(CONTRACT_ABI, CONTRACT_ADDRESS);

                // Update UI
                document.getElementById('statusDot').classList.add('connected');
                document.getElementById('statusText').textContent = `Connected: ${account.substring(0, 6)}...${account.substring(38)}`;
                document.getElementById('notConnected').style.display = 'none';
                document.getElementById('mainContent').style.display = 'block';
                connectBtn.textContent = 'Connected ✓';
                connectBtn.style.background = '#10b981';

                // Load initial data
                await loadGreeting();
                await loadContractInfo();

                showNotification('Successfully connected to Ganache!', 'success');
            } catch (error) {
                console.error('Connection error:', error);
                showNotification('Failed to connect: ' + error.message, 'error');
                document.getElementById('connectBtn').disabled = false;
                document.getElementById('connectBtn').textContent = 'Connect to Ganache';
            }
        }

        async function loadGreeting() {
            try {
                const greeting = await contract.methods.getGreeting().call();
                document.getElementById('currentGreeting').textContent = `"${greeting}"`;
            } catch (error) {
                console.error('Error loading greeting:', error);
                showNotification('Error loading greeting', 'error');
            }
        }

        async function loadContractInfo() {
            try {
                const info = await contract.methods.getContractInfo().call();
                document.getElementById('greetingCount').textContent = info[2];
                document.getElementById('historyCount').textContent = info[3];
                document.getElementById('contractOwner').textContent = info[1];
            } catch (error) {
                console.error('Error loading contract info:', error);
            }
        }

        async function setGreeting() {
            const newGreeting = document.getElementById('newGreeting').value.trim();
            const resultDiv = document.getElementById('setResult');
            
            if (!newGreeting) {
                resultDiv.innerHTML = '<div class="result-box error">❌ Greeting cannot be empty!</div>';
                return;
            }

            if (newGreeting.length > 200) {
                resultDiv.innerHTML = '<div class="result-box error">❌ Greeting too long (max 200 characters)!</div>';
                return;
            }

            try {
                resultDiv.innerHTML = '<div class="result-box"><div class="spinner"></div>Sending transaction...</div>';

                const result = await contract.methods.setGreeting(newGreeting).send({
                    from: account,
                    gas: 200000
                });

                resultDiv.innerHTML = `
                    <div class="result-box success">
                        <strong>✅ Greeting Updated Successfully!</strong><br>
                        <small>Transaction Hash: ${result.transactionHash.substring(0, 10)}...${result.transactionHash.substring(56)}</small>
                    </div>
                `;

                // Reload data
                await loadGreeting();
                await loadContractInfo();
                
                // Clear input
                document.getElementById('newGreeting').value = '';
                document.getElementById('charCount').textContent = '0';

                showNotification('Greeting updated successfully!', 'success');
            } catch (error) {
                console.error('Error setting greeting:', error);
                resultDiv.innerHTML = `<div class="result-box error">❌ Error: ${error.message}</div>`;
                showNotification('Transaction failed', 'error');
            }
        }

        async function loadHistory() {
            const historyDiv = document.getElementById('historyList');
            
            try {
                historyDiv.innerHTML = '<div class="loading"><div class="spinner"></div>Loading history...</div>';

                const count = await contract.methods.getHistoryCount().call();
                
                if (count == 0) {
                    historyDiv.innerHTML = '<div class="loading">No history available</div>';
                    return;
                }

                let historyHTML = '';
                for (let i = count - 1; i >= 0; i--) {
                    const history = await contract.methods.getGreetingFromHistory(i).call();
                    const date = new Date(history[2] * 1000);
                    
                    historyHTML += `
                        <div class="history-item">
                            <strong>#${i}: "${history[0]}"</strong>
                            <div class="address">By: ${history[1]}</div>
                            <div class="timestamp">⏰ ${date.toLocaleString()}</div>
                        </div>
                    `;
                }

                historyDiv.innerHTML = historyHTML;
            } catch (error) {
                console.error('Error loading history:', error);
                historyDiv.innerHTML = `<div class="result-box error">❌ Error loading history</div>`;
            }
        }

        async function getHistoryByIndex() {
            const index = document.getElementById('historyIndex').value;
            const resultDiv = document.getElementById('searchResult');
            
            if (index === '') {
                resultDiv.innerHTML = '<div class="result-box error">❌ Please enter an index number</div>';
                return;
            }

            try {
                resultDiv.innerHTML = '<div class="result-box"><div class="spinner"></div>Searching...</div>';

                const history = await contract.methods.getGreetingFromHistory(index).call();
                const date = new Date(history[2] * 1000);

                resultDiv.innerHTML = `
                    <div class="result-box success">
                        <strong>✅ History Entry #${index}</strong><br><br>
                        <strong>Message:</strong> "${history[0]}"<br>
                        <strong>Updated By:</strong> ${history[1]}<br>
                        <strong>Timestamp:</strong> ${date.toLocaleString()}
                    </div>
                `;
            } catch (error) {
                console.error('Error:', error);
                resultDiv.innerHTML = `<div class="result-box error">❌ Index out of bounds or error occurred</div>`;
            }
        }

        function showNotification(message, type) {
            // Simple notification (you can enhance this)
            console.log(`${type.toUpperCase()}: ${message}`);
        }

        // Auto-connect on page load (optional)
        window.addEventListener('load', () => {
            // Uncomment to auto-connect
            // setTimeout(connectWallet, 500);
        });