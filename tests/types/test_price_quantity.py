"""Tests price.quantity type, version 000"""
import json

import pytest
from gridworks.errors import SchemaError
from pydantic import ValidationError

from gwmm.enums import MarketPriceUnit
from gwmm.enums import MarketQuantityUnit
from gwmm.types import PriceQuantity_Maker as Maker


def test_price_quantity_generated() -> None:
    d = {
        "PriceTimes1000": 40000,
        "QuantityTimes1000": 10000,
        "PriceUnitGtEnumSymbol": "00000000",
        "QuantityUnitGtEnumSymbol": "c272f3b3",
        "InjectionIsPositive": False,
        "TypeName": "price.quantity",
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
        price_times1000=gtuple.PriceTimes1000,
        quantity_times1000=gtuple.QuantityTimes1000,
        price_unit=gtuple.PriceUnit,
        quantity_unit=gtuple.QuantityUnit,
        injection_is_positive=gtuple.InjectionIsPositive,
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
    del d2["PriceTimes1000"]
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d2)

    d2 = dict(d)
    del d2["QuantityTimes1000"]
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
    del d2["InjectionIsPositive"]
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d2)

    ######################################
    # Behavior on incorrect types
    ######################################

    d2 = dict(d, PriceTimes1000="40000.1")
    with pytest.raises(ValidationError):
        Maker.dict_to_tuple(d2)

    d2 = dict(d, QuantityTimes1000="10000.1")
    with pytest.raises(ValidationError):
        Maker.dict_to_tuple(d2)

    d2 = dict(d, PriceUnitGtEnumSymbol="hi")
    Maker.dict_to_tuple(d2).PriceUnit = MarketPriceUnit.default()

    d2 = dict(d, QuantityUnitGtEnumSymbol="hi")
    Maker.dict_to_tuple(d2).QuantityUnit = MarketQuantityUnit.default()

    d2 = dict(d, InjectionIsPositive="this is not a boolean")
    with pytest.raises(ValidationError):
        Maker.dict_to_tuple(d2)

    ######################################
    # SchemaError raised if TypeName is incorrect
    ######################################

    d2 = dict(d, TypeName="not the type alias")
    with pytest.raises(ValidationError):
        Maker.dict_to_tuple(d2)
