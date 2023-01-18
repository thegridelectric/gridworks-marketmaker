"""Tests market.type.gt type, version 000"""
import json

import pytest
from gridworks.errors import SchemaError
from pydantic import ValidationError

from gwmm.enums import MarketPriceUnit
from gwmm.enums import MarketQuantityUnit
from gwmm.enums import MarketTypeName
from gwmm.enums import RecognizedCurrencyUnit
from gwmm.types import MarketTypeGt_Maker as Maker


def test_market_type_gt_generated() -> None:
    d = {
        "NameGtEnumSymbol": "618f9c0a",
        "DurationMinutes": 60,
        "GateClosingSeconds": 60,
        "PriceUnitGtEnumSymbol": "00000000",
        "QuantityUnitGtEnumSymbol": "c272f3b3",
        "CurrencyUnitGtEnumSymbol": "e57c5143",
        "PriceMax": 10000,
        "TypeName": "market.type.gt",
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
        name=gtuple.Name,
        duration_minutes=gtuple.DurationMinutes,
        gate_closing_seconds=gtuple.GateClosingSeconds,
        price_unit=gtuple.PriceUnit,
        quantity_unit=gtuple.QuantityUnit,
        currency_unit=gtuple.CurrencyUnit,
        price_max=gtuple.PriceMax,
    ).tuple
    assert t == gtuple

    ######################################
    # Dataclass related tests
    ######################################

    dc = Maker.tuple_to_dc(gtuple)
    assert gtuple == Maker.dc_to_tuple(dc)
    assert Maker.type_to_dc(Maker.dc_to_type(dc)) == dc

    ######################################
    # SchemaError raised if missing a required attribute
    ######################################

    d2 = dict(d)
    del d2["TypeName"]
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d2)

    d2 = dict(d)
    del d2["NameGtEnumSymbol"]
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d2)

    d2 = dict(d)
    del d2["DurationMinutes"]
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d2)

    d2 = dict(d)
    del d2["GateClosingSeconds"]
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d2)

    d2 = dict(d)
    del d2["PriceUnitGtEnumSymbol"]
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d2)

    d2 = dict(d)
    del d2["QuantityUnitGtEnumSymbol"]
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d2)

    d2 = dict(d)
    del d2["CurrencyUnitGtEnumSymbol"]
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d2)

    d2 = dict(d)
    del d2["PriceMax"]
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d2)

    ######################################
    # Behavior on incorrect types
    ######################################

    d2 = dict(d, NameGtEnumSymbol="hi")
    Maker.dict_to_tuple(d2).Name = MarketTypeName.default()

    d2 = dict(d, DurationMinutes="60.1")
    with pytest.raises(ValidationError):
        Maker.dict_to_tuple(d2)

    d2 = dict(d, GateClosingSeconds="60.1")
    with pytest.raises(ValidationError):
        Maker.dict_to_tuple(d2)

    d2 = dict(d, PriceUnitGtEnumSymbol="hi")
    Maker.dict_to_tuple(d2).PriceUnit = MarketPriceUnit.default()

    d2 = dict(d, QuantityUnitGtEnumSymbol="hi")
    Maker.dict_to_tuple(d2).QuantityUnit = MarketQuantityUnit.default()

    d2 = dict(d, CurrencyUnitGtEnumSymbol="hi")
    Maker.dict_to_tuple(d2).CurrencyUnit = RecognizedCurrencyUnit.default()

    d2 = dict(d, PriceMax="10000.1")
    with pytest.raises(ValidationError):
        Maker.dict_to_tuple(d2)

    ######################################
    # SchemaError raised if TypeName is incorrect
    ######################################

    d2 = dict(d, TypeName="not the type alias")
    with pytest.raises(ValidationError):
        Maker.dict_to_tuple(d2)
