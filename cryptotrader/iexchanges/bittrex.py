from typing import Set
from decimal import Decimal
import time
import hmac
import hashlib

import requests

from cryptotrader.iexchanges.abc import BaseExchangeInterface


class Bittrex(BaseExchangeInterface):
    def __init__(self, key: str, secret: str) -> None:
        super().__init__()
        self.key = key
        self.secret = secret

    def get_now_btc_tickers(self) -> Set[str]:
        res = set()

        markets = requests.get(
            'https://bittrex.com/api/v1.1/public/getmarkets'
        )

        for t in markets.json()['result']:
            if t['BaseCurrency'] == "BTC" and t['IsActive']:
                res.add(t['MarketCurrency'])
        return res

    def buy_tickets(self, ticker: str, btc_amount: Decimal) -> str:
        bid_str = requests.get(
            'https://bittrex.com/api/v1.1/public/getticker',
            params={
                'market': f"BTC-{ticker}"
            }
        ).json()['result']['Bid']

        bid = Decimal(bid_str).quantize(Decimal("0.000000000000"))
        quantity = btc_amount / bid
        quantity = quantity.quantize(Decimal("0.00000000"))

        url = f"https://bittrex.com/api/v1.1/market/buylimit?market=BTC-{ticker}&quantity={str(quantity)}&rate={bid}&apikey={self.key}&nonce={time.time()}"
        apisign = hmac.new(self.secret.encode(), url.encode(), hashlib.sha512).hexdigest()
        res = requests.get(
            url,
            headers={"apisign": apisign},
            timeout=10
        ).json()

        if res['success'] is True:
            return res['result']['uuid']
        else:
            raise ValueError(res)

    def get_active_order_ids(self) -> Set[str]:
        url = f"https://bittrex.com/api/v1.1/market/getopenorders?apikey={self.key}&nonce={time.time()}"
        apisign = hmac.new(self.secret.encode(), url.encode(), hashlib.sha512).hexdigest()
        res = requests.get(
            url,
            headers={"apisign": apisign},
            timeout=10
        ).json()

        return set([x['OrderUuid'] for x in res['result']])

    def sell_tokens_from_order(self, order_id: str, profit: Decimal) -> str:
        url = f"https://bittrex.com/api/v1.1/account/getorder?apikey={self.key}&nonce={time.time()}&uuid={order_id}"
        apisign = hmac.new(self.secret.encode(), url.encode(), hashlib.sha512).hexdigest()
        res = requests.get(
            url,
            headers={"apisign": apisign},
            timeout=10
        ).json()
        buyed = Decimal(res['result']['Quantity'])
        market = res['result']['Exchange']
        price = Decimal(res['result']['PricePerUnit'])
        profit = price * profit
        rate = price + profit
        rate = rate.quantize(Decimal("0.000000000000"))

        url = f"https://bittrex.com/api/v1.1/market/selllimit?market={market}&quantity={str(buyed)}&rate={rate}&apikey={self.key}&nonce={time.time()}"
        apisign = hmac.new(self.secret.encode(), url.encode(), hashlib.sha512).hexdigest()
        res = requests.get(
            url,
            headers={"apisign": apisign},
            timeout=10
        ).json()

        if res['success'] is True:
            return res['result']['uuid']
        else:
            raise ValueError(res)

        raise ValueError