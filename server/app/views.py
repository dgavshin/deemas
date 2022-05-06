from flask import jsonify, request
from flask import render_template

from server.app import app
from server.app import auth


@app.route("/")
def hello():
    return "hello!"


flags = []


@app.route("/flags")
def get_flag():
    return jsonify(flags=flags)


@app.route("/flags", methods=["POST"])
def put_flag():
    flag = request.json["flag"]
    flags.append(flag)
    return flag


@app.route('/services', methods=["GET"])
@auth.auth_required
def services():
    return render_template("services.html")


@app.route('/rules', methods=["GET"])
@auth.auth_required
def rules():
    return render_template("rules.html")
