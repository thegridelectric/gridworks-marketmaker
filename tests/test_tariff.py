"""Versant A-1 delivery periods and prices, by local wall-clock hour."""

from datetime import date, datetime

from gwmm.tariff import (
    OFF_PEAK_USD_PER_MWH,
    ON_PEAK_NON_WINTER_USD_PER_MWH,
    ON_PEAK_WINTER_USD_PER_MWH,
    SHOULDER_USD_PER_MWH,
    TARIFF_TZ,
    delivery_usd_per_mwh,
    holidays,
)


def at(year: int, month: int, day: int, hour: int) -> int:
    return int(datetime(year, month, day, hour, tzinfo=TARIFF_TZ).timestamp())


def test_weekday_windows_in_winter() -> None:
    # Tuesday 2026-01-20.
    assert delivery_usd_per_mwh(at(2026, 1, 20, 6)) == OFF_PEAK_USD_PER_MWH
    assert delivery_usd_per_mwh(at(2026, 1, 20, 7)) == ON_PEAK_WINTER_USD_PER_MWH
    assert delivery_usd_per_mwh(at(2026, 1, 20, 12)) == SHOULDER_USD_PER_MWH
    assert delivery_usd_per_mwh(at(2026, 1, 20, 16)) == ON_PEAK_WINTER_USD_PER_MWH
    assert delivery_usd_per_mwh(at(2026, 1, 20, 20)) == OFF_PEAK_USD_PER_MWH


def test_non_winter_on_peak_rate() -> None:
    # Tuesday 2026-10-20.
    assert delivery_usd_per_mwh(at(2026, 10, 20, 8)) == ON_PEAK_NON_WINTER_USD_PER_MWH


def test_weekend_and_holiday_have_no_peak() -> None:
    # Saturday 2026-01-24; Thanksgiving 2026-11-26.
    assert delivery_usd_per_mwh(at(2026, 1, 24, 8)) == SHOULDER_USD_PER_MWH
    assert date(2026, 11, 26) in holidays(2026)
    assert delivery_usd_per_mwh(at(2026, 11, 26, 18)) == SHOULDER_USD_PER_MWH
