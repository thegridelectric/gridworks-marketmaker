"""Tests for schema enum bid.price.unit.000"""
from gwmm.enums import BidPriceUnit


def test_bid_price_unit() -> None:

    assert set(BidPriceUnit.values()) == {
        "USDPerMWh",
    }

    assert BidPriceUnit.default() == BidPriceUnit.USDPerMWh
