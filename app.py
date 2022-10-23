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
                virhe = "Käyttäjänimi tai salasana oli väärin"
                virhe_id = 1
                return render_template("error.html", virhe=virhe, virhe_id=virhe_id)
        else:
                salasalasana = user.password
                if check_password_hash(salasalasana, password):
                        session["username"] = user.id
                        sql = "SELECT title, author, year FROM Books LIMIT 10"
                        result = db.session.execute(sql)
                        kirjat = result.fetchall()
                        return render_template("login.html", name=name, kirjat=kirjat)
                else:
                        virhe = "Käyttäjänimi tai salasana oli väärin"
                        virhe_id = 1
                        return render_template("error.html", virhe=virhe, virhe_id=virhe_id)

@app.route("/hae")
def hae():
        käyttäjä = session["username"]
        sql = "SELECT B.id, B.title, B.author, B.year, L.user_id FROM Books B LEFT JOIN Loans L ON B.id=L.book_id LIMIT 10"
        result = db.session.execute(sql)
        kirjat = result.fetchall()
        return render_template("hae.html", kirjat=kirjat, käyttäjä=käyttäjä)

@app.route("/haehakusanalla", methods=["POST"])
def haehakusanalla():
        käyttäjä = session["username"]
        hakusana = request.form["hakusana"]
        sql = "SELECT B.id, B.title, B.author, B.year, L.user_id FROM Books B LEFT JOIN Loans L ON B.id=L.book_id WHERE (B.title LIKE :hakusana OR B.author LIKE :hakusana) LIMIT 10"
        result = db.session.execute(sql, {"hakusana":"%"+hakusana+"%"})
        kirjat = result.fetchall()
        return render_template("/hae.html", kirjat=kirjat, käyttäjä=käyttäjä)

@app.route("/palauta")
def palauta():
        kirja = request.args.get("book_id")
        käyttäjä = session["username"]
        if kirja is not None:
                try:
                        sql = "DELETE FROM Loans WHERE book_id=:kirja AND user_id=:käyttäjä"
                        db.session.execute(sql, {"kirja":kirja, "käyttäjä":käyttäjä})
                        db.session.commit()
                        return redirect("/hae")
                except:
                        virhe = "Palautus ei onnistunut"
                        virhe_id = 3
                        return render_template("/error.html", virhe=virhe, virhe_id=virhe_id)
        else:
                virhe = "Palautus ei onnistunut"
                virhe_id = 3
                return render_template("/error.html", virhe=virhe, virhe_id=virhe_id)

@app.route("/lainaa")
def lainaa():
        kirja = request.args.get("book_id")
        käyttäjä = session["username"]
        if kirja is not None:
                try:
                        sql = "INSERT INTO Loans (book_id, user_id) VALUES (:kirja, :käyttäjä)"
                        db.session.execute(sql, {"kirja":kirja, "käyttäjä":käyttäjä})
                        db.session.commit()
                        return redirect("/hae")
                except:
                        virhe = "Lainaus ei onnistunut"
                        virhe_id = 3
                        return render_template("/error.html", virhe=virhe, virhe_id=virhe_id)
        else:
                virhe = "Lainaus ei onnistunut"
                virhe_id = 3
                return render_template("/error.html", virhe=virhe, virhe_id=virhe_id)

@app.route("/luotunnus")
def luotunnus():
        return render_template("luotunnus.html")

@app.route("/luotunnus_varmistus", methods=["POST"])
def luotunnus_varmistus():
        name = request.form["name"]
        password = request.form["password"]
        password2 = request.form["password2"]
        if password == password2:
                salasalasana = generate_password_hash(password)
                sql = "SELECT id FROM Users WHERE username=:name"
                result = db.session.execute(sql, {"name":name})
                user = result.fetchone()
                if not user:
                        sql = "INSERT INTO Users (username, password) VALUES (:username, :password)"
                        db.session.execute(sql, {"username":name, "password":salasalasana})
                        db.session.commit()
                        return redirect("/")
                else:
                        virhe = "Käyttäjänimi on varattu"
                        virhe_id = 2
                        return render_template("/error.html", virhe=virhe, virhe_id=virhe_id)
        else:
                virhe = "Salasanat eivät täsmää"
                virhe_id = 2
                return render_template("/error.html", virhe=virhe, virhe_id=virhe_id)

@app.route("/logout")
def logout():
        del session["username"]
        return redirect("/")
