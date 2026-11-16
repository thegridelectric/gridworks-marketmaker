"""The maker on a real broker: one publish, heard on its mic exchange
as `rjb.<alias>.mm.latest-price` with a valid latest.price body.

Needs a broker at `GWMM_TEST_RABBIT_URL` (the dev broker's `d1__1`
vhost); self-skips without one.
"""

from __future__ import annotations

import json
import os
import threading
import time
from pathlib import Path

import pika
import pytest
from gwbase.config.rabbit_settings import RabbitBrokerClient
from pydantic import SecretStr

from gwmm.config import GwmmSettings
from gwmm.gate import SLOT_S, FiveMinuteLmp, SlotPrice, WholesaleLmp, slot_start
from gwmm.market_maker import MarketMaker, market_slot_name, price_components
from gwmm.sema.codec import default_codec
from gwmm.sema.enums import PriceComponentName, PriceStage
from gwmm.sema.types import LatestPrice
from gwmm.tariff import TARIFF_ALIAS

DEV_IDENTITY = Path(__file__).resolve().parents[1] / "scripts" / "dev-g.node.gt.json"


def test_market_slot_name_is_well_formed() -> None:
    name = market_slot_name("rt60gate5", "d1.isone.me.versant.keene", 1792335600)
    assert name == "e.rt60gate5.d1.isone.me.versant.keene.1792335600"


def test_components_are_the_lmp_parts_and_delivery() -> None:
    price = SlotPrice(
        1792335600, WholesaleLmp(32_120, 40, -820), 58_556, PriceStage.Final
    )
    parts = price_components(price)
    assert [c.name for c in parts] == [
        PriceComponentName.WholesaleEnergy,
        PriceComponentName.WholesaleCongestion,
        PriceComponentName.WholesaleLoss,
        PriceComponentName.Delivery,
    ]
    assert sum(c.price_x1000 for c in parts) == price.price_x1000 == 89_896


@pytest.mark.integration
def test_publish_is_heard_on_the_mic_exchange() -> None:
    url = os.environ.get("GWMM_TEST_RABBIT_URL")
    if not url:
        pytest.skip("no GWMM_TEST_RABBIT_URL")
    settings = GwmmSettings(
        rabbit=RabbitBrokerClient(url=SecretStr(url)),
        g_node_path=DEV_IDENTITY,
        isone_user="unused",
        isone_api_pass=SecretStr("unused"),
    )
    heard: list[tuple[str, bytes]] = []
    ready = threading.Event()

    def listen() -> None:
        conn = pika.BlockingConnection(pika.URLParameters(url))
        ch = conn.channel()
        q = ch.queue_declare("", exclusive=True).method.queue
        ch.queue_bind(q, "mmmic_tx", "rjb.#")
        ready.set()
        for method, _props, body in ch.consume(q, inactivity_timeout=15):
            if method is None:
                break
            heard.append((str(method.routing_key), bytes(body or b"")))
            break
        conn.close()

    listener = threading.Thread(target=listen, daemon=True)
    listener.start()
    assert ready.wait(10)

    maker = MarketMaker(
        settings, fetch_lmp=lambda: FiveMinuteLmp(0, WholesaleLmp(30_000, 0, 0))
    )
    maker.start()
    try:
        deadline = time.time() + 15
        while not maker.consuming and time.time() < deadline:
            time.sleep(0.1)
        assert maker.consuming
        start = slot_start(int(time.time()))
        maker.publish_price(
            SlotPrice(start, WholesaleLmp(30_000, 250, -400), 58_556, PriceStage.Final)
        )
        listener.join(20)
    finally:
        maker.stop()

    assert heard, "nothing heard on mmmic_tx rjb.#"
    key, body = heard[0]
    assert key == "rjb.d1-isone-me-versant-keene.mm.latest-price"
    word = default_codec.from_dict(json.loads(body))
    assert isinstance(word, LatestPrice)
    assert word.from_g_node_alias == "d1.isone.me.versant.keene"
    assert word.price_x1000 == 30_000 + 250 - 400 + 58_556
    assert sum(c.price_x1000 for c in word.components) == word.price_x1000
    assert word.tariff_alias == TARIFF_ALIAS
    assert word.price_stage == PriceStage.Final
    assert word.market_slot_name.endswith(f".{start}")
    assert int(word.market_slot_name.rsplit(".", 1)[1]) % SLOT_S == 0
