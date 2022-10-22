from flask import Flask
from flask import redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
from os import getenv

app = Flask(__name__)
db_url = getenv("DATABASE_URL")
if db_url.startswith("postgres://"):
        db_url = "postgresql" + db_url[8:]
#tämä on herokun bugin kiertämistä varten
app.config["SQLALCHEMY_DATABASE_URI"] = db_url
db = SQLAlchemy(app)
app.secret_key = getenv("SECRET_KEY")

@app.route("/")
def index():
        return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
        name = request.form["name"]
        password = request.form["password"]
        sql = "SELECT id, password FROM Users WHERE username=:name"
        result = db.session.execute(sql, {"name":name})
        user = result.fetchone()
        if not user:
                return redirect("/")
        else:
                salasalasana = user.password
                if check_password_hash(salasalasana, password):
                        session["username"] = name
                        sql = "SELECT title, author, year FROM Books LIMIT 10"
                        result = db.session.execute(sql)
                        kirjat = result.fetchall()
                        return render_template("login.html", name=name, kirjat=kirjat)
                else:
                        return redirect("/")

@app.route("/hae")
def hae():
        sql = "SELECT title, author, year FROM Books LIMIT 10"
        result = db.session.execute(sql)
        kirjat = result.fetchall()
        return render_template("hae.html", kirjat=kirjat)

@app.route("/haehakusanalla", methods=["POST"])
def haehakusanalla():
        hakusana = request.form["hakusana"]
        sql = "SELECT title, author, year FROM Books WHERE title=:hakusana OR author=:hakusana LIMIT 10"
        result = db.session.execute(sql, {"hakusana":hakusana})
        kirjat = result.fetchall()
        return render_template("/hae.html", kirjat=kirjat)

@app.route("/luotunnus")
def luotunnus():
        return render_template("luotunnus.html")

@app.route("/luotunnus_varmistus", methods=["POST"])
def luotunnus_varmistus():
        name = request.form["name"]
        password = request.form["password"]
        salasalasana = generate_password_hash(password)
        sql = "SELECT id FROM Users WHERE username=:name"
        result = db.session.execute(sql, {"name":name})
        user = result.fetchone()
        if not user:
                sql = "INSERT INTO Users (username, password) VALUES (:username, :password)"
                db.session.execute(sql, {"username":name, "password":salasalasana})
                db.session.commit()
                return redirect("/login")
        else:
                return redirect("/luotunnus")

@app.route("/logout")
def logout():
        del session["username"]
        return redirect("/")
