from typing import Set
from decimal import Decimal


class BaseExchangeInterface:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def get_now_btc_tickers(self) -> Set[str]:
        raise NotImplementedError

    def buy_tickets(self, ticker: str, btc_amount: Decimal) -> str:
        raise NotImplementedError

    def get_active_order_ids(self) -> Set[str]:
        raise NotImplementedError

    def sell_tokens_from_order(self, order_id: str, profit: Decimal) -> str:
        raise NotImplementedError
