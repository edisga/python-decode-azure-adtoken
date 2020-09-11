from flask import Flask, request, jsonify
import os, sys, platform, json
app = Flask(__name__)

import jwt
import requests
from cryptography.x509 import load_pem_x509_certificate
from cryptography.hazmat.backends import default_backend

PEMSTART = '-----BEGIN CERTIFICATE-----\n'
PEMEND = '\n-----END CERTIFICATE-----\n'

    # get Microsoft Azure public key
def get_public_key_for_token(kid):
  response = requests.get(
  'https://login.microsoftonline.com/common/.well-known/openid-configuration',
  ).json()

  jwt_uri = response['jwks_uri']
  response_keys = requests.get(jwt_uri).json()
  pubkeys = response_keys['keys']

  public_key = ''

  for key in pubkeys:
      # found the key that matching the kid in the token header
      if key['kid'] == kid:
          # construct the public key object
          mspubkey = str(key['x5c'][0])
          cert_str = PEMSTART + mspubkey + PEMEND
          cert_obj = load_pem_x509_certificate(cert_str, default_backend())
          public_key = cert_obj.public_key()

  return public_key

# decode the given Azure AD access token
def aad_access_token_decoder(access_token):
  header = jwt.get_unverified_header(access_token)
  public_key = get_jwt_publickey(header['kid'])
  decoded = jwt.decode(access_token, key=public_key, algorithms='RS256',null)

  for key in decoded.keys():
      print key + ': ' + str(decoded[key])

@app.route("/")
def home():

    token1 =  request.headers.get('x-ms-token-aad-id-token')
    token2 =  request.headers.get('x-ms-token-aad-access-token')

    print("Token 1:" + token1)
    print("Token 2:" + token2)
    token_decoded = aad_access_token_decoder(token1)
    return token_decoded

if __name__ == '__main__':
    app.run(host='0.0.0.0')