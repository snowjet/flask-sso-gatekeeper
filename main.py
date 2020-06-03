from flask import request
from flask import Flask
from flask import jsonify
from flask import redirect
from flask import render_template
from flask import session
from flask import url_for
import json

from functools import wraps

import jwt
import os
import sys

app = Flask(__name__)


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "profile" not in session:
            # Redirect to Login page here
            return redirect("/")
        return f(*args, **kwargs)

    return decorated


def is_admin(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        userinfo = session["profile"]

        return f(*args, **kwargs)

    return decorated



def decode_jwt(auth_token, aud):

  try:
    PUBLIC_KEY = os.getenv("PUBLIC_KEY", "RSA Public Key")
    aud = aud.split(",")
    payload = jwt.decode(auth_token, PUBLIC_KEY, audience=aud)

    return "verified"
  except:
    return "verification failed with - %s" % sys.exc_info()[0]


@app.route("/")
def index():

    headers = dict(request.headers)

    if "X-Auth-Token" in headers:
         headers["payload_verified"] = decode_jwt(auth_token=headers["X-Auth-Token"], aud=headers["X-Auth-Audience"])

    return jsonify(session)


@app.route("/admin")
@is_admin
def admin():

    headers = dict(request.headers)

    if "X-Auth-Token" in headers:
         headers["payload_verified"] = decode_jwt(auth_token=headers["X-Auth-Token"], aud=headers["X-Auth-Audience"])

    return jsonify(headers)