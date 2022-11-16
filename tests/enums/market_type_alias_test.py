"""Tests for schema enum market.type.alias.000"""
from gwmm.enums import MarketTypeAlias


def test_market_type_alias() -> None:

    assert set(MarketTypeAlias.values()) == {
        "unknown",
        "rt5gate5",
        "rt60gate5",
        "da60",
        "rt60gate30",
        "rt15gate5",
        "rt30gate5",
        "rt60gate30b",
    }

    assert MarketTypeAlias.default() == MarketTypeAlias.unknown
