"""Tests for schema enum universe.type.000"""
from gwmm.enums import UniverseType


def test_universe_type() -> None:
    assert set(UniverseType.values()) == {
        "Dev",
        "Hybrid",
        "Production",
    }

    assert UniverseType.default() == UniverseType.Dev
