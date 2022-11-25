from flask import request
from flask import Flask
from flask import jsonify
from flask import redirect
from flask import render_template
from flask import session
from flask import url_for
from flask import abort

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
        headers = dict(request.headers)

        if "X-Forwarded-Groups" not in headers:
            raise abort(403, description="Not an admin")

        groups = headers["X-Forwarded-Groups"].split(",")

        if "admin" not in groups:
            raise abort(403, description="Not an admin")

        return f(*args, **kwargs)

    return decorated


def decode_jwt(token):

    try:
        PUBLIC_KEY = os.getenv("PUBLIC_KEY", "RSA Public Key")
        options={'verify_aud': False}
        payload = jwt.decode(token, PUBLIC_KEY, algorithms=["RS256"], options=options)

        return "verified"
    except:
        return "verification failed with - %s" % sys.exc_info()[0]


@app.route("/")
def index():

    headers = dict(request.headers)

    if "X-Forwarded-Access-Token" in headers:
        headers["payload_verified"] = decode_jwt(
            token=headers["X-Forwarded-Access-Token"]
        )

    json_format = json.dumps(headers, sort_keys = False, indent = 2)
 
    return render_template("index.html", json_format=json_format)



@app.route("/admin")
@is_admin
def admin():

    headers = dict(request.headers)

    if "X-Forwarded-Access-Token" in headers:
        headers["payload_verified"] = decode_jwt(
            token=headers["X-Forwarded-Access-Token"]
        )

    admin_return = {}
    admin_return["user"] = headers["X-Forwarded-Preferred-Username"]
    admin_return["is_admin"] = True

    json_format = json.dumps(admin_return, sort_keys = False, indent = 2)
 
    return render_template("index.html", json_format=json_format)
