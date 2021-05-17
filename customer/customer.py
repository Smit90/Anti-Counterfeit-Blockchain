from flask import Flask, request,jsonify, render_template, redirect, url_for, make_response, g
from pymongo import MongoClient
#QR code library
import qrcode
import qrtools
from bson.objectid import ObjectId
from bson.json_util import dumps
import json
from dotenv import load_dotenv
import os

load_dotenv()

MONGODB_URL = os.getenv('MONGODB_URL')


client = MongoClient(MONGODB_URL)
db = client.get_database('Blockchain')
transaction_blocks = db.chain_db
user_name = db.u_public_keys


# print(transaction_blocks.find_one({'_id': ObjectId('6058347a5a06ed289b7d6f35')}))

app = Flask(__name__)


@app.route('/')
def index():

    # if request.method == 'POST':
    #     procductId = request.form.get('productId')
    #     # print(procductId)
    #     product = transaction_blocks.find_one({"_id": ObjectId(procductId)})
    #     response = {
    #         "blockNumber" : jsonify(product['data']['block_number']),
    #         "senderPublicKey" : jsonify(product['data']['transactions'][0]['sender_public_key']),
    #         "recipientPublicKey" : jsonify(product['data']['transactions'][0]['recipient_public_key']),
    #         "amount" : jsonify(product['data']['transactions'][0]['amount'])
    #         }
    #     print(response)
    #     return 'ok'

    return render_template('searchById.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/product', methods=['POST'])
def fetchDeatails():
    
    procductId = request.form.get('productId')
    print(procductId)
    product = transaction_blocks.find_one({"_id": ObjectId(procductId)})
    if product:
        # response = {
        #     'blockNumber' : jsonify(product['data']['block_number']),
        #     'senderPublicKey' : jsonify(product['data']['transactions'][0]['sender_public_key']),
        #     'recipientPublicKey' : jsonify(product['data']['transactions'][0]['recipient_public_key']),
        #     'amount' : jsonify(product['data']['transactions'][0]['amount'])
        #     }

        # sender_key = product['data']['transactions'][0]['sender_public_key']
        # sender_details = user_name.find_one({'public_key': sender_key})
        # sender_name = sender_details['userEmail']
        response = jsonify({
            'blockNumber' : product['data']['block_number'],
            'timestamp' : product['data']['timestamp'],
            'senderPublicKey' : product['data']['transactions'][0]['sender_public_key'],
            'recipientPublicKey' : product['data']['transactions'][0]['recipient_public_key'],
            'productName' : product['data']['transactions'][0]['product_name'],
            'productDetails' : product['data']['transactions'][0]['product_details'],
            'amount' : product['data']['transactions'][0]['amount']
            })
    
        # print(product.items())
        # return render_template('product.html', blockNumber = blockNumber)
        return response
    else:
        response = {"message": "Invalid product ID"}
        return response
    return 'done!'



if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=3001, type=int, help="port to listen to")
    args = parser.parse_args()
    port = args.port

    app.run(host='127.0.0.1', port=port, debug=True)
