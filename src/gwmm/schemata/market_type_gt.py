"""Type market.type.gt, version 000"""
import json
from enum import auto
from typing import Any
from typing import Dict
from typing import List
from typing import Literal

from fastapi_utils.enums import StrEnum
from pydantic import BaseModel
from pydantic import validator

from gwmm.data_classes import MarketType
from gwmm.enums import BidPriceUnit
from gwmm.enums import BidQuantityUnit
from gwmm.enums import MarketTypeAlias
from gwmm.enums import RecognizedCurrencyUnit
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


class RecognizedCurrencyUnit000SchemaEnum:
    enum_name: str = "recognized.currency.unit.000"
    symbols: List[str] = [
        "00000000",
        "e57c5143",
        "f7b38fc5",
    ]

    @classmethod
    def is_symbol(cls, candidate: str) -> bool:
        if candidate in cls.symbols:
            return True
        return False


class RecognizedCurrencyUnit000(StrEnum):
    UNKNOWN = auto()
    USD = auto()
    GBP = auto()

    @classmethod
    def default(cls) -> "RecognizedCurrencyUnit000":
        return cls.UNKNOWN

    @classmethod
    def values(cls) -> List[str]:
        return [elt.value for elt in cls]


class RecognizedCurrencyUnitMap:
    @classmethod
    def type_to_local(cls, symbol: str) -> RecognizedCurrencyUnit:
        if not RecognizedCurrencyUnit000SchemaEnum.is_symbol(symbol):
            raise SchemaError(
                f"{symbol} must belong to RecognizedCurrencyUnit000 symbols"
            )
        versioned_enum = cls.type_to_versioned_enum_dict[symbol]
        return as_enum(
            versioned_enum, RecognizedCurrencyUnit, RecognizedCurrencyUnit.default()
        )

    @classmethod
    def local_to_type(cls, recognized_currency_unit: RecognizedCurrencyUnit) -> str:
        if not isinstance(recognized_currency_unit, RecognizedCurrencyUnit):
            raise SchemaError(
                f"{recognized_currency_unit} must be of type {RecognizedCurrencyUnit}"
            )
        versioned_enum = as_enum(
            recognized_currency_unit,
            RecognizedCurrencyUnit000,
            RecognizedCurrencyUnit000.default(),
        )
        return cls.versioned_enum_to_type_dict[versioned_enum]

    type_to_versioned_enum_dict: Dict[str, RecognizedCurrencyUnit000] = {
        "00000000": RecognizedCurrencyUnit000.UNKNOWN,
        "e57c5143": RecognizedCurrencyUnit000.USD,
        "f7b38fc5": RecognizedCurrencyUnit000.GBP,
    }

    versioned_enum_to_type_dict: Dict[RecognizedCurrencyUnit000, str] = {
        RecognizedCurrencyUnit000.UNKNOWN: "00000000",
        RecognizedCurrencyUnit000.USD: "e57c5143",
        RecognizedCurrencyUnit000.GBP: "f7b38fc5",
    }


class MarketTypeAlias000SchemaEnum:
    enum_name: str = "market.type.alias.000"
    symbols: List[str] = [
        "00000000",
        "d20b81e4",
        "b36cbfb4",
        "94a3fe9b",
        "5f335bdb",
        "01a84101",
        "e997ccfb",
        "618f9c0a",
    ]

    @classmethod
    def is_symbol(cls, candidate: str) -> bool:
        if candidate in cls.symbols:
            return True
        return False


class MarketTypeAlias000(StrEnum):
    unknown = auto()
    rt5gate5 = auto()
    rt60gate5 = auto()
    da60 = auto()
    rt60gate30 = auto()
    rt15gate5 = auto()
    rt30gate5 = auto()
    rt60gate30b = auto()

    @classmethod
    def default(cls) -> "MarketTypeAlias000":
        return cls.unknown

    @classmethod
    def values(cls) -> List[str]:
        return [elt.value for elt in cls]


