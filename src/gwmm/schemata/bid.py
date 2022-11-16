"""Type bid, version 000"""
import json
from enum import auto
from typing import Any
from typing import Dict
from typing import List
from typing import Literal

from fastapi_utils.enums import StrEnum
from pydantic import BaseModel
from pydantic import validator

import gwmm.property_format as property_format
from gwmm.enums import BidPriceUnit
from gwmm.enums import BidQuantityUnit
from gwmm.errors import SchemaError
from gwmm.message import as_enum
from gwmm.property_format import predicate_validator
from gwmm.schemata.price_quantity_unitless import PriceQuantityUnitless
from gwmm.schemata.price_quantity_unitless import PriceQuantityUnitless_Maker


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


class Bid(BaseModel):
    BidderAlias: str  #
    BidderGNodeId: str  #
    MarketSlotName: str  #
    BidList: List[PriceQuantityUnitless]
    #
    InjectionIsPositive: bool  #
    PriceUnit: BidPriceUnit  #
    QuantityUnit: BidQuantityUnit  #
    TypeName: Literal["bid"] = "bid"
    Version: str = "000"

    _validator_bidder_alias = predicate_validator(
        "BidderAlias", property_format.is_lrd_alias_format
    )

    _validator_bidder_g_node_id = predicate_validator(
        "BidderGNodeId", property_format.is_uuid_canonical_textual
    )

    _validator_market_slot_name = predicate_validator(
        "MarketSlotName", property_format.is_market_slot_name_lrd_format
    )

    @validator("BidList")
    def _validator_bid_list(cls, v: List) -> List:
        for elt in v:
            if not isinstance(elt, PriceQuantityUnitless):
                raise ValueError(
                    f"elt {elt} of BidList must have type PriceQuantityUnitless."
                )
        return v

    @validator("PriceUnit")
    def _validator_price_unit(cls, v: BidPriceUnit) -> BidPriceUnit:
        return as_enum(v, BidPriceUnit, BidPriceUnit.USDPerMWh)

    @validator("QuantityUnit")
    def _validator_quantity_unit(cls, v: BidQuantityUnit) -> BidQuantityUnit:
        return as_enum(v, BidQuantityUnit, BidQuantityUnit.AvgMW)

    def as_dict(self) -> Dict[str, Any]:
        d = self.dict()

        # Recursively call as_dict() for the SubTypes
        bid_list = []
        for elt in self.BidList:
            bid_list.append(elt.as_dict())
        d["BidList"] = bid_list
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


class Bid_Maker:
    type_name = "bid"
    version = "000"

    def __init__(
        self,
        bidder_alias: str,
        bidder_g_node_id: str,
        market_slot_name: str,
        bid_list: List[PriceQuantityUnitless],
        injection_is_positive: bool,
        price_unit: BidPriceUnit,
        quantity_unit: BidQuantityUnit,
    ):

        self.tuple = Bid(
            BidderAlias=bidder_alias,
            BidderGNodeId=bidder_g_node_id,
            MarketSlotName=market_slot_name,
            BidList=bid_list,
            InjectionIsPositive=injection_is_positive,
            PriceUnit=price_unit,
            QuantityUnit=quantity_unit,
            #
        )

    @classmethod
    def tuple_to_type(cls, tuple: Bid) -> str:
        return tuple.as_type()

    @classmethod
    def type_to_tuple(cls, t: str) -> Bid:
        try:
            d = json.loads(t)
        except TypeError:
            raise SchemaError("Type must be string or bytes!")
        if not isinstance(d, dict):
            raise SchemaError(f"Deserializing {t} must result in dict!")
        return cls.dict_to_tuple(d)

    @classmethod
    def dict_to_tuple(cls, d: dict[str, Any]) -> Bid:
        d2 = dict(d)
        if "BidderAlias" not in d2.keys():
            raise SchemaError(f"dict {d2} missing BidderAlias")
        if "BidderGNodeId" not in d2.keys():
            raise SchemaError(f"dict {d2} missing BidderGNodeId")
        if "MarketSlotName" not in d2.keys():
            raise SchemaError(f"dict {d2} missing MarketSlotName")
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
        if "InjectionIsPositive" not in d2.keys():
            raise SchemaError(f"dict {d2} missing InjectionIsPositive")
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
        if "TypeName" not in d2.keys():
            raise SchemaError(f"dict {d2} missing TypeName")

        return Bid(
            BidderAlias=d2["BidderAlias"],
            BidderGNodeId=d2["BidderGNodeId"],
            MarketSlotName=d2["MarketSlotName"],
            BidList=d2["BidList"],
            InjectionIsPositive=d2["InjectionIsPositive"],
            PriceUnit=d2["PriceUnit"],
            QuantityUnit=d2["QuantityUnit"],
            TypeName=d2["TypeName"],
            Version="000",
        )
