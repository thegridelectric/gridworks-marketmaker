"""The slot gate on a fake clock: the Provisional at the top of the hour
from the last wholesale parts, asks on every tick until ISO-NE posts the
slot's first interval, the Final on it, the Final at the provisional
value with a glitch at the deadline, nothing to publish on a cold
failure."""

from gwmm.gate import (
    SLOT_S,
    FiveMinuteLmp,
    SlotGate,
    SlotPrice,
    WholesaleLmp,
    next_slot_start,
    slot_start,
)
from gwmm.sema.enums import PriceStage
from gwmm.tariff import delivery_x1000

LMP = WholesaleLmp(energy_x1000=30_000, congestion_x1000=250, loss_x1000=-400)
NEWER = WholesaleLmp(energy_x1000=31_000, congestion_x1000=0, loss_x1000=0)

HOUR = 1_770_000_000 - 1_770_000_000 % SLOT_S  # some top of an hour
DEADLINE_S = 240


class Isone:
    """A fake ISO-NE: posts the interval beginning at `posted_begin_s`
    (the previous one until then) at `lmp`, or is down."""

    def __init__(self) -> None:
        self.posted_begin_s: int | None = None
        self.lmp = LMP
        self.down = False
        self.fetches = 0
        self.published: list[SlotPrice] = []
        self.glitches: list[tuple[str, str]] = []

    def post(self, begin_s: int, lmp: WholesaleLmp = LMP) -> None:
        self.posted_begin_s = begin_s
        self.lmp = lmp

    def fetch(self) -> FiveMinuteLmp:
        self.fetches += 1
        if self.down or self.posted_begin_s is None:
            raise ConnectionError("iso-ne down")
        return FiveMinuteLmp(self.posted_begin_s, self.lmp)

    def gate(self) -> SlotGate:
        return SlotGate(
            fetch_lmp=self.fetch,
            publish=self.published.append,
            raise_glitch=lambda s, d: self.glitches.append((s, d)),
            fetch_deadline_s=DEADLINE_S,
        )

    def stages(self) -> list[tuple[int, PriceStage]]:
        return [(p.slot_start_s, p.stage) for p in self.published]


def warm(iso: Isone) -> SlotGate:
    """A gate that booted in the slot before HOUR."""
    g = iso.gate()
    g.tick(HOUR - 600)
    return g


def settled(iso: Isone) -> SlotGate:
    """A warm gate that published HOUR's Final on LMP, so the next slot has
    a provisional value."""
    g = warm(iso)
    iso.post(HOUR)
    g.tick(HOUR)
    assert iso.stages() == [(HOUR, PriceStage.Final)]
    return g


def test_slot_arithmetic() -> None:
    assert slot_start(HOUR + 1234) == HOUR
    assert next_slot_start(HOUR + 1234) == HOUR + SLOT_S
    assert next_slot_start(HOUR) == HOUR + SLOT_S


def test_boot_mid_slot_publishes_nothing() -> None:
    iso = Isone()
    iso.post(HOUR - 300)
    g = iso.gate()
    g.tick(HOUR - 600)
    g.tick(HOUR - 1)
    assert iso.fetches == 0
    assert iso.published == []
    assert iso.glitches == []


def test_first_slot_after_boot_has_no_provisional() -> None:
    iso = Isone()
    iso.post(HOUR - 300)
    g = warm(iso)
    g.tick(HOUR)
    assert iso.published == []
    iso.post(HOUR)
    g.tick(HOUR + 25)
    assert iso.stages() == [(HOUR, PriceStage.Final)]


def test_provisional_at_the_top_of_the_hour_is_the_last_parts_plus_this_hours_delivery() -> (
    None
):
    iso = Isone()
    g = settled(iso)
    g.tick(HOUR + SLOT_S)  # the slot opens: the Provisional, with no fetch needed
    assert iso.stages() == [
        (HOUR, PriceStage.Final),
        (HOUR + SLOT_S, PriceStage.Provisional),
    ]
    p = iso.published[1]
    assert p.lmp == LMP
    assert p.delivery_x1000 == delivery_x1000(HOUR + SLOT_S)
    assert p.price_x1000 == LMP.total_x1000 + delivery_x1000(HOUR + SLOT_S)


