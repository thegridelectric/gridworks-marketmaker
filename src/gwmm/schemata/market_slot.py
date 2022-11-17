"""Type market.slot, version 000"""
import json
from typing import Any
from typing import Dict
from typing import Literal

from pydantic import BaseModel
from pydantic import validator

import gwmm.property_format as property_format
from gwmm.errors import SchemaError
from gwmm.property_format import predicate_validator
from gwmm.schemata.market_type_gt import MarketTypeGt
from gwmm.schemata.market_type_gt import MarketTypeGt_Maker


class MarketSlot(BaseModel):
    Type: MarketTypeGt  #
    MarketMakerAlias: str  #
    StartUnixS: int  #
    TypeName: Literal["market.slot"] = "market.slot"
    Version: str = "000"

    _validator_market_maker_alias = predicate_validator(
        "MarketMakerAlias", property_format.is_lrd_alias_format
    )

    _validator_start_unix_s = predicate_validator(
        "StartUnixS", property_format.is_reasonable_unix_time_s
    )

    def as_dict(self) -> Dict[str, Any]:
        d = self.dict()
        d["Type"] = self.Type.as_dict()
        return d

    def as_type(self) -> str:
        return json.dumps(self.as_dict())


class MarketSlot_Maker:
    type_name = "market.slot"
    version = "000"

    def __init__(self, type: MarketTypeGt, market_maker_alias: str, start_unix_s: int):

        self.tuple = MarketSlot(
            Type=type,
            MarketMakerAlias=market_maker_alias,
            StartUnixS=start_unix_s,
            #
        )

    @classmethod
    def tuple_to_type(cls, tuple: MarketSlot) -> str:
        return tuple.as_type()

    @classmethod
    def type_to_tuple(cls, t: str) -> MarketSlot:
        try:
            d = json.loads(t)
        except TypeError:
            raise SchemaError("Type must be string or bytes!")
        if not isinstance(d, dict):
            raise SchemaError(f"Deserializing {t} must result in dict!")
        return cls.dict_to_tuple(d)

    @classmethod
    def dict_to_tuple(cls, d: dict[str, Any]) -> MarketSlot:
        d2 = dict(d)
        if "Type" not in d2.keys():
            raise SchemaError(f"dict {d2} missing Type")
        if not isinstance(d2["Type"], dict):
            raise SchemaError(f"d['Type'] {d2['Type']} must be a MarketTypeGt!")
        type = MarketTypeGt_Maker.dict_to_tuple(d2["Type"])
        d2["Type"] = type
        if "MarketMakerAlias" not in d2.keys():
            raise SchemaError(f"dict {d2} missing MarketMakerAlias")
        if "StartUnixS" not in d2.keys():
            raise SchemaError(f"dict {d2} missing StartUnixS")
        if "TypeName" not in d2.keys():
            raise SchemaError(f"dict {d2} missing TypeName")

        return MarketSlot(
            Type=d2["Type"],
            MarketMakerAlias=d2["MarketMakerAlias"],
            StartUnixS=d2["StartUnixS"],
            TypeName=d2["TypeName"],
            Version="000",
        )
