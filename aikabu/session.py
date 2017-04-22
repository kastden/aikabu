#!/usr/bin/env python3

import random
import json
from functools import wraps

import requests

from aikabu.model import AikabuException


class SessionTimeoutException(AikabuException):
    pass


class MaintenanceWindowException(AikabuException):
    pass


class Decorators(object):
    def retry_on_session_timeout(func):
        """A decorator for retrying a request if the session
        has expired."""

        @wraps(func)
        def wrapper(self, *args, **kwargs):
            try:
                resp = func(self, *args, **kwargs)
            except SessionTimeoutException:
                self.reset_session_token()
                resp = func(self, *args, **kwargs)
            except BaseException:
                raise

            return resp
        return wrapper


class AikabuSession(object):
    _hosts = ["game0000.aikabu.net", "game0100.aikabu.net"]
    _platform_id = 2
    _app_version = "1.0.0"

    headers = {
        "User-Agent": "Dalvik/1.6.0 (Linux; U; Android 4.4.2; GT-I9508 Build/KOT49H)",
        "Accept": "*/*",
        "Content-Type": "application/json",
        "Accept-Language": "en-us",
        "Accept-Encoding": "X-Unity-Version: 5.5.2f1",
    }

    session_token = None

    def __init__(self, account_token, session_token=False):
        self.requests = requests.Session()
        self.requests.headers.update(self.headers)

        self.account_token = account_token

        if session_token:
            self.session_token = session_token
        else:
            self.reset_session_token()

    def reset_session_token(self):
        path = "auth/login"

        data = {
            "data": {
                "account_token": self.account_token,
                "platform_id": self._platform_id,
                "app_version": self._app_version,
                "trace": "",
            }
        }

        data = self.post(path, data, skip_session_token=True)

        self.session_token = data["session_token"]

    @property
    def baseurl(self):
        host = random.choice(self._hosts)
        return "https://{}/api_server".format(host)

    @Decorators.retry_on_session_timeout
    def post(self, path, data, skip_session_token=False):
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
                    raise SessionTimeoutException
                elif message == "Maintenance ON":
                    raise MaintenanceWindowException(message)
                else:
                    raise AikabuException(message)
        except ValueError:
            raise
