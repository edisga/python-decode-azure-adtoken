from flask import Flask, request, jsonify
import os, sys, platform, json
app = Flask(__name__)

import jwt

def decode_token(token):
  decoded = jwt.decode(token, verify=False)
  for key in decoded.keys():
     print(key + ': ' + str(decoded[key]))
  return decoded

@app.route("/")
def home():

    token =  request.headers.get('x-ms-token-aad-id-token')
    #token2 =  request.headers.get('x-ms-token-aad-access-token')

    print(token)
    print("--------------")
    #print(token2)
    token_decoded = decode_token(token)
    return token_decoded

if __name__ == '__main__':
    app.run(host='0.0.0.0')