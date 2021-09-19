Comentarios
============

import json
import requests
from django.test import TestCase
import unittest

"""
test basico para entender como funciona test.py
"""
realizado el 16/09/2021
"""
from pip._internal import utils


class TestBasic(unittest.TestCase):
    "Basic tests"

    def test_basic(self):
        a = 1
        self.assertEqual(1, a)

    def test_basic_2(self):
        a = 1
        assert a == 1

"""
test para comprobar el Inicio de sesion, pasandole el username password
"""
realizado el 16/09/2021
"""

try:
    from unittest.mock import Mock, patch
except ImportError:
    from mock import Mock, patch  # noqa


class MockedResponse(object):
    def _init_(self, status_code, content, headers=None):
        if headers is None:
            headers = {}

        self.status_code = status_code
        self.content = content.encode("utf8")
        self.headers = headers

    def json(self):
        return json.loads(self.text)

    def raise_for_status(self):
        pass

    @property
    def text(self):
        return self.content.decode("utf8")

    class mocked_response:
        def _init_(self, *responses):
            self.responses = list(responses)

        def _enter_(self):
            self.orig_get = requests.get
            self.orig_post = requests.post
            self.orig_request = requests.request

            def mockable_request(f):
                def new_f(*args, **kwargs):
                    if self.responses:
                        return self.responses.pop(0)
                    return f(*args, **kwargs)

                return new_f

            requests.get = mockable_request(requests.get)
            requests.post = mockable_request(requests.post)
            requests.request = mockable_request(requests.request)

        def _exit_(self, type, value, traceback):
            requests.get = self.orig_get
            requests.post = self.orig_post
            requests.request = self.orig_request

            class BasicTests(TestCase):
                def setUp(self):
                    self.factory = RequestFactory()

                def test_generate_unique_username(self):
                    examples = [
                        ("a.b-c@example.com", "a.b-c"),
                        ("Üsêrnamê", "username"),
                        ("User Name", "user_name"),
                        ("", "user"),
                    ]
                    for input, username in examples:
                        self.assertEqual(utils.generate_unique_username([input]), username)

                def test_email_validation(self):
                    s = "this.email.address.is.a.bit.too.long.but.should.still.validate@example.com"  # noqa
                    self.assertEqual(s, utils.valid_email_or_none(s))

                def test_serializer(self):
                    class SomeValue:
                        pass

                    some_value = SomeValue()