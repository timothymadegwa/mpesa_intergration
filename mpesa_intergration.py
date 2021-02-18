import os
from datetime import datetime
import base64
import json
import requests
from requests.auth import HTTPBasicAuth

from flask import Flask, request, jsonify

app = Flask(__name__)

key = os.environ['MPESA_KEY']
secret = os.environ['MPESA_SECRET']
phone = "254708374149"
test_shortcode = "174379"
passkey = os.environ['MPESA_PASSKEY']

consumer_key = key
consumer_secret = secret

@app.route('/')
def index():
    return 'running....'

@app.route('/payment', methods=['GET','POST'])
def payment():
    access_token = get_token()
    return lipa(access_token, test_shortcode, phone, 1)

@app.route('/confirmation', methods=['GET','POST'])
def confirm():
    data = request.get_json()

    with open('confirmation.json', 'a') as f:
        f.write(jsonify(data))
    return {
        "ResultCode": 0,
        "ResultDesc" : "Accepted"
    }
    

def get_token():
    api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
  
    token = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret)).json()
    return token['access_token']



def lipa(token, shortcode, msisdn, amount):
    time = datetime.now()
    timestamp = time.strftime("%Y%m%d%H%M%S")
    cred = test_shortcode + passkey + timestamp
    cred = cred.encode('ascii')
    password = base64.b64encode(cred).decode("utf-8")
    
    api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    headers = { "Authorization": "Bearer %s" % token }
    request = {
        "BusinessShortCode": shortcode,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": msisdn,
        "PartyB": shortcode,
        "PhoneNumber": msisdn,
        "CallBackURL": "https://sandbox.safaricom.co.ke/mpesa/",
        "AccountReference": "account",
        "TransactionDesc": "test"
    }
  
    return requests.post(api_url, json = request, headers=headers).json()

if __name__ == "__main__":
    app.run(debug=False)