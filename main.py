from cryptotrader.cli import main

import logging
import sys

root = logging.getLogger()
root.setLevel(logging.INFO)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '%(levelname)s [%(asctime)s] %(name)s : %(message)s'
)
ch.setFormatter(formatter)
root.addHandler(ch)


main()
