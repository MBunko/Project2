from application import app
from flask import request, Response
import random

@app.route("/adjective", methods=["GET", "POST"])
def adjective():
    desc= {"Barbarian":["Rabid", "Meaty"], "Artificer":["Genius", "Completely unaware of their surroundings"], "Blood-hunter":["Sadistic beyond belief", "Schimitar master"] "Bard":["Ugly as sin but still charasmatic", "Sharp as a tack"], "Cleric":["Bright", "Unholy"], "Druid":["Hairy", "Versatile"], "Fighter":["Brainless", "Untouchable"], "Monk":["Drunken", "Way too fast"], "Paladin":["Overzealous", "Evil-stomping"], "Ranger":["Spider obsessed","Eagle eyed"], "Rogue":["Shady", "Basically invisible"], "Sorceror":["Overpowered", "Completely spoiled"], "Warlock":["Patron fearing", "Crafty as hell"], "Wizard":["Mad", "Genius"], "Dwarven":["Extremely fat", "Just a tad too greedy", "Immovable when drunk"], "Elven":["Really old", "Less pretentious than you'd think", "Extra deadly"], "Gnomish":["Halfling looking", "Extremely charasmatic", "Con artist"],  "Halfling":["Way too tiny", "Shockingly bloodthirsty", "More agile than a bunny"], "Half-Elven":["Good at eveything", "Racist to everyone", "Wait, another"], "Half-Orcish":["Very, very green", "Aboslutely livid", "Stronger than everyone"], "Human":["Boring", "Versatile", "Lovey dovey"]}
    char=request.get_json()
    class1= char["class2"]
    race= char["race2"]
    a= ["Completely useless", "Super evil"]
    a.extend(desc[class1])
    a.extend(desc[race])
    b=random.choice(a)

    return Response(b, mimetype="text/plain")
