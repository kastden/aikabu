#!/usr/bin/env python3

import aikabu.exceptions
from aikabu.session import AikabuSession


class Aikabu(object):
    def __init__(self, account_token, platform, session_token=False):
        self.account_token = account_token
        self.platform = platform

        self.session = AikabuSession(self.account_token,
                                     self.platform,
                                     session_token=session_token)

    def post(self, *args, **kwargs):
        return self.session.post(*args, **kwargs)

    def stock_summaries(self, codes=None):
        """Get a summary of all the requested stocks.

        Default behaviour is to request the summary of all
        the listed stocks."""
        path = "stock/summaries"

        if not codes:
            codes = self.get_stocks(return_codes_only=True)

        data = {
            "data": {
                "codes": codes,
                "fields": ["dividend_rate"],
                "trace": ""
            }
        }

        resp = self.post(path, data)

        return resp["stocks"]

    def get_stocks(self, return_codes_only=False):
        """Returns a list of all the stocks traded on the exchange."""

        path = "delistedstock/get"

        data = {
            "data": {
                "stock_code": [],
                "trace": ""
            }
        }

        resp = self.post(path, data)

        if return_codes_only:
            codes = [s["stock_code"] for s in resp]
            return codes

        return resp

    def get_stock_data(self, stock_codes=[]):
        """Get the full company/player profile for a stock.

        If stock_codes is None/[] the full profile on all stocks
        in the game will be requested."""

        path = 'stock/get'

        if isinstance(stock_codes, str):
            stock_codes = [stock_codes]

        if not stock_codes:
            stock_codes = self.get_stocks(return_codes_only=True)

        data = {
            "data": {
                "codes": stock_codes,
                "fields": ["trend", "market_value_ranking_history",
                           "dividend_rate", "previous_dividend",
                           "reserve_diamond"],
                "trace": ""}
        }

        resp = self.post(path, data)

        return resp["stocks"]

    def get_player_info(self):
        """Returns information about the account you're authorized with."""
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
        """Returns the stocks you currently own ordered by the
        buy orders."""
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
        """Returns information about the stock exchange."""

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
            "data": {
                "page": page,
                "limit": limit,
                "trace": ""
            }
        }

        resp = self.post(path, data)

        return resp

    def presentbox_receive(self, ids=[]):
        """Receive gifts, ids is a list with present ids."""

        path = "presentbox/receive"

        # Receive all gifts
        if not ids:
            ids = "[-1]"

        data = {
            "data": {
                "ids": ids,
                "trace": ""}
        }

        resp = self.post(path, data)

        return resp


if __name__ == "__main__":
    pass
