from typing import Set
import logging; logger = logging.getLogger(__name__)  # noqa

import settings
from cryptotrader.iexchanges import EXCHANGES
from cryptotrader.db import Db


btc_amount = settings.btc_amount
profit = settings.profit


def main():
    db: Db = Db()

    for exchange in EXCHANGES:
        # handle new tickers
        known_tickers: Set[str] = db.get_last_known_tickers(exchange)
        now_tickers: Set[str] = exchange.get_now_btc_tickers()
        new_tickers = now_tickers - known_tickers
        logger.info(f"New tickers: {list(new_tickers)}")

        new_orders: Set[str] = set()
        for ticker in new_tickers:
            logger.info(f"Placing order to buy {ticker} for {btc_amount}BTC")
            order_id = exchange.buy_tickets(ticker=ticker, btc_amount=btc_amount)
            db.add_new_order_id(exchange, order_id=order_id)
            new_orders.add(order_id)
        db.set_last_known_tickers(exchange, now_tickers)

        # handle buy orders
        db_orders = exchange.get_active_order_ids()
        sell_order = db.get_sell_order_ids(exchange)
        for order_id in db.get_buy_order_ids(exchange):
            if order_id in db_orders:
                logger.info(f" - Buy order #{order_id} still waiting")
            else:
                sell_order_id = exchange.sell_tokens_from_order(order_id=order_id, profit=profit)
                logger.info(f" + Buy order #{order_id} is done, created pair-order {sell_order_id}!")
                db.remove_order_id(exchange, order_id=order_id)
                db.add_sell_order_id(exchange, sell_order_id)

        # handle sell orders
        db_orders = exchange.get_active_order_ids()
        for order_id in sell_order:
            if order_id in db_orders:
                logger.info(f" - Sell order #{order_id} still waiting")
            else:
                logger.info(f" + Sell order #{order_id} is done!")
                db.remove_sell_order_id(exchange, order_id=order_id)
