"""Tests for schema enum g.node.role.000"""
from gwmm.enums import GNodeRole


def test_g_node_role() -> None:
    assert set(GNodeRole.values()) == {
        "GNode",
        "TerminalAsset",
        "Scada",
        "PriceService",
        "WeatherService",
        "AggregatedTNode",
        "AtomicTNode",
        "MarketMaker",
        "AtomicMeteringNode",
        "ConductorTopologyNode",
        "InterconnectionComponent",
        "World",
        "TimeCoordinator",
        "Supervisor",
    }

    assert GNodeRole.default() == GNodeRole.GNode