class MarketTypeAliasMap:
    @classmethod
    def type_to_local(cls, symbol: str) -> MarketTypeAlias:
        if not MarketTypeAlias000SchemaEnum.is_symbol(symbol):
            raise SchemaError(f"{symbol} must belong to MarketTypeAlias000 symbols")
        versioned_enum = cls.type_to_versioned_enum_dict[symbol]
        return as_enum(versioned_enum, MarketTypeAlias, MarketTypeAlias.default())

    @classmethod
    def local_to_type(cls, market_type_alias: MarketTypeAlias) -> str:
        if not isinstance(market_type_alias, MarketTypeAlias):
            raise SchemaError(f"{market_type_alias} must be of type {MarketTypeAlias}")
        versioned_enum = as_enum(
            market_type_alias, MarketTypeAlias000, MarketTypeAlias000.default()
        )
        return cls.versioned_enum_to_type_dict[versioned_enum]

    type_to_versioned_enum_dict: Dict[str, MarketTypeAlias000] = {
        "00000000": MarketTypeAlias000.unknown,
        "d20b81e4": MarketTypeAlias000.rt5gate5,
        "b36cbfb4": MarketTypeAlias000.rt60gate5,
        "94a3fe9b": MarketTypeAlias000.da60,
        "5f335bdb": MarketTypeAlias000.rt60gate30,
        "01a84101": MarketTypeAlias000.rt15gate5,
        "e997ccfb": MarketTypeAlias000.rt30gate5,
        "618f9c0a": MarketTypeAlias000.rt60gate30b,
    }

    versioned_enum_to_type_dict: Dict[MarketTypeAlias000, str] = {
        MarketTypeAlias000.unknown: "00000000",
        MarketTypeAlias000.rt5gate5: "d20b81e4",
        MarketTypeAlias000.rt60gate5: "b36cbfb4",
        MarketTypeAlias000.da60: "94a3fe9b",
        MarketTypeAlias000.rt60gate30: "5f335bdb",
        MarketTypeAlias000.rt15gate5: "01a84101",
        MarketTypeAlias000.rt30gate5: "e997ccfb",
        MarketTypeAlias000.rt60gate30b: "618f9c0a",
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


class MarketTypeGt(BaseModel):
    Alias: MarketTypeAlias  #
    DurationMinutes: int  #
    GateClosingMinutes: int  #
    PriceUnit: BidPriceUnit  #
    QuantityUnit: BidQuantityUnit  #
    CurrencyUnit: RecognizedCurrencyUnit  #
    TypeName: Literal["market.type.gt"] = "market.type.gt"
    Version: str = "000"

    @validator("Alias")
    def _validator_alias(cls, v: MarketTypeAlias) -> MarketTypeAlias:
        return as_enum(v, MarketTypeAlias, MarketTypeAlias.unknown)

    @validator("PriceUnit")
    def _validator_price_unit(cls, v: BidPriceUnit) -> BidPriceUnit:
        return as_enum(v, BidPriceUnit, BidPriceUnit.USDPerMWh)

    @validator("QuantityUnit")
    def _validator_quantity_unit(cls, v: BidQuantityUnit) -> BidQuantityUnit:
        return as_enum(v, BidQuantityUnit, BidQuantityUnit.AvgMW)

    @validator("CurrencyUnit")
    def _validator_currency_unit(
        cls, v: RecognizedCurrencyUnit
    ) -> RecognizedCurrencyUnit:
        return as_enum(v, RecognizedCurrencyUnit, RecognizedCurrencyUnit.UNKNOWN)

    def as_dict(self) -> Dict[str, Any]:
        d = self.dict()
        del d["Alias"]
        Alias = as_enum(self.Alias, MarketTypeAlias, MarketTypeAlias.default())
        d["AliasGtEnumSymbol"] = MarketTypeAliasMap.local_to_type(Alias)
        del d["PriceUnit"]
        PriceUnit = as_enum(self.PriceUnit, BidPriceUnit, BidPriceUnit.default())
        d["PriceUnitGtEnumSymbol"] = BidPriceUnitMap.local_to_type(PriceUnit)
        del d["QuantityUnit"]
        QuantityUnit = as_enum(
            self.QuantityUnit, BidQuantityUnit, BidQuantityUnit.default()
        )
        d["QuantityUnitGtEnumSymbol"] = BidQuantityUnitMap.local_to_type(QuantityUnit)
        del d["CurrencyUnit"]
        CurrencyUnit = as_enum(
            self.CurrencyUnit, RecognizedCurrencyUnit, RecognizedCurrencyUnit.default()
        )
        d["CurrencyUnitGtEnumSymbol"] = RecognizedCurrencyUnitMap.local_to_type(
            CurrencyUnit
        )
        return d

    def as_type(self) -> str:
        return json.dumps(self.as_dict())


class MarketTypeGt_Maker:
    type_name = "market.type.gt"
    version = "000"

    def __init__(
        self,
        alias: MarketTypeAlias,
        duration_minutes: int,
        gate_closing_minutes: int,
        price_unit: BidPriceUnit,
        quantity_unit: BidQuantityUnit,
        currency_unit: RecognizedCurrencyUnit,
    ):

        self.tuple = MarketTypeGt(
            Alias=alias,
            DurationMinutes=duration_minutes,
            GateClosingMinutes=gate_closing_minutes,
            PriceUnit=price_unit,
            QuantityUnit=quantity_unit,
            CurrencyUnit=currency_unit,
            #
        )

    @classmethod
    def tuple_to_type(cls, tuple: MarketTypeGt) -> str:
        return tuple.as_type()

    @classmethod
    def type_to_tuple(cls, t: str) -> MarketTypeGt:
        try:
            d = json.loads(t)
        except TypeError:
            raise SchemaError("Type must be string or bytes!")
        if not isinstance(d, dict):
            raise SchemaError(f"Deserializing {t} must result in dict!")
        return cls.dict_to_tuple(d)

    @classmethod
    def dict_to_tuple(cls, d: dict[str, Any]) -> MarketTypeGt:
        d2 = dict(d)
        if "AliasGtEnumSymbol" not in d2.keys():
            raise SchemaError(f"dict {d2} missing AliasGtEnumSymbol")
        if d2["AliasGtEnumSymbol"] in MarketTypeAlias000SchemaEnum.symbols:
            d2["Alias"] = MarketTypeAliasMap.type_to_local(d2["AliasGtEnumSymbol"])
        else:
            d2["Alias"] = MarketTypeAlias.default()
        if "DurationMinutes" not in d2.keys():
            raise SchemaError(f"dict {d2} missing DurationMinutes")
        if "GateClosingMinutes" not in d2.keys():
            raise SchemaError(f"dict {d2} missing GateClosingMinutes")
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
        if "CurrencyUnitGtEnumSymbol" not in d2.keys():
            raise SchemaError(f"dict {d2} missing CurrencyUnitGtEnumSymbol")
        if (
            d2["CurrencyUnitGtEnumSymbol"]
            in RecognizedCurrencyUnit000SchemaEnum.symbols
        ):
            d2["CurrencyUnit"] = RecognizedCurrencyUnitMap.type_to_local(
                d2["CurrencyUnitGtEnumSymbol"]
            )
        else:
            d2["CurrencyUnit"] = RecognizedCurrencyUnit.default()
        if "TypeName" not in d2.keys():
            raise SchemaError(f"dict {d2} missing TypeName")

        return MarketTypeGt(
            Alias=d2["Alias"],
            DurationMinutes=d2["DurationMinutes"],
            GateClosingMinutes=d2["GateClosingMinutes"],
            PriceUnit=d2["PriceUnit"],
            QuantityUnit=d2["QuantityUnit"],
            CurrencyUnit=d2["CurrencyUnit"],
            TypeName=d2["TypeName"],
            Version="000",
        )

    @classmethod
    def tuple_to_dc(cls, t: MarketTypeGt) -> MarketType:
        if t.Alias in MarketType.by_id.keys():
            dc = MarketType.by_id[t.Alias]
        else:
            dc = MarketType(
                alias=t.Alias,
                duration_minutes=t.DurationMinutes,
                gate_closing_minutes=t.GateClosingMinutes,
                price_unit=t.PriceUnit,
                quantity_unit=t.QuantityUnit,
                currency_unit=t.CurrencyUnit,
            )

        return dc

    @classmethod
    def dc_to_tuple(cls, dc: MarketType) -> MarketTypeGt:
        t = MarketTypeGt_Maker(
            alias=dc.alias,
            duration_minutes=dc.duration_minutes,
            gate_closing_minutes=dc.gate_closing_minutes,
            price_unit=dc.price_unit,
            quantity_unit=dc.quantity_unit,
            currency_unit=dc.currency_unit,
        ).tuple
        return t

    @classmethod
    def type_to_dc(cls, t: str) -> MarketType:
        return cls.tuple_to_dc(cls.type_to_tuple(t))

    @classmethod
    def dc_to_type(cls, dc: MarketType) -> str:
        return cls.dc_to_tuple(dc).as_type()

    @classmethod
    def dict_to_dc(cls, d: dict[Any, str]) -> MarketType:
        return cls.tuple_to_dc(cls.dict_to_tuple(d))
