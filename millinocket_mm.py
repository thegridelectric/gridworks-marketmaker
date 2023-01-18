import logging
import time

import gridworks.dev_utils.algo_setup as algo_setup

from gwmm.market_maker import MarketMaker


screen_handler = logging.StreamHandler()
fmt = "%(filename)s  %(message)s"
screen_handler.setFormatter(logging.Formatter(fmt=fmt))
logging.getLogger().addHandler(screen_handler)

time.sleep(2)
mm = MarketMaker()
algo_setup.dev_fund_to_min(addr=mm.acct.addr, min_algos=3)
mm.start()
