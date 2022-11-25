import logging
import time

import dotenv

import gwmm.config as config
import gwmm.dev_utils.algo_setup as algo_setup
from gwmm.algo_utils import BasicAccount
from gwmm.market_maker import MarketMaker


screen_handler = logging.StreamHandler()
fmt = "%(filename)s  %(message)s"
screen_handler.setFormatter(logging.Formatter(fmt=fmt))
logging.getLogger().addHandler(screen_handler)


# Fund MarketMaker account with seed
settings: config.Settings = config.Settings(_env_file=dotenv.find_dotenv())
addr = BasicAccount(settings.sk.get_secret_value()).addr

# algo_setup.dev_fund_account(
#         settings=settings,
#         to_addr=addr,
#         amt_in_micros=10**6,
#     )


mm = MarketMaker()
mm.start()
