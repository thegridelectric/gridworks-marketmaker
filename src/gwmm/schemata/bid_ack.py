"""Type bid.ack, version 000"""
import json
from typing import Any
from typing import Dict
from typing import Literal

from pydantic import BaseModel
from pydantic import validator

import gwmm.property_format as property_format
from gwmm.errors import SchemaError
from gwmm.property_format import predicate_validator


class BidAck(BaseModel):
    BidIdx: int  #
    BidUid: str  #
    MarketSlotName: str  #
    TypeName: Literal["bid.ack"] = "bid.ack"
    Version: str = "000"

    _validator_bid_uid = predicate_validator(
        "BidUid", property_format.is_uuid_canonical_textual
    )

    _validator_market_slot_name = predicate_validator(
        "MarketSlotName", property_format.is_market_slot_name_lrd_format
    )

    def as_dict(self) -> Dict[str, Any]:
        d = self.dict()
        return d

    def as_type(self) -> str:
        return json.dumps(self.as_dict())


class BidAck_Maker:
    type_name = "bid.ack"
    version = "000"

    def __init__(self, bid_idx: int, bid_uid: str, market_slot_name: str):

        self.tuple = BidAck(
            BidIdx=bid_idx,
            BidUid=bid_uid,
            MarketSlotName=market_slot_name,
            #
        )

    @classmethod
    def tuple_to_type(cls, tuple: BidAck) -> str:
        return tuple.as_type()

    @classmethod
    def type_to_tuple(cls, t: str) -> BidAck:
        try:
            d = json.loads(t)
        except TypeError:
            raise SchemaError("Type must be string or bytes!")
        if not isinstance(d, dict):
            raise SchemaError(f"Deserializing {t} must result in dict!")
        return cls.dict_to_tuple(d)

    @classmethod
    def dict_to_tuple(cls, d: dict[str, Any]) -> BidAck:
        d2 = dict(d)
        if "BidIdx" not in d2.keys():
            raise SchemaError(f"dict {d2} missing BidIdx")
        if "BidUid" not in d2.keys():
            raise SchemaError(f"dict {d2} missing BidUid")
        if "MarketSlotName" not in d2.keys():
            raise SchemaError(f"dict {d2} missing MarketSlotName")
        if "TypeName" not in d2.keys():
            raise SchemaError(f"dict {d2} missing TypeName")

        return BidAck(
            BidIdx=d2["BidIdx"],
            BidUid=d2["BidUid"],
            MarketSlotName=d2["MarketSlotName"],
            TypeName=d2["TypeName"],
            Version="000",
        )
