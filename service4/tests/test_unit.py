import unittest
from flask import url_for
from flask_testing import TestCase
from os import getenv
import requests_mock

from application import app

class Testbase(TestCase):
    def create_app(self):
        return app

class TestCreate(Testbase):
    def test_char(self):
        response=self.client.post(url_for("adjective"), json={"class2":"Barbarian", "race2":"Dwarven"})
        self.assertEqual(response.status_code,200)
        self.assertIn(response.data, [b"Meaty", b"Completely useless", b"Super evil", b"Rabid", b"Extremely fat", b"Just a tad too greedy", b"Immovable when drunk" ])