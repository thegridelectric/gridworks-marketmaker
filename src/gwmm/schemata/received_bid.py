"""Type received.bid, version 000"""
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
from gwmm.schemata.price_quantity_unitless import PriceQuantityUnitless
from gwmm.schemata.price_quantity_unitless import PriceQuantityUnitless_Maker


class ReceivedBid(BaseModel):
    BidderAlias: str  #
    BidList: List[PriceQuantityUnitless]  #
    ReceivedTimeUnixNs: int  #
    TypeName: Literal["received.bid"] = "received.bid"
    Version: str = "000"

    _validator_bidder_alias = predicate_validator(
        "BidderAlias", property_format.is_lrd_alias_format
    )

    @validator("BidList")
    def _validator_bid_list(cls, v: List) -> List:
        for elt in v:
            if not isinstance(elt, PriceQuantityUnitless):
                raise ValueError(
                    f"elt {elt} of BidList must have type PriceQuantityUnitless."
                )
        return v

    def as_dict(self) -> Dict[str, Any]:
        d = self.dict()

        # Recursively call as_dict() for the SubTypes
        bid_list = []
        for elt in self.BidList:
            bid_list.append(elt.as_dict())
        d["BidList"] = bid_list
        return d

    def as_type(self) -> str:
        return json.dumps(self.as_dict())


class ReceivedBid_Maker:
    type_name = "received.bid"
    version = "000"

    def __init__(
        self,
        bidder_alias: str,
        bid_list: List[PriceQuantityUnitless],
        received_time_unix_ns: int,
    ):

        self.tuple = ReceivedBid(
            BidderAlias=bidder_alias,
            BidList=bid_list,
            ReceivedTimeUnixNs=received_time_unix_ns,
            #
        )

    @classmethod
    def tuple_to_type(cls, tuple: ReceivedBid) -> str:
        return tuple.as_type()

    @classmethod
    def type_to_tuple(cls, t: str) -> ReceivedBid:
        try:
            d = json.loads(t)
        except TypeError:
            raise SchemaError("Type must be string or bytes!")
        if not isinstance(d, dict):
            raise SchemaError(f"Deserializing {t} must result in dict!")
        return cls.dict_to_tuple(d)

    @classmethod
    def dict_to_tuple(cls, d: dict[str, Any]) -> ReceivedBid:
        d2 = dict(d)
        if "BidderAlias" not in d2.keys():
            raise SchemaError(f"dict {d2} missing BidderAlias")
        if "BidList" not in d2.keys():
            raise SchemaError(f"dict {d2} missing BidList")
        bid_list = []
        if not isinstance(d2["BidList"], List):
            raise SchemaError("BidList must be a List!")
        for elt in d2["BidList"]:
            if not isinstance(elt, dict):
                raise SchemaError(
                    f"elt {elt} of BidList must be "
                    "PriceQuantityUnitless but not even a dict!"
                )
            bid_list.append(PriceQuantityUnitless_Maker.dict_to_tuple(elt))
        d2["BidList"] = bid_list
        if "ReceivedTimeUnixNs" not in d2.keys():
            raise SchemaError(f"dict {d2} missing ReceivedTimeUnixNs")
        if "TypeName" not in d2.keys():
            raise SchemaError(f"dict {d2} missing TypeName")

        return ReceivedBid(
            BidderAlias=d2["BidderAlias"],
            BidList=d2["BidList"],
            ReceivedTimeUnixNs=d2["ReceivedTimeUnixNs"],
            TypeName=d2["TypeName"],
            Version="000",
        )
