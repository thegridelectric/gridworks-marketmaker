"""The delivery price of an hour under the fleet's time-of-use tariff.

Versant Rate A-1, "Home Eco Rate with Bonus Meter" (Bangor Hydro
District), charges delivery by period: on-peak, shoulder and off-peak
hours set by the weekday, the wall clock in the tariff's zone and the
tariff's holidays, with a higher on-peak price in winter. This module
answers the one question the maker asks of it: the total delivery price,
in the price word's integer form, for the hour starting at a given time.

The prices are a hand copy of the tariff sheet, the same copy the
price-forecast service uses. No sema word states a tariff's prices; a
tariff word with prices and a revision retires this module.
"""

from datetime import date, datetime, timedelta
from enum import Enum, auto
from zoneinfo import ZoneInfo

from pydantic import TypeAdapter

from gwmm.sema.property_format import LeftRightDot

TARIFF_TZ = ZoneInfo("America/New_York")
WINTER_MONTHS = frozenset({11, 12, 1, 2})

# The alias latest.price names the tariff by (its TariffAlias).
TARIFF_ALIAS: LeftRightDot = TypeAdapter(LeftRightDot).validate_python(
    "versant.a1.home.eco.bonus"
)

# Total delivery (distribution, transmission, stranded cost and
# conservation) per period, page 6.1.1 Seventeenth Revision, effective
# 2026-07-01, in USD/MWh times 1000. Winter is November through February.
# The DST-bracketing schedule (the two weeks around each transition) is
# not modelled; those hours take the standard windows.
ON_PEAK_WINTER_X1000 = 588_532
ON_PEAK_NON_WINTER_X1000 = 574_178
SHOULDER_X1000 = 64_429
OFF_PEAK_X1000 = 58_556


class Period(Enum):
    OnPeak = auto()
    Shoulder = auto()
    OffPeak = auto()


def nth_weekday(year: int, month: int, weekday: int, n: int) -> date:
    """The n-th (1-based) given weekday (Monday=0) of the month."""
    first = date(year, month, 1)
    offset = (weekday - first.weekday()) % 7
    return first + timedelta(days=offset + 7 * (n - 1))


def last_weekday(year: int, month: int, weekday: int) -> date:
    """The last given weekday (Monday=0) of the month."""
    following = date(year + (month == 12), month % 12 + 1, 1)
    last = following - timedelta(days=1)
    return last - timedelta(days=(last.weekday() - weekday) % 7)


def holidays(year: int) -> frozenset[date]:
    """The tariff's holidays: New Year's, Washington's, Patriot's,
    Memorial, Independence, Labor, Columbus, Veterans, Thanksgiving and
    Christmas, on the dates the tariff names them."""
    return frozenset(
        {
            date(year, 1, 1),
            nth_weekday(year, 2, 0, 3),
            nth_weekday(year, 4, 0, 3),
            last_weekday(year, 5, 0),
            date(year, 7, 4),
            nth_weekday(year, 9, 0, 1),
            nth_weekday(year, 10, 0, 2),
            date(year, 11, 11),
            nth_weekday(year, 11, 3, 4),
            date(year, 12, 25),
        }
    )


def period_at(local: datetime) -> Period:
    """The tariff period of the hour starting at a local wall-clock time."""
    hour = local.hour
    if hour < 7 or hour >= 20:
        return Period.OffPeak
    if local.weekday() >= 5 or local.date() in holidays(local.year):
        return Period.Shoulder
    if 12 <= hour < 16:
        return Period.Shoulder
    return Period.OnPeak


def delivery_x1000(hour_start_s: int) -> int:
    """Total-delivery price, times 1000 in USD/MWh, for the hour starting
    at the given time (unix seconds; the utc.seconds format is outside
    this snapshot's closure)."""
    local = datetime.fromtimestamp(hour_start_s, TARIFF_TZ)
    period = period_at(local)
    if period is Period.OffPeak:
        return OFF_PEAK_X1000
    if period is Period.Shoulder:
        return SHOULDER_X1000
    if local.month in WINTER_MONTHS:
        return ON_PEAK_WINTER_X1000
    return ON_PEAK_NON_WINTER_X1000
