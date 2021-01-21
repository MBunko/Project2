from application import app, db
from application.models import Character
from flask import request, render_template, jsonify
import requests
from sqlalchemy import desc

@app.route('/')
def index():
    class1 = requests.get("http://service2:5000/class0")
    race1 = requests.get("http://service3:5000/race")
    adjective=requests.get("http://service4:5000/adjective", json={"class2":class1.text, "race2":race1.text})
    char=Character.query.order_by(desc("Id")).limit(5).all()
    new_character= Character(Character_class=class1.text, Character_race=race1.text, Character_description=adjective.text)
    db.session.add(new_character)
    db.session.commit()
    
    return render_template("index.html", class0=class1.text, race=race1.text, adj=adjective.text, char=char)

