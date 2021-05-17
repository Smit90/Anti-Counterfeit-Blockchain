from flask import Flask, request, jsonify, render_template, redirect, url_for, make_response, session, g
import Crypto
import Crypto.Random
from Crypto.PublicKey import RSA
import binascii
from collections import OrderedDict
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA
import jwt
import json
import datetime
from functools import wraps
from datetime import datetime
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()
MONGODB_URL = os.getenv('MONGODB_URL')

# current date and time
now = datetime.now()

timestamp = datetime.timestamp(now)
date_time = datetime.fromtimestamp(timestamp)
print("Date time object:", date_time)

#QR code library
import qrcode
qr = qrcode.QRCode(version=1,box_size=10,border=5)

#db connection
client = MongoClient(MONGODB_URL)
db = client.get_database('Blockchain')
transaction_chain = db['chain_db']
blockchainUser = db['B_user']
UserPublicKey = db['u_public_keys']

class Transaction:

    def __init__(self, sender_public_key, sender_private_key, recipient_public_key, product_name, product_details, amount):
        self.sender_public_key = sender_public_key
        self.sender_private_key = sender_private_key
        self.recipient_public_key = recipient_public_key
        self.product_name = product_name
        self.product_details = product_details
        self.amount = amount

    def to_dict(self):
        return OrderedDict({
            'sender_public_key': self.sender_public_key,
            'recipient_public_key': self.recipient_public_key,
            'product_name': self.product_name,
            'product_details': self.product_details,
            'amount': self.amount,
        })

    def sign_transaction(self):
        private_key = RSA.importKey(binascii.unhexlify(self.sender_private_key))
        signer = PKCS1_v1_5.new(private_key)
        h = SHA.new(str(self.to_dict()).encode('utf8'))
        return binascii.hexlify(signer.sign(h)).decode('ascii')


app = Flask(__name__)
app.secret_key = 'thisissecretkey'

@app.before_request
def before_request():
    g.user = None
    if 'user_email' in session:
        # userMail = request.headers['email']
        user = blockchainUser.find_one( {"email": session['user_email']})
        g.user = user

@app.route('/')
def index():
    if not g.user:
        return redirect('/login')
    # headers = request.headers.get('token')
    # print(headers)
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def userregister():

    if request.method == 'POST':
        name = request.form.get('username')
        email = request.form.get('email')
        category = request.form.get('category')
        password = request.form.get('password')

        userData = {'name':name, 'email':email,'category':category ,'password':password}
        blockchainUser.insert_one(userData)
        return redirect('/login')
    return render_template('registration.html')


@app.route('/login', methods=['GET', 'POST'])
def userlogin():

    if request.method == 'POST' : 
        session.pop('user_email', None)
        
        email = request.form.get('email')
        password = request.form.get('password')

        user = blockchainUser.find_one( { "email": email,})

        if user and user.get('password') == password:
            session['user_email'] = user.get('email') 
            return redirect(url_for('profile'))
        else:
            return redirect('/login')
            

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user_email',None)
    return redirect('/login')

@app.route('/profile')
def profile():
    if not g.user:
        return redirect('/login')
    return render_template('profile.html')


@app.route('/about')
def about():
    return render_template('about.html')

# @app.route('/registration_process', methods=['POST'])
# def registration():
#     name = request.form.get('username')
#     email = request.form.get('email')
#     category = request.form.get('category')
#     password = request.form.get('password')

#     userData = {'name':name, 'email':email,'category':category ,'password':password}
#     blockchainUser.insert_one(userData)

#     return redirect('/login')


# @app.route('/login_process', methods=['POST'])
# def login():

#     email = request.form.get('email')

#     user = blockchainUser.find_one( { "email": email,})
#     userId = user.get('_id')
#     uId = str(userId)
#     if user:
#         encoded_jwt = jwt.encode({'data':uId}, "testJWT", algorithm="HS256")
#         response = make_response(redirect('/'))
#         response.headers["Set-Cookie"]="token=" + encoded_jwt
#         return response
#     else:
#         return redirect('/login')

@app.route('/generate/transaction', methods=['POST'])
def generate_transaction():
    sender_public_key = request.form['sender_public_key']
    sender_private_key = request.form['sender_private_key']
    recipient_public_key = request.form['recipient_public_key']
    product_name = request.form['product_name']
    product_details = request.form['product_details']
    amount = request.form['amount']

    transaction = Transaction(sender_public_key, sender_private_key, recipient_public_key, product_name, product_details, amount)

    response = {'transaction': transaction.to_dict(),
                'signature': transaction.sign_transaction()}


    # new_transaction ={
    #     'sender_public_key': sender_public_key,
    #     'recipient_public_key': recipient_public_key,
    #     'amount': amount,
    #     'signature': response,
    # }
    #
    # transaction_chain.insert_one(new_transaction)
    #
    # id = transaction_chain.find_one({'sender_public_key': sender_public_key})
    # ob_id = id.get('_id')
    #
    # # QR Code generation
    # data = ob_id
    # qr.add_data(data)
    # qr.make(fit=True)
    # img = qr.make_image(fill="black", back_color="white")
    # img.save("test.png")

    return jsonify(response), 200


@app.route('/make/transaction')
def make_transaction():
    if not g.user:
        return redirect('/login')
    return render_template('make_transaction.html')


@app.route('/view/transactions')
def view_transactions():
    return render_template('view_transactions.html')


@app.route('/wallet/new')

def new_wallet():
    if not g.user:
        return redirect('/login')
    else:
        random_gen = Crypto.Random.new().read
        private_key = RSA.generate(1024, random_gen)
        public_key = private_key.publickey()
        userEmail = g.user.get('email')
        response = {
            'private_key': binascii.hexlify(private_key.export_key(format('DER'))).decode('ascii'),
            'public_key': binascii.hexlify(public_key.export_key(format('DER'))).decode('ascii')
        }
        checkMail = UserPublicKey.find_one({'userEmail': userEmail})
        if checkMail:
            response = {'message': 'You already generated your wallet keys!'}
            return response
        else:
            userdata = {"public_key": list(response.values())[1], 'userEmail':userEmail,'timeStamp': date_time}
            UserPublicKey.insert_one(userdata)
            return jsonify(response) , 200
    return 'Done!'



# @app.route('/all/transactions/', methods=['GET'])
# def getAllTransactions():
#     transactions = []
#     allData = list(transaction_chain.find())
#     transactions = allData
#     print(transactions[0]['data']['transactions'][0]['product_name'])
#     print(transactions[1]['data']['transactions'][0]['product_name'])

#     return 'done'


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=8081, type=int, help="port to listen to")
    args = parser.parse_args()
    port = args.port

    app.run(host='127.0.0.1', port=port, debug=True)
