from main import basketbot

import unittest
from unittest.mock import patch

import flask
from telegram import Bot

app = flask.Flask(__name__)


class ClientTestCase(unittest.TestCase):
    def test_basketbot_channel(self):
        with open("channel_request.json") as f:
            with patch.object(Bot, "sendMessage", return_value="test message"):
                with app.test_request_context(method="POST", data=f):
                    r = flask.request
                    basketbot(r)

    def test_basketbot_personal(self):
        with open("private_request.json") as f:
            with patch.object(Bot, "sendMessage", return_value="test message"):
                with app.test_request_context(method="POST", data=f):
                    r = flask.request
                    basketbot(r)


if __name__ == "__main__":
    unittest.main()
