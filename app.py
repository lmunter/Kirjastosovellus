from flask import Flask
from flask import render_template, request
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
if __name__ == "__main__":
        ON_HEROKU = os.environ.get("ON_HEROKU")
        if ON_HEROKU:
                port = int(os.environ.get("ON_HEROKU"))
        else:
                port = 3000

        app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///postgres"
        db = SQLAlchemy(app)

        app.run(port=port)

@app.route("/")
def index():
        return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
        return render_template("login.html", name=request.form["name"])

@app.route("/luotunnus")
def luotunnus():
        return render_template("luotunnus.html")