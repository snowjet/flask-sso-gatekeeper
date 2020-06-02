from flask import request
from flask import Flask
from flask import jsonify
from flask import redirect
from flask import render_template
from flask import session
from flask import url_for
import json

app = Flask(__name__)

@app.route('/')
def index():
  print(request.headers)

  headers = dict(request.headers)

  return jsonify(headers)
