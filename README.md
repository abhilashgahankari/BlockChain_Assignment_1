# BITS F452 Blockchain Technology
# Dexter’s Blockchain

## Programming_Assignment_1
## Team
- Abhilash Gahankari - 2020H1030113H
- Aashita Dutta - 2020H1030130H
- Satish Phale - 2020H1030155H

## Functions
- Dexter has information regarding all the available blocks - CreateBlock(), CreateBlockChain
- None of Dexter's friends should be able to edit the added transactions - Hash() (Immutable and secured)
- Timestamp of each transaction is readily available - CreateBlock, AddNewTransaction
- Dexter should have all the information regarding the completed transactions - Mine(), ProofOfWork(), ValidProof()

- A Block has an index, timestamp, list of transactions, HashValue of previous block, nonce
- Add new transactions to block with new_transaction
- Add genesis block to chain and hash it and create chain by performin new transactions to add new blocks to first block to form chain. 
- Moving transactions from unconfirmed pool to confirmed pool after mining performing proof of work and after consensus from other miners, the block is added to confirmed transactions

## Working
- curl 127.0.0.1:5000/chain - to see chain, ---- working
- curl 127.0.0.1:5000/pending_tx - to see unconfirmed transactions ----- working
- curl 127.0.0.1:5000/mine - to compute transactions ---- working
- curl -X POST -H "Content-Type: application/json" -d '{
 "author": "test1",
 "content": "test2"
}' "http://localhost:5000/new_transaction"  ------working

