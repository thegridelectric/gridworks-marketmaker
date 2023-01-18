import gridworks.property_format as property_format

from gwmm.data_classes import MarketType
from gwmm.types import MarketSlot
from gwmm.types import MarketTypeGt_Maker


def market_slot_from_name(market_slot_name: str) -> MarketSlot:
    """rt60gate30b.d1.isone.ver.keene.1577836800"""
    try:
        property_format.check_is_market_slot_name_lrd_format(market_slot_name)
    except ValueError as e:
        raise ValueError(f"{e}")
    words = market_slot_name.split(".")
    market_type_name = words[0]
    market_type_dc = MarketType.by_id[market_type_name]
    market_type = MarketTypeGt_Maker.dc_to_tuple(market_type_dc)
    market_maker_alias = ".".join(words[1:-1])
    slot_start = int(words[-1])
    return MarketSlot(
        Type=market_type, MarketMakerAlias=market_maker_alias, StartUnixS=slot_start
    )


def name_from_market_slot(slot: MarketSlot) -> str:
    return f"{slot.Type.Name.value}.{slot.MarketMakerAlias}.{slot.StartUnixS}"
