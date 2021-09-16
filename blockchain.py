from hashlib import sha256
import json, time

#creating a single block
class Block:
    def __init__(self, index, timestamp, transactions, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.transactions = transactions
        self.previous_hash = previous_hash
    
    def compute_hash(self):
        block_string = json.dump(self.__dict__, sort_keys=True)
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
    
    @property
    def last_block(self):
        return self.chain[-1]