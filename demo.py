import logging
import time

from gwmm.market_maker import MarketMaker


screen_handler = logging.StreamHandler()
fmt = "%(filename)s  %(message)s"
screen_handler.setFormatter(logging.Formatter(fmt=fmt))
logging.getLogger().addHandler(screen_handler)
mm = MarketMaker()
mm.start()
