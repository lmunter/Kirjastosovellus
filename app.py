from flask import Flask
from flask import render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///postgres"
db = SQLAlchemy(app)

@app.route("/")
def index():
        return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
        return render_template("login.html", name=request.form["name"])

@app.route("/luotunnus")
def luotunnus():
        return render_template("luotunnus.html")