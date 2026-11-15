"""The slot gate on a fake clock: ask on every tick from the top of the
hour until ISO-NE posts the slot's first interval, publish on it, stale
fallback with a glitch at the deadline, nothing to publish on a cold
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

LMP = WholesaleLmp(energy_x1000=30_000, congestion_x1000=250, loss_x1000=-400)
OLDER = WholesaleLmp(energy_x1000=29_000, congestion_x1000=0, loss_x1000=0)

HOUR = 1_770_000_000 - 1_770_000_000 % SLOT_S  # some top of an hour
DEADLINE_S = 240


class Isone:
    """A fake ISO-NE: posts the interval beginning at `posted_begin_s`
    (the previous one until then), or is down."""

    def __init__(self) -> None:
        self.posted_begin_s: int | None = None
        self.down = False
        self.fetches = 0
        self.published: list[SlotPrice] = []
        self.glitches: list[tuple[str, str]] = []

    def post(self, begin_s: int) -> None:
        self.posted_begin_s = begin_s

    def fetch(self) -> FiveMinuteLmp:
        self.fetches += 1
        if self.down or self.posted_begin_s is None:
            raise ConnectionError("iso-ne down")
        return FiveMinuteLmp(self.posted_begin_s, LMP)

    def gate(self) -> SlotGate:
        return SlotGate(
            fetch_lmp=self.fetch,
            publish=self.published.append,
            raise_glitch=lambda s, d: self.glitches.append((s, d)),
            fetch_deadline_s=DEADLINE_S,
        )


def warm(iso: Isone) -> SlotGate:
    """A gate that booted in the slot before HOUR."""
    g = iso.gate()
    g.tick(HOUR - 600)
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


def test_asks_every_tick_from_the_top_of_the_hour_until_the_slot_interval_is_posted() -> (
    None
):
    iso = Isone()
    iso.post(HOUR - 300)
    g = warm(iso)
    g.tick(HOUR - 1)  # before the slot: nothing
    assert iso.fetches == 0
    g.tick(HOUR)  # the slot opens: an ask, ISO-NE still on the old interval
    g.tick(HOUR + 1)
    g.tick(HOUR + 2)
    assert iso.fetches == 3
    assert iso.published == []
    iso.post(HOUR)  # ISO-NE posts the slot's first interval
    g.tick(HOUR + 3)  # the ask that finds it: publish
    assert [p.slot_start_s for p in iso.published] == [HOUR]
    assert iso.published[0].lmp == LMP
    g.tick(HOUR + 4)  # no more asks or publishes this slot
    g.tick(HOUR + 1800)
    assert iso.fetches == 4
    assert len(iso.published) == 1
    assert iso.glitches == []


def test_price_is_the_interval_parts_plus_delivery() -> None:
    iso = Isone()
    g = warm(iso)
    iso.post(HOUR)
    g.tick(HOUR)
    p = iso.published[0]
    assert p.lmp == LMP
    assert p.price_x1000 == 30_000 + 250 - 400 + p.delivery_x1000


def test_deadline_publishes_last_price_and_glitches() -> None:
    iso = Isone()
    g = warm(iso)
    iso.post(HOUR)
    g.tick(HOUR)
    iso.down = True
    for t in range(HOUR + SLOT_S, HOUR + SLOT_S + DEADLINE_S):
        g.tick(t)
    assert len(iso.published) == 1
    g.tick(HOUR + SLOT_S + DEADLINE_S)
    assert [p.slot_start_s for p in iso.published] == [HOUR, HOUR + SLOT_S]
    assert iso.published[1].lmp == LMP
    assert len(iso.glitches) == 1
    assert iso.glitches[0][0] == "stale price published"
    assert "ConnectionError" in iso.glitches[0][1]
    g.tick(HOUR + SLOT_S + DEADLINE_S + 1)  # the stale slot is done
    assert len(iso.published) == 2


def test_deadline_with_iso_stuck_on_the_old_interval_is_stale() -> None:
    iso = Isone()
    g = warm(iso)
    iso.post(HOUR)
    g.tick(HOUR)
    iso.post(HOUR + SLOT_S - 300)  # never posts the next slot's interval
    for t in range(HOUR + SLOT_S, HOUR + SLOT_S + DEADLINE_S + 1):
        g.tick(t)
    assert [p.slot_start_s for p in iso.published] == [HOUR, HOUR + SLOT_S]
    assert iso.glitches[0][0] == "stale price published"
    assert str(HOUR + SLOT_S - 300) in iso.glitches[0][1]


def test_cold_failure_publishes_nothing_and_glitches() -> None:
    iso = Isone()
    iso.down = True
    g = warm(iso)
    for t in range(HOUR, HOUR + DEADLINE_S + 1):
        g.tick(t)
    assert iso.published == []
    assert [s for s, _ in iso.glitches] == ["no price to publish"]
    # the next slot with ISO-NE back publishes fresh, no glitch
    iso.down = False
    iso.post(HOUR + SLOT_S)
    g.tick(HOUR + SLOT_S)
    assert [p.lmp for p in iso.published] == [LMP]
    assert len(iso.glitches) == 1
