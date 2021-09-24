#Blockchain Assignment 1
#Abhilash Gahankari - 2020H1030113H
#Aashita Dutta - 2020H1030130H
#Satish Phale - 2020H1030155H

from hashlib import new, sha256
import json, time
from flask import Flask, jsonify, request

#creating a single block having index, timestamp, 
#list of transactions, hash of previous block, nonce
#compute_hash ensures immutable property of blockchain 
#by creating SHA-256 hash of block
class Block:
    def __init__(self, index, timestamp, transactions, previous_hash, nonce = 0):
        self.index = index
        self.timestamp = timestamp
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce  = nonce
    
    def compute_hash(self):
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return sha256(block_string.encode()).hexdigest()

#creating blockchain
class BlockChain:
    def __init__(self):
        self.unconfirmed_transactions = []
        self.chain = []
        self.create_first_block()

    #creating empty first block and inititing the chain
    def create_first_block(self):
        first_block = Block(0, [], time.time(), "0")
        first_block.hash = first_block.compute_hash()
        self.chain.append(first_block)
        
    # This function is created
    # to display the previous block
    @property
    def last_block(self):
        return self.chain[-1]

    difficulty = 2

    #solves hard puzzles requiring high computation to mine block 
    #while we not get hash starting with 0, hash is computed with nonce value incremented each time
    def proof_of_work(self, block):
        block.nonce = 0
        computed_hash = block.compute_hash()
        while not computed_hash.startswith('0' * BlockChain.difficulty):
            block.nonce += 1
            computed_hash = block.compute_hash()
        return computed_hash
    
    #add new block to chain by linking hash to previous block hash 
    def add_block(self, block, proof):
        previous_hash = self.last_block.hash
        if(previous_hash != block.previous_hash):
            return False
        if not self.is_valid_proof(block, proof):
            return False
        block.hash = proof
        self.chain.append(block)
        return True        

    #validate proof comparing calculated and actual hash
    def is_valid_proof(self, block, block_hash):
        return (block_hash == block.compute_hash() and block_hash.startswith('0' * BlockChain.difficulty))
    
    def add_new_transaction(self, transaction):
        self.unconfirmed_transactions.append(transaction)

    #mine to validate new block and add from unconfirmed transactions to confirmed transactions pool
    #implements proof of work consensus algorithm
    def mine(self):
        if not self.unconfirmed_transactions:
            return False
        
        last_block = self.last_block
        new_block = Block(index = last_block.index + 1,
                            timestamp= time.time(),
                            transactions= self.unconfirmed_transactions,
                            previous_hash= last_block.hash)
        proof = self.proof_of_work(new_block)
        self.add_block(new_block, proof)
        self.unconfirmed_transactions = []
        return new_block.index
        
#web server creation
#Flask famework to map end points to Python functions

#/mine - to tell server to mine new block
#/pending_transations - to see list of unconfirmed transactions
#/new_transaction - create new transaction in block
#/chain- to return full blockchain
app = Flask(__name__)
 
# Create the object
# of the class blockchain
blockchain = BlockChain()
 
@app.route('/mine', methods=['GET'])
def mine_unconfirmed_transactions():
    result = blockchain.mine()
    if not result:
        return "No transactions to mine"
    return "Block #{} is mined.".format(result)

@app.route('/pending_transactions', methods=['GET'])
def get_pending_tx():
    return json.dumps(blockchain.unconfirmed_transactions)


@app.route('/new_transaction', methods=['POST'])
def new_transaction():
    tx_data = request.get_json()
    required_fields = ["author", "content"]
 
    for field in required_fields:
        if not tx_data.get(field):
            return "Invlaid transaction data", 404
 
    tx_data["timestamp"] = time.time()
 
    blockchain.add_new_transaction(tx_data)
 
    return "Success", 201

@app.route('/chain', methods=['GET'])
def full_chain():
    chain_data = []
    for block in blockchain.chain:
        chain_data.append(block.__dict__)
    return json.dumps({"length": len(chain_data),
                       "chain": chain_data})
    #response = {
    #    'chain': blockchain.chain,
    #    'length': len(blockchain.chain),
    #}
    #return jsonify(response), 200

 
 
# Run the flask server locally
app.run(host='127.0.0.1', port=5000)
