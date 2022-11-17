"""Tests latest.price type, version 000"""
import json

import pytest
from pydantic import ValidationError

from gwmm.enums import MarketPriceUnit
from gwmm.errors import SchemaError
from gwmm.schemata import LatestPrice_Maker as Maker


def test_latest_price_generated() -> None:

    d = {
        "FromGNodeAlias": "d1.isone.ver.keene",
        "FromGNodeInstanceId": "f0eaf540-94c8-4f85-a671-395ab86d0392",
        "PriceTimes1000": 32134,
        "PriceUnitGtEnumSymbol": "00000000",
        "MarketSlotName": "rt60gate5.d1.isone.ver.keene.1577854800",
        "IrlTimeUtc": "2021-01-01T05:00:00+00:00",
        "MessageId": "03d27b8e-f6b3-40c5-afe8-880d12921710",
        "TypeName": "latest.price",
        "Version": "000",
    }

    with pytest.raises(SchemaError):
        Maker.type_to_tuple(d)

    with pytest.raises(SchemaError):
        Maker.type_to_tuple('"not a dict"')

    # Test type_to_tuple
    gtype = json.dumps(d)
    gtuple = Maker.type_to_tuple(gtype)

    # test type_to_tuple and tuple_to_type maps
    assert Maker.type_to_tuple(Maker.tuple_to_type(gtuple)) == gtuple

    # test Maker init
    t = Maker(
        from_g_node_alias=gtuple.FromGNodeAlias,
        from_g_node_instance_id=gtuple.FromGNodeInstanceId,
        price_times1000=gtuple.PriceTimes1000,
        price_unit=gtuple.PriceUnit,
        market_slot_name=gtuple.MarketSlotName,
        irl_time_utc=gtuple.IrlTimeUtc,
        message_id=gtuple.MessageId,
    ).tuple
    assert t == gtuple

    ######################################
    # SchemaError raised if missing a required attribute
    ######################################

    d2 = dict(d)
    del d2["TypeName"]
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d2)

    d2 = dict(d)
    del d2["FromGNodeAlias"]
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d2)

    d2 = dict(d)
    del d2["FromGNodeInstanceId"]
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d2)

    d2 = dict(d)
    del d2["PriceTimes1000"]
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d2)

    d2 = dict(d)
    del d2["PriceUnitGtEnumSymbol"]
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d2)

    d2 = dict(d)
    del d2["MarketSlotName"]
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d2)

    ######################################
    # Optional attributes can be removed from type
    ######################################

    d2 = dict(d)
    if "IrlTimeUtc" in d2.keys():
        del d2["IrlTimeUtc"]
    Maker.dict_to_tuple(d2)

    d2 = dict(d)
    if "MessageId" in d2.keys():
        del d2["MessageId"]
    Maker.dict_to_tuple(d2)

    ######################################
    # Behavior on incorrect types
    ######################################

    d2 = dict(d, PriceTimes1000="32134.1")
    with pytest.raises(ValidationError):
        Maker.dict_to_tuple(d2)

    d2 = dict(d, PriceUnitGtEnumSymbol="hi")
    Maker.dict_to_tuple(d2).PriceUnit = MarketPriceUnit.default()

    ######################################
    # SchemaError raised if TypeName is incorrect
    ######################################

    d2 = dict(d, TypeName="not the type alias")
    with pytest.raises(ValidationError):
        Maker.dict_to_tuple(d2)

    ######################################
    # SchemaError raised if primitive attributes do not have appropriate property_format
    ######################################

    d2 = dict(d, FromGNodeAlias="a.b-h")
    with pytest.raises(ValidationError):
        Maker.dict_to_tuple(d2)

    d2 = dict(d, FromGNodeInstanceId="d4be12d5-33ba-4f1f-b9e5")
    with pytest.raises(ValidationError):
        Maker.dict_to_tuple(d2)

    d2 = dict(d, MessageId="d4be12d5-33ba-4f1f-b9e5")
    with pytest.raises(ValidationError):
        Maker.dict_to_tuple(d2)

    # End of Test
