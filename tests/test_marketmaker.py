import time

import gwmm.config as config
from gwmm.market_maker_base import MarketMakerBase
from gwmm.types import HeartbeatA_Maker
from tests.utils import MarketMakerStubRecorder
from tests.utils import SupervisorStubRecorder
from tests.utils import wait_for


# Removing until starting up the Api happens in CI
# def test_market_maker():
#     mm = MarketMakerStubRecorder(settings=config.MarketMakerSettings())
#     su = SupervisorStubRecorder(settings=config.SupervisorSettings())
#     mm.start()
#     su.start()
#     wait_for(
#         lambda: mm._consume_connection, 2, "marketmaker. _consume_connection exists"
#     )
#     wait_for(lambda: mm._consuming, 2, "marketmaker is consuming")
#     wait_for(
#         lambda: mm._publish_connection.is_open,
#         2,
#         "marketmaker. publish connection is open",
#     )
#     wait_for(lambda: su._consume_connection, 2, "supervisor _consume_connection exists")

#     assert su.messages_received == 0
#     assert su.messages_routed_internally == 0

#     mm.send_heartbeat_to_super()

#     wait_for(
#         lambda: su.messages_received == 1,
#         2,
#         f"su.messages_received is {su.messages_received}",
#     )
#     assert su.messages_routed_internally == 1

#     mm.stop()
#     su.stop()
