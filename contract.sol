// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract GreetingContract {
    // State variables
    string private greeting;
    address public owner;
    uint256 public greetingCount;
    
    // Struct to store greeting history
    struct GreetingHistory {
        string message;
        address updatedBy;
        uint256 timestamp;
    }
    
    // Array to store all greeting history
    GreetingHistory[] public greetingHistories;
    
    // Events
    event GreetingUpdated(
        string oldGreeting,
        string newGreeting,
        address indexed updatedBy,
        uint256 timestamp
    );
    
    event GreetingSet(
        string greeting,
        address indexed setBy,
        uint256 timestamp
    );
    
    // Constructor
    constructor(string memory _initialGreeting) {
        greeting = _initialGreeting;
        owner = msg.sender;
        greetingCount = 1;
        
        // Add initial greeting to history
        greetingHistories.push(GreetingHistory({
            message: _initialGreeting,
            updatedBy: msg.sender,
            timestamp: block.timestamp
        }));
        
        emit GreetingSet(_initialGreeting, msg.sender, block.timestamp);
    }
    
    // Function to get current greeting
    function getGreeting() public view returns (string memory) {
        return greeting;
    }
    
    // Function to update greeting
    function setGreeting(string memory _newGreeting) public {
        require(bytes(_newGreeting).length > 0, "Greeting cannot be empty");
        require(bytes(_newGreeting).length <= 200, "Greeting too long (max 200 characters)");
        
        string memory oldGreeting = greeting;
        greeting = _newGreeting;
        greetingCount++;
        
        // Add to history
        greetingHistories.push(GreetingHistory({
            message: _newGreeting,
            updatedBy: msg.sender,
            timestamp: block.timestamp
        }));
        
        emit GreetingUpdated(oldGreeting, _newGreeting, msg.sender, block.timestamp);
    }
    
    // Function to get greeting history count
    function getHistoryCount() public view returns (uint256) {
        return greetingHistories.length;
    }
    
    // Function to get specific greeting from history
    function getGreetingFromHistory(uint256 index) public view returns (
        string memory message,
        address updatedBy,
        uint256 timestamp
    ) {
        require(index < greetingHistories.length, "Index out of bounds");
        GreetingHistory memory history = greetingHistories[index];
        return (history.message, history.updatedBy, history.timestamp);
    }
    
    // Function to get all greeting history
    function getAllHistory() public view returns (GreetingHistory[] memory) {
        return greetingHistories;
    }
    
    // Function to get contract info
    function getContractInfo() public view returns (
        string memory currentGreeting,
        address contractOwner,
        uint256 totalGreetings,
        uint256 historyLength
    ) {
        return (greeting, owner, greetingCount, greetingHistories.length);
    }
}