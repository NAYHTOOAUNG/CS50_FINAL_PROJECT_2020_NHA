from flask import Flask, request, jsonify, redirect, render_template
import sqlite3

app = Flask(__name__)

@app.route("/main")
def main():
    # Build SQL connection, select entire records and return the json object
    with sqlite3.connect("clinic.db") as con:
        cursor = con.cursor()
        cursor.execute("SELECT * FROM patient")
        db_patient = cursor.fetchall()
    return jsonify(db_patient)

@app.route("/information")
def information():
    if request.method == "POST":
        return redirect("/")
    return render_template("information.html")

@app.route("/append", methods=["POST"])
def append():
    # Build SQL connection, insert the values from the query string
    with sqlite3.connect("clinic.db") as con:
        cursor = con.cursor()
        cursor.execute("INSERT INTO patient (firstname, lastname, birthdate, age, sex, st, srlt) VALUES (?,?,?,?,?,?,?)",
            (request.args.get("firstName", ""),
            request.args.get("lastName", ""),
            request.args.get("birthdate", ""),
            request.args.get("age", ""),
            request.args.get("gender", ""),
            request.args.get("swab", ""),
            request.args.get("serology", "")))
    return "200"

@app.route("/delete", methods=["POST"])
def delete():
    # Build SQL connection, get UID from query string and execute DELETE statement
    if request.args.get("uid", ""):
        with sqlite3.connect("clinic.db") as con:
            cursor = con.cursor()
            cursor.execute("DELETE FROM patient WHERE id = (?)", (request.args.get("uid",""),))
        return "200"

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001, debug=True)