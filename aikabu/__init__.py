#!/usr/bin/env python3

import aikabu.exceptions
from aikabu.session import AikabuSession


class Aikabu(object):
    def __init__(self, account_token, session_token=False):
        self.session = AikabuSession(account_token,
                                     session_token=session_token)

    def post(self, *args, **kwargs):
        return self.session.post(*args, **kwargs)

    def stock_summaries(self, codes=None):
        """Get a summary of all the requested stocks.
        Default behaviour is to request the summary of all the listed stocks."""
        path = "stock/summaries"

        if not codes:
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
        """Returns a list of all the stocks traded on the exchange."""
        path = "delistedstock/get"

        data = {
            "data": {
                "stock_code": [],
                "trace": ""
            }
        }

        resp = self.post(path, data)

        return resp

    def get_player_info(self):
        """Returns information about the account you're authorized with.

        Information like your user id, level, holdings, etc."""
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
        # Don't know what this does
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
        """Returns a history of stocks you have bought and sold."""
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
        """Returns information about the stock exchange.

        Information like index value etc."""
        path = "stock/exchange"

        data = {
            "data": {
                "index": index,
                "trace": ""
            }
        }

        resp = self.post(path, data)

        return resp

    def get_presentbox(self, page=0, limit=999):
        """Returns a list with all your gifts."""

        path = "presentbox/get"

        data = {
            "data" : {
                "page": page,
                "limit": limit,
                "trace": ""
            }
        }

        resp = self.post(path, data)

        return resp

    def presentbox_receive(self, ids=None):
        """Receive gifts, ids is a list with present ids."""

        path = "presentbox/receive"

        # Receive all gifts
        if not ids:
            ids = "[-1]"

        data = {
            "data": {
                "ids": ids,
                "trace":""}
            }

        resp = self.post(path, data)

        return resp


if __name__ == "__main__":
    pass
