#!/usr/bin/env python3

from aikabu.session import AikabuSession
from aikabu.model import AikabuException


class InvalidCodeException(AikabuException):
    pass


class Aikabu(object):
    def __init__(self, account_token, session_token=False):
        self.session = AikabuSession(account_token,
                                     session_token=session_token)

    def post(self, *args, **kwargs):
        return self.session.post(*args, **kwargs)

    def stock_summaries(self):
        path = "stock/summaries"

        stocks = self.get_stocks()
        codes = [s["stock_code"] for s in stocks]

        data = {
            "data": {
                "codes": codes,
                "fields": ["dividend_rate"],
                "trace": ""
            }
        }

        resp = self.post(path, data)

        return resp["stocks"]

    def get_stocks(self):
        path = "delistedstock/get"

        data = {
            "data": {
                "stock_code": [],
                "trace": ""
            }
        }

        resp = self.post(path, data)

        return resp

    def player_get(self):
        path = "player/get"

        data = {
            "data": {
                "fields": ["level", "holdings", "ex_holdings",
                           "total_profit_loss", "temp_holdings"],
                "trace": ""
            }
        }

        resp = self.post(path, data)

        return resp

    def stock_holdings(self, page=0):
        path = "stock/holdings"

        data = {
            "data": {
                "data": {
                    "page": page
                },
                "trace": ""
            }
        }

        resp = self.post(path, data)

        return resp

    def stock_history(self):
        path = "stock/history"

        data = {
            "data": {
                "data": [],
                "trace": ""
            }
        }

        resp = self.post(path, data)

        return resp

    def stock_exchange(self, index=0):
        path = "stock/exchange"

        data = {
            "data": {
                "index": index,
                "trace": ""
            }
        }


if __name__ == "__main__":
    pass
