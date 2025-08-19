from flask import Flask
from flask import request
from flask import render_template
from flask import redirect
from flask import url_for
from pymongo import MongoClient
from bson import ObjectId
client = MongoClient("mongodb://mongo:27017/")
mydb = client["mydatabase"]
mycol = mydb["mycollection"]



app = Flask(__name__)



@app.route("/")
def main():
    data = []
    for x in mycol.find():
        data.append(x)
    return render_template("index.html", data=data)

@app.route("/add", methods=["POST"])
def add_comment():
    ip = request.form.get("ip")
    username = request.form.get("username")
    password = request.form.get("password")
    if username and password and ip:
        x = mycol.insert_one({"ip": ip,"username": username,"password": password})

    return redirect(url_for("main"))

@app.route("/delete", methods=["POST"])
def delete_comment():
    try:
        idx = request.form.get("idx")
        myq = {'_id': ObjectId(idx)}
        x = mycol.delete_one(myq)
    except Exception:
        pass
    return redirect(url_for("main"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
