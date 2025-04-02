import hashlib
import time
import json

class Block:
    def __init__(self, index, previous_hash, transactions, timestamp=None):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp or time.time()
        self.transactions = transactions  # List of transactions
        self.nonce = 0  # Used for mining
        self.hash = self.calculate_hash()
    
    def calculate_hash(self):
        block_content = json.dumps({
            "index": self.index,
            "previous_hash": self.previous_hash,
            "timestamp": self.timestamp,
            "transactions": self.transactions,
            "nonce": self.nonce
        }, sort_keys=True)
        return hashlib.sha256(block_content.encode()).hexdigest()
    
    def mine_block(self, difficulty):
        while self.hash[:difficulty] != "0" * difficulty:
            self.nonce += 1
            self.hash = self.calculate_hash()
        print(f"Block Mined! Hash: {self.hash}")

# Example usage
def create_genesis_block():
    return Block(0, "0", ["Genesis Block"])

def create_new_block(previous_block, transactions):
    return Block(previous_block.index + 1, previous_block.hash, transactions)

# Simulating Blockchain
blockchain = [create_genesis_block()]
new_block = create_new_block(blockchain[-1], ["Alice pays Bob 5 BTC", "Charlie pays Dave 3 BTC"])
new_block.mine_block(difficulty=4)  # Adjust difficulty as needed
blockchain.append(new_block)

# Display the blocks
for block in blockchain:
    print(vars(block))
