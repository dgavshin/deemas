from flask import Flask
from flask import request

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def hello():

    flag = "Default Flag"
    if request.args.get("flag"):
        flag = request.args.get("flag")
    elif request.get_data():
        flag = request.get_data().decode()
    print(f"Getting some flag! {flag}")
    return f'Here is your flag: {flag}'
