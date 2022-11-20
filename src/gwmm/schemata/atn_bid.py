"""Type atn.bid, version 000"""
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
from gwmm.enums import MarketPriceUnit
from gwmm.enums import MarketQuantityUnit
from gwmm.errors import SchemaError
from gwmm.message import as_enum
from gwmm.property_format import predicate_validator
from gwmm.schemata.price_quantity_unitless import PriceQuantityUnitless
from gwmm.schemata.price_quantity_unitless import PriceQuantityUnitless_Maker


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


class MarketQuantityUnit000SchemaEnum:
    enum_name: str = "market.quantity.unit.000"
    symbols: List[str] = [
        "00000000",
        "c272f3b3",
    ]

    @classmethod
    def is_symbol(cls, candidate: str) -> bool:
        if candidate in cls.symbols:
            return True
        return False


class MarketQuantityUnit000(StrEnum):
    AvgMW = auto()
    AvgkW = auto()

    @classmethod
    def default(cls) -> "MarketQuantityUnit000":
        return cls.AvgMW

    @classmethod
    def values(cls) -> List[str]:
        return [elt.value for elt in cls]


class MarketQuantityUnitMap:
    @classmethod
    def type_to_local(cls, symbol: str) -> MarketQuantityUnit:
        if not MarketQuantityUnit000SchemaEnum.is_symbol(symbol):
            raise SchemaError(f"{symbol} must belong to MarketQuantityUnit000 symbols")
        versioned_enum = cls.type_to_versioned_enum_dict[symbol]
        return as_enum(versioned_enum, MarketQuantityUnit, MarketQuantityUnit.default())

    @classmethod
    def local_to_type(cls, market_quantity_unit: MarketQuantityUnit) -> str:
        if not isinstance(market_quantity_unit, MarketQuantityUnit):
            raise SchemaError(
                f"{market_quantity_unit} must be of type {MarketQuantityUnit}"
            )
        versioned_enum = as_enum(
            market_quantity_unit, MarketQuantityUnit000, MarketQuantityUnit000.default()
        )
        return cls.versioned_enum_to_type_dict[versioned_enum]

    type_to_versioned_enum_dict: Dict[str, MarketQuantityUnit000] = {
        "00000000": MarketQuantityUnit000.AvgMW,
        "c272f3b3": MarketQuantityUnit000.AvgkW,
    }

    versioned_enum_to_type_dict: Dict[MarketQuantityUnit000, str] = {
        MarketQuantityUnit000.AvgMW: "00000000",
        MarketQuantityUnit000.AvgkW: "c272f3b3",
    }


