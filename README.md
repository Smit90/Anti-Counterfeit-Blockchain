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
![Miner Side](screen_shot/Implementation4.png?raw=true)

## Client Side Scripting
    -> default PORT is 8081
    Run -> python blockchain_client.py

    -> You can run this script on multiple PORT
    Run -> python blockchain_client.py -p 8082 
                    OR
    Run -> python blockchain_client.py --port 8082
![Client Side](screen_shot/Implementation1.png?raw=true)

## Customer Side
    Run -> python customer.py

    -> You can find product by product id but first you need to scan QR code, so you get product id.
![Customer Side](screen_shot/search.png?raw=true)

## Distributed System
    -> You need to config PORTS with other PORTS
    -> When miner mine blocks then all configured port are share same mined block.
![Distributed System](screen_shot/Implementation5.png?raw=true)

## Other Images
    -> Signup Page
![Signup Page](screen_shot/signup.png?raw=true)
    
    -> Login Page
![Login Page](screen_shot/login.png?raw=true)

    -> Profile Page
![Profile Page](screen_shot/profile.png?raw=true)

    -> Generated QR Code
![QR Code](screen_shot/QR.png?raw=true)

    -> Product search details
![Seach Details](screen_shot/searchDetails.png?raw=true)
