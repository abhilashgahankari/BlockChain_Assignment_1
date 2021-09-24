# BITS F452 Blockchain Technology

## Programming_Assignment_1
***
# Dexter’s Blockchain

### Team
- Abhilash Gahankari - 2020H1030113H
- Aashita Dutta - 2020H1030130H
- Satish Phale - 2020H1030155H
***
### Functions
- Dexter has information regarding all the available blocks - add_block()
- None of Dexter's friends should be able to edit the added transactions - compute_hash(), mine() (Immutable and secured)
- Timestamp of each transaction is readily available - CreateBlock, AddNewTransaction
- Dexter should have all the information regarding the completed transactions - mine(), ProofOfWork(), ValidProof()

### Details
- A Block has an index, timestamp, list of transactions, HashValue of previous block, nonce
- Add new transactions to block with new_transaction
- Add genesis block to chain and hash it and create chain 
- add_blcok will add the new block with information to the pending_transactions.(unconfirmed pool)
- Moving transactions from unconfirmed pool to confirmed pool after mining performing proof of work and after consensus from other miners, the block is added to confirmed transactions.

***
### Working
*** To start the server***:

`python blockchain.py`

Following API's are available:

(one can use the postman or curl to hit these api).

- `curl 127.0.0.1:5000/chain `- to see chain (GET)
- `curl 127.0.0.1:5000/pending_transactions` - to see unconfirmed transactions (GET)
- `curl 127.0.0.1:5000/mine `- to compute transactions (GET)
- ``` 
  curl -X POST -H "Content-Type: application/json" -d '{  
    "author": "test1",
    "content": "test2"}' "http://localhost:5000/new_transaction" 
    ```
  to add new transaction/block (POST)

To create the new block, a json object with author and content have to be passed.(example for curl is given above. In the postman, POST request with body as above will also work.)

### sequence
1. To see empty chain, check `127.0.0.1:5000/chain`
2. To add new block/transaction, use POST method `http://localhost:5000/new_transaction`
3. To see unconfirmed transactions, use `curl 127.0.0.1:5000/pending_transactions`
4. To move unconfirmed transactions to confirmed chain, use `curl 127.0.0.1:5000/mine`
5. To see the new chain, use `127.0.0.1:5000/chain`