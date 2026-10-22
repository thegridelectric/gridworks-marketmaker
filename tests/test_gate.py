"""The slot gate on a fake clock: fetch before the hour, publish at it,
stale fallback with a glitch, nothing to publish on a cold failure."""

from gwmm.gate import SLOT_S, SlotGate, SlotPrice, next_slot_start, slot_start

HOUR = 1_770_000_000 - 1_770_000_000 % SLOT_S  # some top of an hour


class Recorder:
    def __init__(self, lmp: float | None = 30.0) -> None:
        self.lmp = lmp
        self.fetches = 0
        self.published: list[SlotPrice] = []
        self.glitches: list[tuple[str, str]] = []

    def fetch(self) -> float:
        self.fetches += 1
        if self.lmp is None:
            raise ConnectionError("iso-ne down")
        return self.lmp

    def gate(self, lead_s: int = 20) -> SlotGate:
        return SlotGate(
            fetch_lmp=self.fetch,
            publish=self.published.append,
            raise_glitch=lambda s, d: self.glitches.append((s, d)),
            fetch_lead_s=lead_s,
        )


def test_slot_arithmetic() -> None:
    assert slot_start(HOUR + 1234) == HOUR
    assert next_slot_start(HOUR + 1234) == HOUR + SLOT_S
    assert next_slot_start(HOUR) == HOUR + SLOT_S


def test_first_tick_publishes_the_open_slot() -> None:
    r = Recorder()
    g = r.gate()
    g.tick(HOUR + 600)
    assert r.fetches == 1
    assert [p.slot_start_s for p in r.published] == [HOUR]
    assert r.glitches == []


def test_fetch_before_the_hour_then_publish_at_it() -> None:
    r = Recorder()
    g = r.gate(lead_s=20)
    g.tick(HOUR + 600)  # boot publish
    g.tick(HOUR + SLOT_S - 30)  # before the lead window: nothing
    assert r.fetches == 1
    g.tick(HOUR + SLOT_S - 20)  # lead window opens: fetch once
    g.tick(HOUR + SLOT_S - 10)
    assert r.fetches == 2
    assert len(r.published) == 1
    g.tick(HOUR + SLOT_S)  # top of the hour: publish
    assert [p.slot_start_s for p in r.published] == [HOUR, HOUR + SLOT_S]
    g.tick(HOUR + SLOT_S + 1)  # once per slot
    assert len(r.published) == 2


def test_energy_is_lmp_plus_delivery() -> None:
    r = Recorder(lmp=30.0)
    g = r.gate()
    g.tick(HOUR)
    p = r.published[0]
    assert p.lmp_usd_per_mwh == 30.0
    assert p.energy_usd_per_mwh == 30.0 + p.delivery_usd_per_mwh


def test_failed_fetch_publishes_last_price_and_glitches() -> None:
    r = Recorder(lmp=30.0)
    g = r.gate()
    g.tick(HOUR)
    r.lmp = None
    g.tick(HOUR + SLOT_S - 20)
    g.tick(HOUR + SLOT_S)
    assert [p.slot_start_s for p in r.published] == [HOUR, HOUR + SLOT_S]
    assert r.published[1].lmp_usd_per_mwh == 30.0
    assert len(r.glitches) == 1
    assert r.glitches[0][0] == "stale price published"
    assert "ConnectionError" in r.glitches[0][1]


def test_cold_failure_publishes_nothing_and_glitches() -> None:
    r = Recorder(lmp=None)
    g = r.gate()
    g.tick(HOUR)
    assert r.published == []
    assert [s for s, _ in r.glitches] == ["no price to publish"]
    # the next slot with ISO-NE back publishes fresh, no glitch
    r.lmp = 40.0
    g.tick(HOUR + SLOT_S - 20)
    g.tick(HOUR + SLOT_S)
    assert [p.lmp_usd_per_mwh for p in r.published] == [40.0]
    assert len(r.glitches) == 1
