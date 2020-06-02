from flask import request
from flask import Flask
from flask import jsonify
from flask import redirect
from flask import render_template
from flask import session
from flask import url_for
import json

import jwt
import os

app = Flask(__name__)

def decode_token(auth_token):

  SECRET_KEY = os.getenv("SECRET_KEY", "random key")
  payload = jwt.decode(auth_token, SECRET_KEY)
  
  return payload

@app.route('/')
def index():
  print(request.headers)

  headers = dict(request.headers)

  if 'X-Auth-Token' in headers:
    token = decode_token(auth_token=headers['X-Auth-Token'])
    print(token)

  print(json.dumps(headers))

  return jsonify(headers)
