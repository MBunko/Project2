import unittest
from flask import url_for
from flask_testing import TestCase
from os import getenv
import requests_mock

from application import app, db
from application.models import Character

class Testbase(TestCase):
    def create_app(self):
        app.config.update(SQLALCHEMY_DATABASE_URI=getenv("DATABASE_URI2"),
            DEBUG=True, WTF_CSRF_ENABLED=False
        )
        return app

    def setUp(self):
        db.create_all()
        test_character=Character(Character_class="Paladin", Character_race="Gnomish", Character_description="Super evil")
        db.session.add(test_character)
        db.session.commit()
        
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()

class TestCreate(Testbase):
    def test_char(self):
        with requests_mock.mock() as r:
            r.get("http://roller_service2:5000/class0", text="Barbarian")
            r.get("http://roller_service3:5000/race", text="Human")
            r.get("http://roller_service4:5000/adjective", text="Meaty")
            response=self.client.get(url_for("index"))
            self.assertEqual(response.status_code,200)
            self.assertIn(b'A Meaty Human Barbarian', response.data)
            self.assertIn(b'Someone got a Super evil Gnomish Paladin', response.data)
