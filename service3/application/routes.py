from application import app
from flask import request, Response
import random

@app.route("/race", methods=["GET"])
def race(): 
    races = ["Dwarf", "Elf", "Gnome", "Halfling", "Half-Elf", "Half-Orc", "Human"]
    ranrace= random.choice(races)
    return Response(str(ranrace), mimetype="text/plain")
