""" MarketMakerBase """
import functools
import logging
import time
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
from gwmm.enums import UniverseType
from gwmm.schemata import HeartbeatA
from gwmm.schemata import HeartbeatA_Maker
from gwmm.schemata import LatestPrice_Maker
from gwmm.schemata import SimTimestep
from gwmm.schemata import SimTimestep_Maker
from gwmm.utils import RestfulResponse


LOG_FORMAT = (
    "%(levelname) -10s %(sasctime)s %(name) -30s %(funcName) "
    "-35s %(lineno) -5d: %(message)s"
)
LOGGER = logging.getLogger(__name__)

LOGGER.setLevel(logging.INFO)


class MarketMakerBase(ActorBase):
    def __init__(self, settings: Settings):
        super().__init__(settings=settings)
        self._time: float = 0

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
        if self._time == 0:
            self._time = float(payload.TimeUnixS)
            self.new_timestep(payload)
            LOGGER.info(f"TIME STARTED: {self.time_utc_str()}")
        elif self._time < payload.TimeUnixS:
            self._time = float(payload.TimeUnixS)
            self.new_timestep(payload)
        elif self._time == float(payload.TimeUnixS):
            self.repeated_timestep(payload)

    def new_timestep(self, payload: SimTimestep) -> None:
        # LOGGER.info("New timestep in atn_actor_base")
        raise NotImplementedError

    def repeated_timestep(self, payload: SimTimestep) -> None:
        # LOGGER.info("Timestep received again in atn_actor_base")
        raise NotImplementedError

    def send_heartbeat_to_super(self) -> None:
        self.send_message(
            payload=HeartbeatA_Maker().tuple,
            to_role=GNodeRole.Supervisor,
            to_g_node_alias=self.settings.my_super_alias,
        )

    def time(self) -> float:
        if self.universe_type == UniverseType.Dev:
            return self._time
        else:
            return time.time()

    def time_utc_str(self) -> str:
        return pendulum.from_timestamp(self._time).strftime("%m/%d/%Y, %H:%M")
