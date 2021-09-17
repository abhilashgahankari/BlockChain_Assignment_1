# BlockChain_Assignment_1

## Working
- curl 127.0.0.1:5000/chain - to see chain, ---- working
- curl 127.0.0.1:5000/pending_tx - to see unconfirmed transactions ----- working,
- curl 127.0.0.1:5000/mine - to compute transactions ---- **not working**,
- curl -X POST -H "Content-Type: application/json" -d '{
 "author": "test1",
 "content": "test2"
}' "http://localhost:5000/new_transaction"  ------working