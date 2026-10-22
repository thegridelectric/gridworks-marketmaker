"""gwmm console entry point: `gwmm {rabbit,show}`.

`rabbit` runs the maker (the systemd unit `mm-rabbit.service`). `show`
prints the price the maker would publish for the open slot right now,
with no broker, for a check from a shell.
"""

from __future__ import annotations

import argparse
import time
from datetime import datetime

import dotenv

from gwmm.config import GwmmSettings
from gwmm.gate import SlotPrice, slot_start
from gwmm.isone import IsoneClient
from gwmm.market_maker import MarketMaker, market_slot_name
from gwmm.tariff import TARIFF_TZ, delivery_usd_per_mwh


def load_settings() -> GwmmSettings:
    """Settings from the environment; the ISO-NE account has no default."""
    return GwmmSettings()  # type: ignore[call-arg]


def run_rabbit() -> None:
    actor = MarketMaker(load_settings())
    actor.start()
    try:
        while actor.main_loop_running:
            time.sleep(1)
    except KeyboardInterrupt:
        actor.stop()


def run_show() -> None:
    settings = load_settings()
    client = IsoneClient(
        settings.isone_user,
        settings.isone_api_pass.get_secret_value(),
        settings.isone_location_id,
    )
    interval = client.current()
    start = slot_start(int(time.time()))
    price = SlotPrice(start, interval.lmp_usd_per_mwh, delivery_usd_per_mwh(start))
    local = datetime.fromtimestamp(start, TARIFF_TZ)
    print(market_slot_name(settings.market_product, settings.service_alias, start))
    print(f"slot {local:%Y-%m-%d %H:%M %Z}")
    print(
        f"lmp {price.lmp_usd_per_mwh:.2f} (interval "
        f"{datetime.fromtimestamp(interval.begin_s, TARIFF_TZ):%H:%M}) "
        f"+ delivery {price.delivery_usd_per_mwh:.2f} "
        f"= {price.energy_usd_per_mwh:.2f} USD/MWh"
    )


def main(argv: list[str] | None = None) -> None:
    dotenv.load_dotenv(dotenv.find_dotenv())  # populate env BEFORE Settings()
    parser = argparse.ArgumentParser(prog="gwmm")
    subcommands = parser.add_subparsers(dest="command", required=True)
    subcommands.add_parser("rabbit", help="run the maker")
    subcommands.add_parser("show", help="print the price for the open slot now")
    args = parser.parse_args(argv)
    {"rabbit": run_rabbit, "show": run_show}[args.command]()
