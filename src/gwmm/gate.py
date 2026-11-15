"""The slot gate: when to fetch, when to publish, and what price.

Pure clock logic with no broker and no HTTP, so the top-of-hour behavior
is testable on a fake clock. The maker owns the side effects and hands
them in as callables.

Each slot is one hour on the wall clock, and its wholesale price is the
5-minute LMP of the slot's first interval, the one that begins as the
slot opens. ISO-NE posts an interval's price about 25 s after it
begins, so from the top of the hour the gate asks ISO-NE for its current
interval on every tick until the answer is the slot's own, then
publishes the slot's price: that interval's parts plus the delivery
price for the hour. A maker that boots mid-slot publishes nothing for
that slot. When fetch_deadline_s pass with no price for the slot, the
gate publishes the last wholesale parts it published and raises a
critical glitch, so the houses still clear and someone is paged. With no
price ever published it can only raise the glitch.
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


class FiveMinuteLmp(NamedTuple):
    """One 5-minute interval's locational marginal price at one node: the
    interval's start (unix seconds; the utc.seconds format is outside this
    snapshot's closure) and the LMP in its parts. Interior to the fetch;
    latest.price is the boundary form."""

    begin_s: int
    lmp: WholesaleLmp


class SlotPrice(NamedTuple):
    """The price the maker publishes for one slot: the slot's start, the
    LMP of its first interval in its parts and the delivery price for the
    hour, times 1000 in USD/MWh. The start is unix seconds (the
    utc.seconds format is outside this snapshot's closure). Interior
    record; latest.price is the boundary form."""

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
    """Drives the fetches and the one publish per slot from repeated `tick` calls."""

    def __init__(
        self,
        *,
        fetch_lmp: Callable[[], FiveMinuteLmp],
        publish: Callable[[SlotPrice], None],
        raise_glitch: Callable[[str, str], None],
        fetch_deadline_s: int,
    ) -> None:
        self.fetch_lmp = fetch_lmp
        self.publish = publish
        self.raise_glitch = raise_glitch
        self.fetch_deadline_s = fetch_deadline_s
        self.current_slot: int | None = None
        self.pending_slot: int | None = None
        self.fetch_error: str | None = None
        self.last_published: SlotPrice | None = None

    def tick(self, now_s: int) -> None:
        current = slot_start(now_s)
        if self.current_slot is None:
            # Boot: the open slot is already cleared or missed; the first
            # price is for the next slot.
            self.current_slot = current
            return
        if self.current_slot != current:
            self.current_slot = current
            self.pending_slot = current
            self.fetch_error = None
        if self.pending_slot is None:
            return
        if self.fetch_for(self.pending_slot):
            return
        if now_s >= self.pending_slot + self.fetch_deadline_s:
            self.publish_stale(self.pending_slot)

    def fetch_for(self, slot_start_s: int) -> bool:
        """One ask of ISO-NE for the slot's first interval; True when the
        slot's price went out on it."""
        try:
            interval = self.fetch_lmp()
        except Exception as e:  # noqa: BLE001 -- any fetch failure is one case
            self.fetch_error = f"{type(e).__name__}: {e}"
            return False
        if interval.begin_s != slot_start_s:
            self.fetch_error = (
                f"ISO-NE's latest posted interval begins at {interval.begin_s}"
            )
            return False
        self.publish_for(
            SlotPrice(slot_start_s, interval.lmp, delivery_x1000(slot_start_s))
        )
        return True

    def publish_stale(self, slot_start_s: int) -> None:
        self.pending_slot = None
        if self.last_published is None:
            self.raise_glitch(
                "no price to publish",
                f"no price for slot {slot_start_s} within {self.fetch_deadline_s} s "
                f"({self.fetch_error}) and nothing published before",
            )
            return
        self.raise_glitch(
            "stale price published",
            f"no price for slot {slot_start_s} within {self.fetch_deadline_s} s "
            f"({self.fetch_error}); published the LMP from slot "
            f"{self.last_published.slot_start_s}",
        )
        self.publish_for(
            SlotPrice(
                slot_start_s, self.last_published.lmp, delivery_x1000(slot_start_s)
            )
        )

    def publish_for(self, price: SlotPrice) -> None:
        self.pending_slot = None
        self.publish(price)
        self.last_published = price
