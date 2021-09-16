#############################

from hashlib import new, sha256
import json, time
from flask import Flask, jsonify, request

#creating a single block
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

    def proof_of_work(self, block):
        block.nonce = 0
        computed_hash = block.compute_hash()
        while not computed_hash.startswith('0' * BlockChain.difficulty):
            block.nonce += 1
            computed_hash = block.compute_hash()
        return computed_hash
    
    def add_block(self, block, proof):
        previous_hash = self.last_block().hash
        if(previous_hash != block.previous_hash):
            return False
        if not self.is_valid_proof(block, proof):
            return False
        block.hash = proof
        self.chain.append(block)
        return True        

    def is_valid_proof(self, block, block_hash):
        return (block.hash == block.compute_hash() and block.hash.startswith('0' * BlockChain.difficulty))
    
    def add_new_transaction(self, transaction):
        self.unconfirmed_transactions.append(transaction)

    #compute method also called as mine
    def mine(self):
        if not self.unconfirmed_transactions:
            return False
        
        last_block = self.last_block
        new_block = Block(index = last_block.index + 1,
                            timestamp= time.time(),
                            transactions= self.unconfirmed_transactions,
                            previous_hash= last_block.hash)
        proof = self.proof_of_work(new_block)
        self.add_block(new_block)
        self.unconfirmed_transactions = []
        return new_block.index
        
#web server creation

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

@app.route('/pending_tx')
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
