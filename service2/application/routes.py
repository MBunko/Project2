from application import app
from flask import request, Response
import random

@app.route("/class0", methods=["GET"])
def class0(): 
    classes = ["Barbarian", "Bard", "Cleric", "Druid", "Fighter", "Monk", "Paladin", "Ranger", "Rogue", "Sorceror", "Warlock", "Wizard", "Artificer", "Blood-hunter"]
    rclass= random.choice(classes)
    return Response(str(rclass), mimetype="text/plain")