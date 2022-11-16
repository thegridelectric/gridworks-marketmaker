"""Type price.quantity, version 000"""
import json
from enum import auto
from typing import Any
from typing import Dict
from typing import List
from typing import Literal

from fastapi_utils.enums import StrEnum
from pydantic import BaseModel
from pydantic import validator

from gwmm.enums import BidPriceUnit
from gwmm.enums import BidQuantityUnit
from gwmm.errors import SchemaError
from gwmm.message import as_enum


class BidPriceUnit000SchemaEnum:
    enum_name: str = "bid.price.unit.000"
    symbols: List[str] = [
        "00000000",
    ]

    @classmethod
    def is_symbol(cls, candidate: str) -> bool:
        if candidate in cls.symbols:
            return True
        return False


class BidPriceUnit000(StrEnum):
    USDPerMWh = auto()

    @classmethod
    def default(cls) -> "BidPriceUnit000":
        return cls.USDPerMWh

    @classmethod
    def values(cls) -> List[str]:
        return [elt.value for elt in cls]


class BidPriceUnitMap:
    @classmethod
    def type_to_local(cls, symbol: str) -> BidPriceUnit:
        if not BidPriceUnit000SchemaEnum.is_symbol(symbol):
            raise SchemaError(f"{symbol} must belong to BidPriceUnit000 symbols")
        versioned_enum = cls.type_to_versioned_enum_dict[symbol]
        return as_enum(versioned_enum, BidPriceUnit, BidPriceUnit.default())

    @classmethod
    def local_to_type(cls, bid_price_unit: BidPriceUnit) -> str:
        if not isinstance(bid_price_unit, BidPriceUnit):
            raise SchemaError(f"{bid_price_unit} must be of type {BidPriceUnit}")
        versioned_enum = as_enum(
            bid_price_unit, BidPriceUnit000, BidPriceUnit000.default()
        )
        return cls.versioned_enum_to_type_dict[versioned_enum]

    type_to_versioned_enum_dict: Dict[str, BidPriceUnit000] = {
        "00000000": BidPriceUnit000.USDPerMWh,
    }

    versioned_enum_to_type_dict: Dict[BidPriceUnit000, str] = {
        BidPriceUnit000.USDPerMWh: "00000000",
    }


class BidQuantityUnit000SchemaEnum:
    enum_name: str = "bid.quantity.unit.000"
    symbols: List[str] = [
        "00000000",
        "c272f3b3",
    ]

    @classmethod
    def is_symbol(cls, candidate: str) -> bool:
        if candidate in cls.symbols:
            return True
        return False


class BidQuantityUnit000(StrEnum):
    AvgMW = auto()
    AvgkW = auto()

    @classmethod
    def default(cls) -> "BidQuantityUnit000":
        return cls.AvgMW

    @classmethod
    def values(cls) -> List[str]:
        return [elt.value for elt in cls]


class BidQuantityUnitMap:
    @classmethod
    def type_to_local(cls, symbol: str) -> BidQuantityUnit:
        if not BidQuantityUnit000SchemaEnum.is_symbol(symbol):
            raise SchemaError(f"{symbol} must belong to BidQuantityUnit000 symbols")
        versioned_enum = cls.type_to_versioned_enum_dict[symbol]
        return as_enum(versioned_enum, BidQuantityUnit, BidQuantityUnit.default())

    @classmethod
    def local_to_type(cls, bid_quantity_unit: BidQuantityUnit) -> str:
        if not isinstance(bid_quantity_unit, BidQuantityUnit):
            raise SchemaError(f"{bid_quantity_unit} must be of type {BidQuantityUnit}")
        versioned_enum = as_enum(
            bid_quantity_unit, BidQuantityUnit000, BidQuantityUnit000.default()
        )
        return cls.versioned_enum_to_type_dict[versioned_enum]

    type_to_versioned_enum_dict: Dict[str, BidQuantityUnit000] = {
        "00000000": BidQuantityUnit000.AvgMW,
        "c272f3b3": BidQuantityUnit000.AvgkW,
    }

    versioned_enum_to_type_dict: Dict[BidQuantityUnit000, str] = {
        BidQuantityUnit000.AvgMW: "00000000",
        BidQuantityUnit000.AvgkW: "c272f3b3",
    }


