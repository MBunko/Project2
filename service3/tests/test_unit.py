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
        response=self.client.get(url_for("race"))
        self.assertEqual(response.status_code,200)
        self.assertIn(response.data, [b"Dwarven", b"Elven", b"Gnome", b"Halfling", b"Half-Elf", b"Half-Orc", b"Human"])