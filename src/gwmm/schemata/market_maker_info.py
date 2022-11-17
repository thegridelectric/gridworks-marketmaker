"""Type market.maker.info, version 000"""
import json
from typing import Any
from typing import Dict
from typing import List
from typing import Literal

from pydantic import BaseModel
from pydantic import validator

import gwmm.property_format as property_format
from gwmm.errors import SchemaError
from gwmm.property_format import predicate_validator
from gwmm.schemata.market_type_gt import MarketTypeGt
from gwmm.schemata.market_type_gt import MarketTypeGt_Maker


class MarketMakerInfo(BaseModel):
    GNodeAlias: str  #
    MarketTypeList: List[MarketTypeGt]  #
    SampleMarketName: str  #
    SampleMarketSlotName: str  #
    TypeName: Literal["market.maker.info"] = "market.maker.info"
    Version: str = "000"

    _validator_g_node_alias = predicate_validator(
        "GNodeAlias", property_format.is_lrd_alias_format
    )

    @validator("MarketTypeList")
    def _validator_market_type_list(cls, v: List) -> List:
        for elt in v:
            if not isinstance(elt, MarketTypeGt):
                raise ValueError(
                    f"elt {elt} of MarketTypeList must have type MarketTypeGt."
                )
        return v

    _validator_sample_market_slot_name = predicate_validator(
        "SampleMarketSlotName", property_format.is_market_slot_name_lrd_format
    )

    def as_dict(self) -> Dict[str, Any]:
        d = self.dict()

        # Recursively call as_dict() for the SubTypes
        market_type_list = []
        for elt in self.MarketTypeList:
            market_type_list.append(elt.as_dict())
        d["MarketTypeList"] = market_type_list
        return d

    def as_type(self) -> str:
        return json.dumps(self.as_dict())


class MarketMakerInfo_Maker:
    type_name = "market.maker.info"
    version = "000"

    def __init__(
        self,
        g_node_alias: str,
        market_type_list: List[MarketTypeGt],
        sample_market_name: str,
        sample_market_slot_name: str,
    ):

        self.tuple = MarketMakerInfo(
            GNodeAlias=g_node_alias,
            MarketTypeList=market_type_list,
            SampleMarketName=sample_market_name,
            SampleMarketSlotName=sample_market_slot_name,
            #
        )

    @classmethod
    def tuple_to_type(cls, tuple: MarketMakerInfo) -> str:
        return tuple.as_type()

    @classmethod
    def type_to_tuple(cls, t: str) -> MarketMakerInfo:
        try:
            d = json.loads(t)
        except TypeError:
            raise SchemaError("Type must be string or bytes!")
        if not isinstance(d, dict):
            raise SchemaError(f"Deserializing {t} must result in dict!")
        return cls.dict_to_tuple(d)

    @classmethod
    def dict_to_tuple(cls, d: dict[str, Any]) -> MarketMakerInfo:
        d2 = dict(d)
        if "GNodeAlias" not in d2.keys():
            raise SchemaError(f"dict {d2} missing GNodeAlias")
        if "MarketTypeList" not in d2.keys():
            raise SchemaError(f"dict {d2} missing MarketTypeList")
        market_type_list = []
        if not isinstance(d2["MarketTypeList"], List):
            raise SchemaError("MarketTypeList must be a List!")
        for elt in d2["MarketTypeList"]:
            if not isinstance(elt, dict):
                raise SchemaError(
                    f"elt {elt} of MarketTypeList must be "
                    "MarketTypeGt but not even a dict!"
                )
            market_type_list.append(MarketTypeGt_Maker.dict_to_tuple(elt))
        d2["MarketTypeList"] = market_type_list
        if "SampleMarketName" not in d2.keys():
            raise SchemaError(f"dict {d2} missing SampleMarketName")
        if "SampleMarketSlotName" not in d2.keys():
            raise SchemaError(f"dict {d2} missing SampleMarketSlotName")
        if "TypeName" not in d2.keys():
            raise SchemaError(f"dict {d2} missing TypeName")

        return MarketMakerInfo(
            GNodeAlias=d2["GNodeAlias"],
            MarketTypeList=d2["MarketTypeList"],
            SampleMarketName=d2["SampleMarketName"],
            SampleMarketSlotName=d2["SampleMarketSlotName"],
            TypeName=d2["TypeName"],
            Version="000",
        )
