"""The slot gate: when to fetch, when to publish, and what price.

Pure clock logic with no broker and no HTTP, so the top-of-hour behavior
is testable on a fake clock. The maker owns the side effects and hands
them in as callables.

Each slot is one hour on the wall clock. A few seconds before the slot
opens the gate fetches the current 5-minute LMP in its parts; at the top
of the hour it publishes the slot's price: the wholesale parts plus the
delivery price for the hour. A maker that boots mid-slot publishes
nothing for that slot: an LTN clears against a price only at the top of
the hour, when its bid is in. When the fetch for a slot failed, the gate
publishes the last wholesale parts it published and raises a critical
glitch, so the houses still clear and someone is paged. With no price
ever published it can only raise the glitch.
"""

from collections.abc import Callable
from typing import NamedTuple

from gwmm.tariff import delivery_x1000

SLOT_S = 3600


class WholesaleLmp(NamedTuple):
    """One locational marginal price in its three parts, each times 1000
    in USD/MWh. Interior record; the parts become price.component
    instances in latest.price."""

    energy_x1000: int
    congestion_x1000: int
    loss_x1000: int

    @property
    def total_x1000(self) -> int:
        return self.energy_x1000 + self.congestion_x1000 + self.loss_x1000


class SlotPrice(NamedTuple):
    """The price the maker publishes for one slot: the slot's start, the
    LMP at the gate in its parts and the delivery price for the hour,
    times 1000 in USD/MWh. The start is unix seconds (the utc.seconds
    format is outside this snapshot's closure). Interior record;
    latest.price is the boundary form."""

    slot_start_s: int
    lmp: WholesaleLmp
    delivery_x1000: int

    @property
    def price_x1000(self) -> int:
        return self.lmp.total_x1000 + self.delivery_x1000


def slot_start(now_s: int) -> int:
    """The start of the slot containing `now_s`."""
    return now_s - now_s % SLOT_S


def next_slot_start(now_s: int) -> int:
    """The start of the slot after the one containing `now_s`."""
    return slot_start(now_s) + SLOT_S


class SlotGate:
    """Drives one fetch and one publish per slot from repeated `tick` calls."""

    def __init__(
        self,
        *,
        fetch_lmp: Callable[[], WholesaleLmp],
        publish: Callable[[SlotPrice], None],
        raise_glitch: Callable[[str, str], None],
        fetch_lead_s: int,
    ) -> None:
        self.fetch_lmp = fetch_lmp
        self.publish = publish
        self.raise_glitch = raise_glitch
        self.fetch_lead_s = fetch_lead_s
        self.fetched_slot: int | None = None
        self.fetched_lmp: WholesaleLmp | None = None
        self.fetch_error: str | None = None
        self.published_slot: int | None = None
        self.last_published: SlotPrice | None = None

    def tick(self, now_s: int) -> None:
        upcoming = next_slot_start(now_s)
        if now_s >= upcoming - self.fetch_lead_s and self.fetched_slot != upcoming:
            self.fetch_for(upcoming)
        current = slot_start(now_s)
        if self.published_slot is None:
            # Boot: the open slot is already cleared or missed; the first
            # publish is the next top of the hour.
            self.published_slot = current
        elif self.published_slot != current:
            self.publish_for(current)

    def fetch_for(self, slot_start_s: int) -> None:
        self.fetched_slot = slot_start_s
        try:
            self.fetched_lmp = self.fetch_lmp()
            self.fetch_error = None
        except Exception as e:  # noqa: BLE001 -- any fetch failure is one case
            self.fetched_lmp = None
            self.fetch_error = f"{type(e).__name__}: {e}"

    def publish_for(self, slot_start_s: int) -> None:
        self.published_slot = slot_start_s
        delivery = delivery_x1000(slot_start_s)
        if self.fetched_slot == slot_start_s and self.fetched_lmp is not None:
            price = SlotPrice(slot_start_s, self.fetched_lmp, delivery)
        elif self.last_published is not None:
            price = SlotPrice(slot_start_s, self.last_published.lmp, delivery)
            self.raise_glitch(
                "stale price published",
                f"no fresh LMP for slot {slot_start_s} ({self.fetch_error}); "
                f"published the LMP from slot {self.last_published.slot_start_s}",
            )
        else:
            self.raise_glitch(
                "no price to publish",
                f"no fresh LMP for slot {slot_start_s} ({self.fetch_error}) "
                "and nothing published before",
            )
            return
        self.publish(price)
        self.last_published = price