class AtnBid(BaseModel):
    BidderAlias: str  #
    BidderGNodeInstanceId: str  #
    MarketSlotName: str  #
    BidList: List[PriceQuantityUnitless]  #
    InjectionIsPositive: bool = False  #
    PriceUnit: MarketPriceUnit = MarketPriceUnit.USDPerMWh  #
    QuantityUnit: MarketQuantityUnit = MarketQuantityUnit.AvgMW  #
    SignedMarketFeeTxn: str  #
    TypeName: Literal["atn.bid"] = "atn.bid"
    Version: str = "000"

    _validator_bidder_alias = predicate_validator(
        "BidderAlias", property_format.is_lrd_alias_format
    )

    _validator_bidder_g_node_instance_id = predicate_validator(
        "BidderGNodeInstanceId", property_format.is_uuid_canonical_textual
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
    def _validator_price_unit(cls, v: MarketPriceUnit) -> MarketPriceUnit:
        return as_enum(v, MarketPriceUnit, MarketPriceUnit.USDPerMWh)

    @validator("QuantityUnit")
    def _validator_quantity_unit(cls, v: MarketQuantityUnit) -> MarketQuantityUnit:
        return as_enum(v, MarketQuantityUnit, MarketQuantityUnit.AvgMW)

    _validator_signed_market_fee_txn = predicate_validator(
        "SignedMarketFeeTxn", property_format.is_algo_msg_pack_encoded
    )

    def as_dict(self) -> Dict[str, Any]:
        d = self.dict()

        # Recursively call as_dict() for the SubTypes
        bid_list = []
        for elt in self.BidList:
            bid_list.append(elt.as_dict())
        d["BidList"] = bid_list
        del d["PriceUnit"]
        PriceUnit = as_enum(self.PriceUnit, MarketPriceUnit, MarketPriceUnit.default())
        d["PriceUnitGtEnumSymbol"] = MarketPriceUnitMap.local_to_type(PriceUnit)
        del d["QuantityUnit"]
        QuantityUnit = as_enum(
            self.QuantityUnit, MarketQuantityUnit, MarketQuantityUnit.default()
        )
        d["QuantityUnitGtEnumSymbol"] = MarketQuantityUnitMap.local_to_type(
            QuantityUnit
        )
        return d

    def as_type(self) -> str:
        return json.dumps(self.as_dict())


class AtnBid_Maker:
    type_name = "atn.bid"
    version = "000"

    def __init__(
        self,
        bidder_alias: str,
        bidder_g_node_instance_id: str,
        market_slot_name: str,
        bid_list: List[PriceQuantityUnitless],
        injection_is_positive: bool,
        price_unit: MarketPriceUnit,
        quantity_unit: MarketQuantityUnit,
        signed_market_fee_txn: str,
    ):

        self.tuple = AtnBid(
            BidderAlias=bidder_alias,
            BidderGNodeInstanceId=bidder_g_node_instance_id,
            MarketSlotName=market_slot_name,
            BidList=bid_list,
            InjectionIsPositive=injection_is_positive,
            PriceUnit=price_unit,
            QuantityUnit=quantity_unit,
            SignedMarketFeeTxn=signed_market_fee_txn,
            #
        )

    @classmethod
    def tuple_to_type(cls, tuple: AtnBid) -> str:
        return tuple.as_type()

    @classmethod
    def type_to_tuple(cls, t: str) -> AtnBid:
        try:
            d = json.loads(t)
        except TypeError:
            raise SchemaError("Type must be string or bytes!")
        if not isinstance(d, dict):
            raise SchemaError(f"Deserializing {t} must result in dict!")
        return cls.dict_to_tuple(d)

    @classmethod
    def dict_to_tuple(cls, d: dict[str, Any]) -> AtnBid:
        d2 = dict(d)
        if "BidderAlias" not in d2.keys():
            raise SchemaError(f"dict {d2} missing BidderAlias")
        if "BidderGNodeInstanceId" not in d2.keys():
            raise SchemaError(f"dict {d2} missing BidderGNodeInstanceId")
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
        if d2["PriceUnitGtEnumSymbol"] in MarketPriceUnit000SchemaEnum.symbols:
            d2["PriceUnit"] = MarketPriceUnitMap.type_to_local(
                d2["PriceUnitGtEnumSymbol"]
            )
        else:
            d2["PriceUnit"] = MarketPriceUnit.default()
        if "QuantityUnitGtEnumSymbol" not in d2.keys():
            raise SchemaError(f"dict {d2} missing QuantityUnitGtEnumSymbol")
        if d2["QuantityUnitGtEnumSymbol"] in MarketQuantityUnit000SchemaEnum.symbols:
            d2["QuantityUnit"] = MarketQuantityUnitMap.type_to_local(
                d2["QuantityUnitGtEnumSymbol"]
            )
        else:
            d2["QuantityUnit"] = MarketQuantityUnit.default()
        if "SignedMarketFeeTxn" not in d2.keys():
            raise SchemaError(f"dict {d2} missing SignedMarketFeeTxn")
        if "TypeName" not in d2.keys():
            raise SchemaError(f"dict {d2} missing TypeName")

        return AtnBid(
            BidderAlias=d2["BidderAlias"],
            BidderGNodeInstanceId=d2["BidderGNodeInstanceId"],
            MarketSlotName=d2["MarketSlotName"],
            BidList=d2["BidList"],
            InjectionIsPositive=d2["InjectionIsPositive"],
            PriceUnit=d2["PriceUnit"],
            QuantityUnit=d2["QuantityUnit"],
            SignedMarketFeeTxn=d2["SignedMarketFeeTxn"],
            TypeName=d2["TypeName"],
            Version="000",
        )
