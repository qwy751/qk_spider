# -*- coding: utf-8 -*-


from unittest import TestCase
import time
from app import create_app, db
from app.models import User
from app.models import Role
from app.models import Permission


class TestUser(TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        Role.insert_roles()

    def test_generate_fake(self):
        self.fail()

    def test_password_setter(self):
        u = User(password='cat')
        self.assertTrue(u.password_hash is not None)

    def test_verify_password(self):
        self.fail()

    def test_ping(self):
        self.fail()

    def test_generate_confirmation_token(self):
        self.fail()

    def test_confirm(self):
        self.fail()
