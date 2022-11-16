""" MarketMakerBase """
import functools
import logging
import traceback
from abc import abstractmethod
from datetime import datetime
from typing import Optional
from typing import no_type_check

import pendulum

from gwmm.actor_base import ActorBase
from gwmm.config import Settings
from gwmm.enums import GNodeRole
from gwmm.enums import MessageCategorySymbol
from gwmm.schemata import Bid
from gwmm.schemata import Bid_Maker
from gwmm.schemata import HeartbeatA
from gwmm.schemata import HeartbeatA_Maker
from gwmm.schemata import LatestPrice_Maker
from gwmm.schemata import SimTimestep
from gwmm.schemata import SimTimestep_Maker


LOG_FORMAT = (
    "%(levelname) -10s %(sasctime)s %(name) -30s %(funcName) "
    "-35s %(lineno) -5d: %(message)s"
)
LOGGER = logging.getLogger(__name__)


class MarketMakerBase(ActorBase):
    def __init__(self, settings: Settings):
        super().__init__(settings=settings)
        self.latest_time_unix_s: int = 0
        LOGGER.setLevel(self.logging_level)

    def additional_rabbit_stuff_after_rabbit_base_setup_is_done(self):
        rjb = MessageCategorySymbol.rjb.value
        tc_alias_lrh = self.settings.my_time_coordinator_alias.replace(".", "-")
        binding = f"{rjb}.{tc_alias_lrh}.timecoordinator.sim-timestep"

        cb = functools.partial(self.on_timecoordinator_bindok, binding=binding)
        self._consume_channel.queue_bind(
            self.queue_name, "timecoordinatormic_tx", routing_key=binding, callback=cb
        )

    @no_type_check
    def on_timecoordinator_bindok(self, _unused_frame, binding) -> None:
        LOGGER.info(f"Queue {self.queue_name} bound with {binding}")

    def prepare_for_death(self) -> None:
        self.actor_main_stopped = True

    ########################
    ## Receives
    ########################

    def route_message(
        self, from_alias: str, from_role: GNodeRole, payload: HeartbeatA
    ) -> None:
        if payload.TypeName == SimTimestep_Maker.type_name:
            try:
                self.timestep_from_timecoordinator(payload)
            except:
                LOGGER.warning("Error in timestep_from_timecoordinator")
                LOGGER.warning(traceback.format_exc(True))

    def timestep_from_timecoordinator(self, payload: SimTimestep):
        if self.latest_time_unix_s == 0:
            self.latest_time_unix_s = payload.TimeUnixS
            self.new_timestep(payload)
            LOGGER.info(f"TIME STARTED: {self.time_utc_str}")
        elif self.latest_time_unix_s < payload.TimeUnixS:
            self.latest_time_unix_s = payload.TimeUnixS
            self.new_timestep(payload)
            LOGGER.debug(f"Time is now {self.time_utc_str}")
        elif self.latest_time_unix_s == payload.TimeUnixS:
            self.timestep_received_again(payload)

    @abstractmethod
    def new_timestep(self, payload: SimTimestep) -> None:
        # LOGGER.info("New timestep in atn_actor_base")
        raise NotImplementedError

    @abstractmethod
    def timestep_received_again(self, payload: SimTimestep) -> None:
        # LOGGER.info("Timestep received again in atn_actor_base")
        raise NotImplementedError

    @no_type_check
    def send_heartbeat_to_super(self) -> None:
        self.send_message(
            payload=HeartbeatA_Maker().tuple,
            to_role=GNodeRole.Supervisor,
            to_g_node_alias=self.settings.my_super_alias,
        )

    @property
    def time_utc_str(self) -> str:
        if self.latest_time_unix_s is None:
            return ""
        return pendulum.from_timestamp(self.latest_time_unix_s).strftime(
            "%m/%d/%Y, %H:%M"
        )
