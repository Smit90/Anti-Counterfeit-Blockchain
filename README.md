# Anti - Counterfeit Blockchain

## Require Modules
    -> flask
    -> cors
    -> binascii
    -> RSA
    -> PKCS1_v1_5
    -> uuid4
    -> hashlib
    -> bson objectId
    -> pymongo
    -> dotenv-python

## Miner Side Scripting
    -> default PORT is 5001
    Run -> python blockchain.py

    -> You can run this script on multiple PORT
    Run -> python blockchain.py -p 5002 
                    OR
    Run -> python blockchain.py --port 5002

## Client Side Scripting
    -> default PORT is 8081
    Run -> python blockchain_client.py

    -> You can run this script on multiple PORT
    Run -> python blockchain_client.py -p 8082 
                    OR
    Run -> python blockchain_client.py --port 8082

## Customer Side
    Run -> python customer.py

    -> You can find product by product id but first you need to scan QR code, so you get product id.

