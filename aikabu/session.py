#!/usr/bin/env python3

import random
import json
from functools import wraps

import requests

import aikabu.exceptions


class Decorators(object):
    def retry_on_session_timeout(func):
        """A decorator for retrying a request if the session
        has expired."""

        @wraps(func)
        def wrapper(self, *args, **kwargs):
            try:
                resp = func(self, *args, **kwargs)
            except aikabu.exceptions.SessionTimeoutException:
                self.reset_session_token()
                resp = func(self, *args, **kwargs)

            return resp
        return wrapper


class AikabuSession(object):
    _hosts = ["game0000.aikabu.net", "game0100.aikabu.net"]

    _platforms = {
        "android": {
            "user-agent": "Dalvik/1.6.0 (Linux; U; Android 4.4.2; GT-I9508 Build/KOT49H)",  # noqa E501,
            "app_version": "1.0.0",
            "platform_id": 2
        },
        "iphone": {
            "user-agent": "aikabu/19 CFNetwork/808.3 Darwin/16.3.0",
            "app_version": "1.0.0",
            "platform_id": "1"
        }
    }

    _headers_template = {
        "Accept": "*/*",
        "Content-Type": "application/json",
        "Accept-Language": "en-us",
        "Accept-Encoding": "X-Unity-Version: 5.5.2f1",
    }

    session_token = None

    def __init__(self, account_token, platform, session_token=False):
        self.account_token = account_token

        if platform not in self._platforms.keys():
            raise ValueError("Invalid platform {}".format(platform))
        self.platform = platform

        self.requests = requests.Session()
        self._update_headers()

        if session_token:
            self.session_token = session_token
        else:
            self.reset_session_token()

    def _update_headers(self):
        """Sets the correct headers for the Requests Session."""
        headers = dict(self._headers_template)
        headers["User-Agent"] = self._platforms[self.platform]["user-agent"]

        return self.requests.headers.update(headers)

    def reset_session_token(self):
        """Requests a new session_token."""

        path = "auth/login"

        platform_id = self._platforms[self.platform]["platform_id"]
        app_version = self._platforms[self.platform]["app_version"]

        data = {
            "data": {
                "account_token": self.account_token,
                "platform_id": platform_id,
                "app_version": app_version,
                "trace": "",
            }
        }

        data = self.post(path, data, skip_session_token=True)

        self.session_token = data["session_token"]

    @property
    def baseurl(self):
        """Creates a base URL using a random host, just
        like the app."""
        host = random.choice(self._hosts)
        return "https://{}/api_server".format(host)

    @Decorators.retry_on_session_timeout
    def post(self, path, data, skip_session_token=False):
        """Perform a POST request to a AiKaBu endpoint,
        with a payload."""
        url = "{}/{}".format(self.baseurl, path)

        if not skip_session_token:
            data["token"] = self.session_token

        data = json.dumps(data)

        resp = self.requests.post(url, data=data)

        if resp.status_code != 200:
            self._error_handler(resp)

        return resp.json()

    def _error_handler(self, response):
        try:
            data = response.json()

            if data.get('message', None):
                message = data['message']

                if message == "session timeout":
                    raise aikabu.exceptions.SessionTimeoutException()
                elif message == "Maintenance ON":
                    raise aikabu.exceptions.MaintenanceWindowException(message)
                else:
                    raise aikabu.exceptions.AikabuException(message)
        except ValueError:
            raise
