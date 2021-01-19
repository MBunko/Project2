from application import app
from flask import request, render_template, jsonify
import requests

@app.route('/')
def index():
    class1 = requests.get("http://service2:5000/class0")
    race1 = requests.get("http://service3:5000/race")
    adjective=requests.get("http://service4:5000/adjective", json={"class2":class1.text, "race2":race1.text})
    return render_template("index.html", class0=class1.text, race=race1.text, adj=adjective.text)

