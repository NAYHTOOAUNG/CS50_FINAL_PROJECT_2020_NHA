from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
import datetime
import urllib3
from urllib.parse import urlencode
import json
#import sqlite3
import os
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from cs50 import SQL
from helpers import apology, login_required

# Create Flask app instance
app = Flask(__name__)
app.secret_key = "abcde12345"

http = urllib3.PoolManager()

# Make sure responses
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        response.headers['Cache-Control'] = 'public, max-age=0'
        return response

#con = sqlite3.connect("clinic.db")
#c = con.cursor()

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///clinic.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")

@app.route("/")
@login_required
def main():
    # take the list of entire patients from the rear
    r = http.request('GET','http://localhost:5001/main')
    db_patient = json.loads(r.data.decode('utf-8'))
    return render_template("main.html", db_patient=db_patient)

@app.route("/information")
@login_required
def information():
    if request.method == "POST":
        return redirect("/")
    return render_template("information.html")

@app.route("/append", methods=["GET", "POST"])
@login_required
def append():
    if request.method == "POST":
        # Convert entire records of an object which is transferred to the rear
        birthdate = datetime.date(int(request.form["year"]),int(request.form["month"]),int(request.form["day"])).isoformat()
        args = {
            "firstName":request.form.get("firstName"),
            "lastName":request.form.get("lastName"),
            "birthdate": birthdate,
            "age":datetime.datetime.now().year - int(request.form.get("year")),
            "gender":request.form.get("gender"),
            "swab":request.form.get("swab"),
            "serology":request.form.get("serology")
        }
        # Encode arguments to a query string
        url_args = urlencode(args)
        r = http.request("POST","http://localhost:5001/append?" + url_args)
        return redirect("/")
    return render_template("append.html")

@app.route("/delete", methods=["GET", "POST"])
@login_required
def delete():
    if request.method == "POST":
        # Build an object with the UID to be deleted
        args = {
            "uid": request.form["uid"]
        }
        # Encode object to a query string
        url_args = urlencode(args)
        r = http.request("POST","http://localhost:5001/delete?" + url_args)
    return redirect("/")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM user WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/create", methods=["GET", "POST"])
def create():
    """Create User"""

    session.clear()
    # Submitting A Form Via POST
    if request.method == "POST":
        # Verify User Name Submission
        if not request.form.get("username"):
            return apology("User Name Must Be Provided", 403)
        # Verify Password Submission
        elif not request.form.get("password"):
            return apology("Password Must Be Provided", 403)
        # Verify Confirm Password Matching
        elif request.form.get("password") != request.form.get("confirm-password"):
            return apology("Unmatched Passwords", 403)

        # Verify User Name Is Already Taken
        elif db.execute("select * from user where username = :username", username=request.form.get("username")):
            return apology("User Name Is Already Existed", 403)
        # Inserting User Name & Passowrd (Hash)
        db.execute("insert into user(username, hash) values (:username, :hash)",
            username = request.form.get("username"), hash = generate_password_hash(request.form.get ("password")))
        # Retrieve User
        rows = db.execute("select * from user where username = :username", username = request.form.get("username"))
        # Save Logged In User
        session["user_id"] = rows[0]["id"]
        # Redirecting To Home Page
        return redirect("/")

    else:
        return render_template("create.html")
    #return apology("TODO")

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)

# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
