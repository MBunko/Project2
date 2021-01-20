from application import db
#from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, DateField
from wtforms.validators import DataRequired, NumberRange, Length
from datetime import datetime

class Character(db.Model):
    Id=db.Column(db.Integer, primary_key=True)
    Character_class=db.Column(db.String(30), nullable=False)
    Character_race=db.Column(db.String(30), nullable=False)
    Character_description= db.Column(db.String(3000), nullable=False)
    Date=db.Column(db.DateTime, nullable=False, default=datetime.utcnow)