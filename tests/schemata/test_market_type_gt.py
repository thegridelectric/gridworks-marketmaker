"""Tests market.type.gt type, version 000"""
import json

import pytest
from pydantic import ValidationError

from gwmm.enums import BidPriceUnit
from gwmm.enums import BidQuantityUnit
from gwmm.enums import MarketTypeAlias
from gwmm.enums import RecognizedCurrencyUnit
from gwmm.errors import SchemaError
from gwmm.schemata import MarketTypeGt_Maker as Maker


def test_market_type_gt_generated() -> None:

    d = {
        "AliasGtEnumSymbol": "618f9c0a",
        "DurationMinutes": 60,
        "GateClosingMinutes": 30,
        "PriceUnitGtEnumSymbol": "00000000",
        "QuantityUnitGtEnumSymbol": "c272f3b3",
        "CurrencyUnitGtEnumSymbol": "e57c5143",
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
        alias=gtuple.Alias,
        duration_minutes=gtuple.DurationMinutes,
        gate_closing_minutes=gtuple.GateClosingMinutes,
        price_unit=gtuple.PriceUnit,
        quantity_unit=gtuple.QuantityUnit,
        currency_unit=gtuple.CurrencyUnit,
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
    del d2["AliasGtEnumSymbol"]
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d2)

    d2 = dict(d)
    del d2["DurationMinutes"]
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d2)

    d2 = dict(d)
    del d2["GateClosingMinutes"]
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

    ######################################
    # Behavior on incorrect types
    ######################################

    d2 = dict(d, AliasGtEnumSymbol="hi")
    Maker.dict_to_tuple(d2).Alias = MarketTypeAlias.default()

    d2 = dict(d, DurationMinutes="60.1")
    with pytest.raises(ValidationError):
        Maker.dict_to_tuple(d2)

    d2 = dict(d, GateClosingMinutes="30.1")
    with pytest.raises(ValidationError):
        Maker.dict_to_tuple(d2)

    d2 = dict(d, PriceUnitGtEnumSymbol="hi")
    Maker.dict_to_tuple(d2).PriceUnit = BidPriceUnit.default()

    d2 = dict(d, QuantityUnitGtEnumSymbol="hi")
    Maker.dict_to_tuple(d2).QuantityUnit = BidQuantityUnit.default()

    d2 = dict(d, CurrencyUnitGtEnumSymbol="hi")
    Maker.dict_to_tuple(d2).CurrencyUnit = RecognizedCurrencyUnit.default()

    ######################################
    # SchemaError raised if TypeName is incorrect
    ######################################

    d2 = dict(d, TypeName="not the type alias")
    with pytest.raises(ValidationError):
        Maker.dict_to_tuple(d2)