class PriceQuantity(BaseModel):
    PriceTimes1000: int  #
    QuantityTimes1000: int  #
    PriceUnit: BidPriceUnit  #
    QuantityUnit: BidQuantityUnit  #
    InjectionIsPositive: bool  #
    TypeName: Literal["price.quantity"] = "price.quantity"
    Version: str = "000"

    @validator("PriceUnit")
    def _validator_price_unit(cls, v: BidPriceUnit) -> BidPriceUnit:
        return as_enum(v, BidPriceUnit, BidPriceUnit.USDPerMWh)

    @validator("QuantityUnit")
    def _validator_quantity_unit(cls, v: BidQuantityUnit) -> BidQuantityUnit:
        return as_enum(v, BidQuantityUnit, BidQuantityUnit.AvgMW)

    def as_dict(self) -> Dict[str, Any]:
        d = self.dict()
        del d["PriceUnit"]
        PriceUnit = as_enum(self.PriceUnit, BidPriceUnit, BidPriceUnit.default())
        d["PriceUnitGtEnumSymbol"] = BidPriceUnitMap.local_to_type(PriceUnit)
        del d["QuantityUnit"]
        QuantityUnit = as_enum(
            self.QuantityUnit, BidQuantityUnit, BidQuantityUnit.default()
        )
        d["QuantityUnitGtEnumSymbol"] = BidQuantityUnitMap.local_to_type(QuantityUnit)
        return d

    def as_type(self) -> str:
        return json.dumps(self.as_dict())


class PriceQuantity_Maker:
    type_name = "price.quantity"
    version = "000"

    def __init__(
        self,
        price_times1000: int,
        quantity_times1000: int,
        price_unit: BidPriceUnit,
        quantity_unit: BidQuantityUnit,
        injection_is_positive: bool,
    ):

        self.tuple = PriceQuantity(
            PriceTimes1000=price_times1000,
            QuantityTimes1000=quantity_times1000,
            PriceUnit=price_unit,
            QuantityUnit=quantity_unit,
            InjectionIsPositive=injection_is_positive,
            #
        )

    @classmethod
    def tuple_to_type(cls, tuple: PriceQuantity) -> str:
        return tuple.as_type()

    @classmethod
    def type_to_tuple(cls, t: str) -> PriceQuantity:
        try:
            d = json.loads(t)
        except TypeError:
            raise SchemaError("Type must be string or bytes!")
        if not isinstance(d, dict):
            raise SchemaError(f"Deserializing {t} must result in dict!")
        return cls.dict_to_tuple(d)

    @classmethod
    def dict_to_tuple(cls, d: dict[str, Any]) -> PriceQuantity:
        d2 = dict(d)
        if "PriceTimes1000" not in d2.keys():
            raise SchemaError(f"dict {d2} missing PriceTimes1000")
        if "QuantityTimes1000" not in d2.keys():
            raise SchemaError(f"dict {d2} missing QuantityTimes1000")
        if "PriceUnitGtEnumSymbol" not in d2.keys():
            raise SchemaError(f"dict {d2} missing PriceUnitGtEnumSymbol")
        if d2["PriceUnitGtEnumSymbol"] in BidPriceUnit000SchemaEnum.symbols:
            d2["PriceUnit"] = BidPriceUnitMap.type_to_local(d2["PriceUnitGtEnumSymbol"])
        else:
            d2["PriceUnit"] = BidPriceUnit.default()
        if "QuantityUnitGtEnumSymbol" not in d2.keys():
            raise SchemaError(f"dict {d2} missing QuantityUnitGtEnumSymbol")
        if d2["QuantityUnitGtEnumSymbol"] in BidQuantityUnit000SchemaEnum.symbols:
            d2["QuantityUnit"] = BidQuantityUnitMap.type_to_local(
                d2["QuantityUnitGtEnumSymbol"]
            )
        else:
            d2["QuantityUnit"] = BidQuantityUnit.default()
        if "InjectionIsPositive" not in d2.keys():
            raise SchemaError(f"dict {d2} missing InjectionIsPositive")
        if "TypeName" not in d2.keys():
            raise SchemaError(f"dict {d2} missing TypeName")

        return PriceQuantity(
            PriceTimes1000=d2["PriceTimes1000"],
            QuantityTimes1000=d2["QuantityTimes1000"],
            PriceUnit=d2["PriceUnit"],
            QuantityUnit=d2["QuantityUnit"],
            InjectionIsPositive=d2["InjectionIsPositive"],
            TypeName=d2["TypeName"],
            Version="000",
        )
