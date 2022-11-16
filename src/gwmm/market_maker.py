"""MarketMaker"""
import logging
import pendulum
import dotenv
from gwmm.schemata import SimTimestep
import gwmm.config as config
from gwmm.market_maker_base import MarketMakerBase
from gwmm.schemata import LatestPrice_Maker
from gwmm.config import Settings

LOG_FORMAT = (
    "%(levelname) -10s %(sasctime)s %(name) -30s %(funcName) "
    "-35s %(lineno) -5d: %(message)s"
)
LOGGER = logging.getLogger(__name__)


class MarketMaker(MarketMakerBase):
    def __init__(
        self, 
        settings: config.Settings = config.Settings(
            _env_file=dotenv.find_dotenv()
        ),
    ):
        super().__init__(settings=settings)

    def new_timestep(self, payload: SimTimestep) -> None:
        LOGGER.info(f"Got timestep. Time is now {self.time_utc_str}")
        # send latest market price

    def timestep_received_again(self, payload: SimTimestep) -> None:
        LOGGER.info("Received timestep again")