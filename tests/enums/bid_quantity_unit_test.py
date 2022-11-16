"""Tests for schema enum bid.quantity.unit.000"""
from gwmm.enums import BidQuantityUnit


def test_bid_quantity_unit() -> None:

    assert set(BidQuantityUnit.values()) == {
        "AvgMW",
        "AvgkW",
    }

    assert BidQuantityUnit.default() == BidQuantityUnit.AvgMW
