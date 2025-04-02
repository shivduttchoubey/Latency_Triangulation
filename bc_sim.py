import hashlib
import time
import json
import tkinter as tk
from tkinter import scrolledtext

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

def create_genesis_block():
    return Block(0, "0", ["Genesis Block"])

def create_new_block(previous_block, transactions):
    new_block = Block(previous_block.index + 1, previous_block.hash, transactions)
    new_block.mine_block(difficulty=4)
    return new_block

# Tkinter GUI
def add_block():
    transactions = transaction_entry.get("1.0", tk.END).strip().split("\n")
    if transactions:
        new_block = create_new_block(blockchain[-1], transactions)
        blockchain.append(new_block)
        update_display()

def update_display():
    blockchain_display.delete("1.0", tk.END)
    for block in blockchain:
        blockchain_display.insert(tk.END, json.dumps(vars(block), indent=4) + "\n\n")

# Initialize Blockchain
blockchain = [create_genesis_block()]

# Tkinter Setup
root = tk.Tk()
root.title("Blockchain Simulator")
root.geometry("600x500")

tk.Label(root, text="Enter Transactions (One per Line):").pack()
transaction_entry = scrolledtext.ScrolledText(root, height=5, width=70)
transaction_entry.pack()

tk.Button(root, text="Add Block", command=add_block).pack()

tk.Label(root, text="Blockchain Representation:").pack()
blockchain_display = scrolledtext.ScrolledText(root, height=15, width=70)
blockchain_display.pack()
update_display()

root.mainloop()
