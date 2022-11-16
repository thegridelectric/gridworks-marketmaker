""" List of all the types used"""
from typing import Dict
from typing import List
from typing import no_type_check

from gwmm.schemata import Bid_Maker
from gwmm.schemata import BidAck_Maker
from gwmm.schemata import GnodeGt_Maker
from gwmm.schemata import HeartbeatA_Maker
from gwmm.schemata import LatestPrice_Maker
from gwmm.schemata import MarketTypeGt_Maker
from gwmm.schemata import PriceQuantity_Maker
from gwmm.schemata import PriceQuantityUnitless_Maker
from gwmm.schemata import Ready_Maker
from gwmm.schemata import SimTimestep_Maker


TypeMakerByName: Dict[str, HeartbeatA_Maker] = {}


@no_type_check
def type_makers() -> List[HeartbeatA_Maker]:
    return [
        Bid_Maker,
        BidAck_Maker,
        GnodeGt_Maker,
        HeartbeatA_Maker,
        LatestPrice_Maker,
        MarketTypeGt_Maker,
        PriceQuantity_Maker,
        PriceQuantityUnitless_Maker,
        Ready_Maker,
        SimTimestep_Maker,
    ]


for maker in type_makers():
    TypeMakerByName[maker.type_name] = maker


def version_by_type_name() -> Dict[str, str]:
    """
    Returns:
        Dict[str, str]: Keys are TypeNames, values are versions
    """

    v: Dict[str, str] = {
        "bid": "000",
        "bid.ack": "000",
        "gnode.gt": "000",
        "heartbeat.a": "000",
        "latest.price": "000",
        "market.type.gt": "000",
        "price.quantity": "000",
        "price.quantity.unitless": "000",
        "ready": "000",
        "sim.timestep": "000",
    }

    return v


def status_by_versioned_type_name() -> Dict[str, str]:
    """
    Returns:
        Dict[str, str]: Keys are versioned TypeNames, values are type status
    """

    v: Dict[str, str] = {
        "bid.000": "Pending",
        "bid.ack.000": "Pending",
        "gnode.gt.000": "Pending",
        "heartbeat.a.000": "Pending",
        "latest.price.000": "Pending",
        "market.type.gt.000": "Pending",
        "price.quantity.000": "Pending",
        "price.quantity.unitless.000": "Pending",
        "ready.000": "Pending",
        "sim.timestep.000": "Pending",
    }

    return v
