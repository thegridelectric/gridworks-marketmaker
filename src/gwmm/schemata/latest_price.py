"""Type latest.price, version 000"""
import json
from enum import auto
from typing import Any
from typing import Dict
from typing import List
from typing import Literal
from typing import Optional

from fastapi_utils.enums import StrEnum
from pydantic import BaseModel
from pydantic import validator

import gwmm.property_format as property_format
from gwmm.enums import MarketPriceUnit
from gwmm.errors import SchemaError
from gwmm.message import as_enum
from gwmm.property_format import predicate_validator


class MarketPriceUnit000SchemaEnum:
    enum_name: str = "market.price.unit.000"
    symbols: List[str] = [
        "00000000",
    ]

    @classmethod
    def is_symbol(cls, candidate: str) -> bool:
        if candidate in cls.symbols:
            return True
        return False


class MarketPriceUnit000(StrEnum):
    USDPerMWh = auto()

    @classmethod
    def default(cls) -> "MarketPriceUnit000":
        return cls.USDPerMWh

    @classmethod
    def values(cls) -> List[str]:
        return [elt.value for elt in cls]


class MarketPriceUnitMap:
    @classmethod
    def type_to_local(cls, symbol: str) -> MarketPriceUnit:
        if not MarketPriceUnit000SchemaEnum.is_symbol(symbol):
            raise SchemaError(f"{symbol} must belong to MarketPriceUnit000 symbols")
        versioned_enum = cls.type_to_versioned_enum_dict[symbol]
        return as_enum(versioned_enum, MarketPriceUnit, MarketPriceUnit.default())

    @classmethod
    def local_to_type(cls, market_price_unit: MarketPriceUnit) -> str:
        if not isinstance(market_price_unit, MarketPriceUnit):
            raise SchemaError(f"{market_price_unit} must be of type {MarketPriceUnit}")
        versioned_enum = as_enum(
            market_price_unit, MarketPriceUnit000, MarketPriceUnit000.default()
        )
        return cls.versioned_enum_to_type_dict[versioned_enum]

    type_to_versioned_enum_dict: Dict[str, MarketPriceUnit000] = {
        "00000000": MarketPriceUnit000.USDPerMWh,
    }

    versioned_enum_to_type_dict: Dict[MarketPriceUnit000, str] = {
        MarketPriceUnit000.USDPerMWh: "00000000",
    }


class LatestPrice(BaseModel):
    FromGNodeAlias: str  #
    FromGNodeInstanceId: str  #
    PriceTimes1000: int  #
    PriceUnit: MarketPriceUnit  #
    MarketSlotName: str  #
    IrlTimeUtc: Optional[str] = None
    MessageId: Optional[str] = None
    TypeName: Literal["latest.price"] = "latest.price"
    Version: str = "000"

    _validator_from_g_node_alias = predicate_validator(
        "FromGNodeAlias", property_format.is_lrd_alias_format
    )

    _validator_from_g_node_instance_id = predicate_validator(
        "FromGNodeInstanceId", property_format.is_uuid_canonical_textual
    )

    @validator("PriceUnit")
    def _validator_price_unit(cls, v: MarketPriceUnit) -> MarketPriceUnit:
        return as_enum(v, MarketPriceUnit, MarketPriceUnit.USDPerMWh)

    _validator_market_slot_name = predicate_validator(
        "MarketSlotName", property_format.is_market_slot_name_lrd_format
    )

    @validator("IrlTimeUtc")
    def _validator_irl_time_utc(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        if not property_format.is_iso_format(v):
            raise ValueError(f"IrlTimeUtc {v} must have IsoFormat")
        return v

    @validator("MessageId")
    def _validator_message_id(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        if not property_format.is_uuid_canonical_textual(v):
            raise ValueError(f"MessageId {v} must have UuidCanonicalTextual")
        return v

    def as_dict(self) -> Dict[str, Any]:
        d = self.dict()
        del d["PriceUnit"]
        PriceUnit = as_enum(self.PriceUnit, MarketPriceUnit, MarketPriceUnit.default())
        d["PriceUnitGtEnumSymbol"] = MarketPriceUnitMap.local_to_type(PriceUnit)
        if d["IrlTimeUtc"] is None:
            del d["IrlTimeUtc"]
        if d["MessageId"] is None:
            del d["MessageId"]
        return d

    def as_type(self) -> str:
        return json.dumps(self.as_dict())


class LatestPrice_Maker:
    type_name = "latest.price"
    version = "000"

    def __init__(
        self,
        from_g_node_alias: str,
        from_g_node_instance_id: str,
        price_times1000: int,
        price_unit: MarketPriceUnit,
        market_slot_name: str,
        irl_time_utc: Optional[str],
        message_id: Optional[str],
    ):

        self.tuple = LatestPrice(
            FromGNodeAlias=from_g_node_alias,
            FromGNodeInstanceId=from_g_node_instance_id,
            PriceTimes1000=price_times1000,
            PriceUnit=price_unit,
            MarketSlotName=market_slot_name,
            IrlTimeUtc=irl_time_utc,
            MessageId=message_id,
            #
        )

    @classmethod
    def tuple_to_type(cls, tuple: LatestPrice) -> str:
        return tuple.as_type()

    @classmethod
    def type_to_tuple(cls, t: str) -> LatestPrice:
        try:
            d = json.loads(t)
        except TypeError:
            raise SchemaError("Type must be string or bytes!")
        if not isinstance(d, dict):
            raise SchemaError(f"Deserializing {t} must result in dict!")
        return cls.dict_to_tuple(d)

    @classmethod
    def dict_to_tuple(cls, d: dict[str, Any]) -> LatestPrice:
        d2 = dict(d)
        if "FromGNodeAlias" not in d2.keys():
            raise SchemaError(f"dict {d2} missing FromGNodeAlias")
        if "FromGNodeInstanceId" not in d2.keys():
            raise SchemaError(f"dict {d2} missing FromGNodeInstanceId")
        if "PriceTimes1000" not in d2.keys():
            raise SchemaError(f"dict {d2} missing PriceTimes1000")
        if "PriceUnitGtEnumSymbol" not in d2.keys():
            raise SchemaError(f"dict {d2} missing PriceUnitGtEnumSymbol")
        if d2["PriceUnitGtEnumSymbol"] in MarketPriceUnit000SchemaEnum.symbols:
            d2["PriceUnit"] = MarketPriceUnitMap.type_to_local(
                d2["PriceUnitGtEnumSymbol"]
            )
        else:
            d2["PriceUnit"] = MarketPriceUnit.default()
        if "MarketSlotName" not in d2.keys():
            raise SchemaError(f"dict {d2} missing MarketSlotName")
        if "IrlTimeUtc" not in d2.keys():
            d2["IrlTimeUtc"] = None
        if "MessageId" not in d2.keys():
            d2["MessageId"] = None
        if "TypeName" not in d2.keys():
            raise SchemaError(f"dict {d2} missing TypeName")

        return LatestPrice(
            FromGNodeAlias=d2["FromGNodeAlias"],
            FromGNodeInstanceId=d2["FromGNodeInstanceId"],
            PriceTimes1000=d2["PriceTimes1000"],
            PriceUnit=d2["PriceUnit"],
            MarketSlotName=d2["MarketSlotName"],
            IrlTimeUtc=d2["IrlTimeUtc"],
            MessageId=d2["MessageId"],
            TypeName=d2["TypeName"],
            Version="000",
        )
