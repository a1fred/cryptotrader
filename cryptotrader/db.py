from typing import Set

import pickledb

from cryptotrader.iexchanges.abc import BaseExchangeInterface


def fullname(o: object) -> str:
    module = o.__class__.__module__
    if module is None or module == str.__class__.__module__:
        return o.__class__.__name__
    return module + '.' + o.__class__.__name__


class Db:
    def __init__(self, *args, **kwargs) -> None:
        self.db = pickledb.load('cryptotrader.db', True)

        self.known_tickers_key = 'known_tickers'
        self.orders_key = 'orders'
        self.sell_orders_key = 'sell-orders'

    # Tickers
    def get_last_known_tickers(self, exchange: BaseExchangeInterface) -> Set[str]:
        return set(self.db.get(f"{self.known_tickers_key}-{fullname(exchange)}") or [])

    def set_last_known_tickers(self, exchange: BaseExchangeInterface, tickers: Set['str']) -> None:
        self.db.set(f"{self.known_tickers_key}-{fullname(exchange)}", list(tickers))

    # Buy orders
    def add_new_order_id(self, exchange: BaseExchangeInterface, order_id: str) -> None:
        key = f"{self.orders_key}-{fullname(exchange)}"
        orders = list(self.db.get(key) or [])
        orders.append(order_id)
        self.db.set(key, orders)

    def remove_order_id(self, exchange: BaseExchangeInterface, order_id: str) -> None:
        key = f"{self.orders_key}-{fullname(exchange)}"
        orders = list(self.db.get(key) or [])
        self.db.set(key, [x for x in orders if x != order_id])

    def get_buy_order_ids(self, exchange: BaseExchangeInterface) -> Set[str]:
        key = f"{self.orders_key}-{fullname(exchange)}"
        return set(self.db.get(key) or [])

    # Sell orders
    def add_sell_order_id(self, exchange: BaseExchangeInterface, order_id: str) -> None:
        key = f"{self.sell_orders_key}-{fullname(exchange)}"
        orders = list(self.db.get(key) or [])
        orders.append(order_id)
        self.db.set(key, orders)

    def remove_sell_order_id(self, exchange: BaseExchangeInterface, order_id: str) -> None:
        key = f"{self.sell_orders_key}-{fullname(exchange)}"
        orders = list(self.db.get(key) or [])
        self.db.set(key, [x for x in orders if x != order_id])

    def get_sell_order_ids(self, exchange: BaseExchangeInterface) -> Set[str]:
        key = f"{self.sell_orders_key}-{fullname(exchange)}"
        return set(self.db.get(key) or [])
