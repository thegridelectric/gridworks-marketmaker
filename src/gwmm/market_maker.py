"""The MarketMaker actor: publishes latest.price at the top of every hour.

A gwbase GridworksActor with the MarketMaker transport class. Its one
publication is the broadcast

    rjb.<maker-alias-lrh>.mm.latest-price

whose body is the latest.price word for the slot that just opened. Bids
addressed to the maker are received and dropped; the ack that makes a
bid a contract is the full maker's job.
"""

import json
import threading
import time
import uuid
from collections.abc import Callable

from gwbase.gridworks_actor import GridworksActor
from gwbase.sema.types.gridworks_header import GridworksHeader
from gwbase.transport_encoding import RoutingEnvelope, TransportClass

from gwmm.config import GwmmSettings
from gwmm.gate import SlotGate, SlotPrice
from gwmm.isone import IsoneClient
from gwmm.sema.enums import LogLevel, MarketPriceUnit
from gwmm.sema.types import Glitch, LatestPrice

TICK_S = 1
GLITCH_NODE = "gate"


def market_slot_name(product: str, maker_alias: str, slot_start_s: int) -> str:
    """`e.<product>.<maker alias>.<slot start>` (format market.slot.name)."""
    return f"e.{product}.{maker_alias}.{slot_start_s}"


class MarketMaker(GridworksActor):
    """Publishes the cleared price for its one market, every hour."""

    def __init__(
        self,
        settings: GwmmSettings,
        *,
        fetch_lmp: Callable[[], float] | None = None,
    ) -> None:
        super().__init__(
            settings=settings,
            transport_class=TransportClass.MarketMaker,
            my_super_alias=settings.my_super_alias,
            my_time_coordinator_alias=settings.my_time_coordinator_alias,
        )
        self.market_product: str = settings.market_product
        if fetch_lmp is None:
            client = IsoneClient(
                settings.isone_user,
                settings.isone_api_pass.get_secret_value(),
                settings.isone_location_id,
            )
            fetch_lmp = lambda: client.current().lmp_usd_per_mwh
        self.gate = SlotGate(
            fetch_lmp=fetch_lmp,
            publish=self.publish_price,
            raise_glitch=self.raise_glitch,
            fetch_lead_s=settings.fetch_lead_s,
        )
        self.main_thread = threading.Thread(target=self.main, daemon=True)

    def local_start(self) -> None:
        self._main_loop_running = True
        self.main_thread.start()

    def local_stop(self) -> None:
        self._main_loop_running = False
        self.main_thread.join()

    def process_message(
        self,
        *,
        envelope: RoutingEnvelope,
        body: bytes,
        header: GridworksHeader | None,
    ) -> None:
        self.logger.info(
            "dropped %s from %s: the stopgap maker answers nothing",
            envelope.type_name,
            envelope.from_alias,
        )

    def main(self) -> None:
        while self._main_loop_running:
            try:
                self.gate.tick(int(time.time()))
            except Exception:
                self.logger.exception("gate tick failed")
            time.sleep(TICK_S)

    def latest_price(self, price: SlotPrice) -> LatestPrice:
        return LatestPrice(
            from_g_node_alias=self.alias,
            price_times1000=round(price.energy_usd_per_mwh * 1000),
            price_unit=MarketPriceUnit.USDPerMWh,
            market_slot_name=market_slot_name(
                self.market_product, self.alias, price.slot_start_s
            ),
            message_id=str(uuid.uuid4()),
        )

    def publish_price(self, price: SlotPrice) -> None:
        word = self.latest_price(price)
        envelope = self.broadcast_envelope(type_name=word.type_name)
        self.send(envelope=envelope, body=json.dumps(word.to_dict()).encode("utf-8"))
        self.logger.info(
            "published %s: lmp %.2f + delivery %.2f = %.2f USD/MWh",
            word.market_slot_name,
            price.lmp_usd_per_mwh,
            price.delivery_usd_per_mwh,
            price.energy_usd_per_mwh,
        )

    def raise_glitch(self, summary: str, details: str) -> None:
        glitch = Glitch(
            from_g_node_alias=self.alias,
            node=GLITCH_NODE,
            type=LogLevel.Critical,
            summary=summary,
            details=details,
            created_ms=int(time.time() * 1000),
        )
        envelope = self.broadcast_envelope(type_name=glitch.type_name)
        self.send(envelope=envelope, body=json.dumps(glitch.to_dict()).encode("utf-8"))
        self.logger.critical("glitch: %s: %s", summary, details)
