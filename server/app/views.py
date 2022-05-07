from flask import render_template, redirect

from server.app import app


@app.route("/")
def hello():
    return redirect('/docs')


@app.route('/services', methods=["GET"])
def services():
    return render_template("services.html")


@app.route('/rules', methods=["GET"])
def rules():
    return render_template("rules.html")
