from typing import List

import settings
from cryptotrader.iexchanges import (
    abc,
    bittrex
)

EXCHANGES: List[abc.BaseExchangeInterface] = [
    bittrex.Bittrex(**settings.BITTREX)
]