def test_asks_every_tick_from_the_top_of_the_hour_until_the_slot_interval_is_posted() -> (
    None
):
    iso = Isone()
    g = settled(iso)
    second = HOUR + SLOT_S
    g.tick(second - 1)  # before the slot: nothing
    assert iso.fetches == 1
    g.tick(second)  # the slot opens: an ask, ISO-NE still on the old interval
    g.tick(second + 1)
    g.tick(second + 2)
    assert iso.fetches == 4
    assert iso.stages() == [(HOUR, PriceStage.Final), (second, PriceStage.Provisional)]
    iso.post(second, NEWER)  # ISO-NE posts the slot's first interval
    g.tick(second + 3)  # the ask that finds it: the Final
    assert iso.stages()[-1] == (second, PriceStage.Final)
    assert iso.published[-1].lmp == NEWER
    g.tick(second + 4)  # no more asks or publishes this slot
    g.tick(second + 1800)
    assert iso.fetches == 5
    assert len(iso.published) == 3
    assert iso.glitches == []


def test_final_is_the_interval_parts_plus_delivery() -> None:
    iso = Isone()
    g = warm(iso)
    iso.post(HOUR)
    g.tick(HOUR)
    p = iso.published[0]
    assert p.stage == PriceStage.Final
    assert p.lmp == LMP
    assert p.price_x1000 == 30_000 + 250 - 400 + p.delivery_x1000


def test_next_provisional_takes_the_last_final_parts() -> None:
    iso = Isone()
    g = settled(iso)
    second = HOUR + SLOT_S
    iso.post(second, NEWER)
    g.tick(second)
    g.tick(second + SLOT_S)
    assert iso.stages()[-1] == (second + SLOT_S, PriceStage.Provisional)
    assert iso.published[-1].lmp == NEWER


def test_deadline_publishes_the_final_at_the_provisional_value_and_glitches() -> None:
    iso = Isone()
    g = settled(iso)
    second = HOUR + SLOT_S
    iso.down = True
    for t in range(second, second + DEADLINE_S):
        g.tick(t)
    assert iso.stages() == [(HOUR, PriceStage.Final), (second, PriceStage.Provisional)]
    g.tick(second + DEADLINE_S)
    assert iso.stages()[-1] == (second, PriceStage.Final)
    assert iso.published[-1].lmp == iso.published[-2].lmp == LMP
    assert iso.published[-1].price_x1000 == iso.published[-2].price_x1000
    assert len(iso.glitches) == 1
    assert iso.glitches[0][0] == "final at the provisional value"
    assert "ConnectionError" in iso.glitches[0][1]
    g.tick(second + DEADLINE_S + 1)  # the slot is done
    assert len(iso.published) == 3


def test_deadline_with_iso_stuck_on_the_old_interval() -> None:
    iso = Isone()
    g = settled(iso)
    second = HOUR + SLOT_S
    iso.post(second - 300)  # never posts the next slot's interval
    for t in range(second, second + DEADLINE_S + 1):
        g.tick(t)
    assert iso.stages()[-2:] == [
        (second, PriceStage.Provisional),
        (second, PriceStage.Final),
    ]
    assert iso.glitches[0][0] == "final at the provisional value"
    assert str(second - 300) in iso.glitches[0][1]


def test_cold_failure_publishes_nothing_and_glitches() -> None:
    iso = Isone()
    iso.down = True
    g = warm(iso)
    for t in range(HOUR, HOUR + DEADLINE_S + 1):
        g.tick(t)
    assert iso.published == []
    assert [s for s, _ in iso.glitches] == ["no price to publish"]
    # the next slot with ISO-NE back has no provisional and a fresh Final, no glitch
    iso.down = False
    iso.post(HOUR + SLOT_S)
    g.tick(HOUR + SLOT_S)
    assert iso.stages() == [(HOUR + SLOT_S, PriceStage.Final)]
    assert len(iso.glitches) == 1
