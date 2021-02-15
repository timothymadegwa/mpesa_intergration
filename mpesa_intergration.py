import os
import json
import requests
from requests.auth import HTTPBasicAuth

key = os.environ['MPESA_KEY']
secret = os.environ['MPESA_SECRET']
phone = "254708374149"

test_shortcode = "174379"
passkey = ''
credential = ''

consumer_key = key
consumer_secret = secret
def get_token():
    api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
  
    token = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret)).json()
    return token['access_token']

access_token = get_token()
print(access_token)

def lipa(token, shortcode, msisdn, amount):
    api_url = "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/simulate"
    headers = {"Authorization": "Bearer %s" % token}
    request = {"ShortCode":shortcode,
        "CommandID":"CustomerPayBillOnline",
        "Amount":amount,
        "Msisdn":msisdn,
        "BillRefNumber":" "}
  
    return requests.post(api_url, json = request, headers=headers).json()

response = lipa(access_token, test_shortcode, phone, 10)
print(response)