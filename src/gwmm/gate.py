"""The slot gate: when to publish, at which stage, and what price.

Pure clock logic with no broker and no HTTP, so the top-of-hour behavior
is testable on a fake clock. The maker owns the side effects and hands
them in as callables.

Each slot is one hour on the wall clock, and the maker states its price
twice. At the top of the hour it publishes the Provisional price: the
last wholesale parts it published, which are the previous slot's first
interval, plus the delivery price for this hour, both in hand with no
fetch. The slot's wholesale price is the 5-minute LMP of its first
interval, the one that begins as the slot opens. ISO-NE posts an
interval's price about 25 s after it begins, so from the top of the hour
the gate asks ISO-NE for its current interval on every tick until the
answer is the slot's own, then publishes the Final price: that
interval's parts plus the delivery price for the hour. When
fetch_deadline_s pass with no answer, the gate publishes the Final at
the provisional value and raises a critical glitch, so the contract
binds and someone is paged. A maker that boots mid-slot publishes
nothing for that slot, and with nothing published before it has no
provisional to state: its first slot gets a Final alone, or the glitch.
"""

from collections.abc import Callable
from typing import NamedTuple

from gwmm.sema.enums import PriceStage
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
    """The price the maker publishes for one slot at one stage: the slot's
    start, the wholesale LMP in its parts, the delivery price for the
    hour, times 1000 in USD/MWh, and the stage of the maker's commitment.
    The start is unix seconds (the utc.seconds format is outside this
    snapshot's closure). Interior record; latest.price is the boundary
    form."""

    slot_start_s: int
    lmp: WholesaleLmp
    delivery_x1000: int
    stage: PriceStage

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
    """Drives the publishes of each slot, provisional then final, from
    repeated `tick` calls."""

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
        self.last_lmp: WholesaleLmp | None = None

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
            self.publish_provisional(current)
        if self.pending_slot is None:
            return
        if self.fetch_for(self.pending_slot):
            return
        if now_s >= self.pending_slot + self.fetch_deadline_s:
            self.publish_at_deadline(self.pending_slot)

    def publish_provisional(self, slot_start_s: int) -> None:
        """The slot's Provisional price at its open, from the last
        wholesale parts published; nothing when there are none."""
        if self.last_lmp is None:
            return
        self.publish(
            SlotPrice(
                slot_start_s,
                self.last_lmp,
                delivery_x1000(slot_start_s),
                PriceStage.Provisional,
            )
        )

    def fetch_for(self, slot_start_s: int) -> bool:
        """One ask of ISO-NE for the slot's first interval; True when the
        slot's Final went out on it."""
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
        self.publish_final(slot_start_s, interval.lmp)
        return True

    def publish_at_deadline(self, slot_start_s: int) -> None:
        """The deadline passed with no answer: the Final at the provisional
        value with a critical glitch, or the glitch alone when there is no
        provisional value."""
        self.pending_slot = None
        if self.last_lmp is None:
            self.raise_glitch(
                "no price to publish",
                f"no price for slot {slot_start_s} within {self.fetch_deadline_s} s "
                f"({self.fetch_error}) and nothing published before",
            )
            return
        self.raise_glitch(
            "final at the provisional value",
            f"no ISO-NE price for slot {slot_start_s} within "
            f"{self.fetch_deadline_s} s ({self.fetch_error}); the Final is the "
            f"provisional value",
        )
        self.publish_final(slot_start_s, self.last_lmp)

    def publish_final(self, slot_start_s: int, lmp: WholesaleLmp) -> None:
        self.pending_slot = None
        self.publish(
            SlotPrice(slot_start_s, lmp, delivery_x1000(slot_start_s), PriceStage.Final)
        )
        self.last_lmp = lmp
