from flask import request

@app.route('/')
def index():
    print(request.headers)
