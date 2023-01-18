"""Type bid.ack, version 000"""
import json
from typing import Any
from typing import Dict
from typing import Literal

from gridworks.errors import SchemaError
from pydantic import BaseModel
from pydantic import Field
from pydantic import validator


def check_is_uuid_canonical_textual(v: str) -> None:
    """
    UuidCanonicalTextual format:  A string of hex words separated by hyphens
    of length 8-4-4-4-12.

    Raises:
        ValueError: if not UuidCanonicalTextual format
    """
    try:
        x = v.split("-")
    except AttributeError as e:
        raise ValueError(f"Failed to split on -: {e}")
    if len(x) != 5:
        raise ValueError(f"{v} split by '-' did not have 5 words")
    for hex_word in x:
        try:
            int(hex_word, 16)
        except ValueError:
            raise ValueError(f"Words of {v} are not all hex")
    if len(x[0]) != 8:
        raise ValueError(f"{v} word lengths not 8-4-4-4-12")
    if len(x[1]) != 4:
        raise ValueError(f"{v} word lengths not 8-4-4-4-12")
    if len(x[2]) != 4:
        raise ValueError(f"{v} word lengths not 8-4-4-4-12")
    if len(x[3]) != 4:
        raise ValueError(f"{v} word lengths not 8-4-4-4-12")
    if len(x[4]) != 12:
        raise ValueError(f"{v} word lengths not 8-4-4-4-12")


def check_is_market_type_name_lrd_format(v: str) -> None:
    from gwmm.enums import MarketTypeName

    try:
        x = v.split(".")
    except AttributeError:
        raise ValueError(f"{v} failed to split on '.'")
    if not x[0] in MarketTypeName.values():
        raise ValueError(f"{v} not recognized MarketType")
    g_node_alias = ".".join(x[1:])
    check_is_left_right_dot(g_node_alias)


def check_is_market_slot_name_lrd_format(v: str) -> None:
    """
    MaketSlotNameLrdFormat: the format of a MarketSlotName.
      - The first word must be a MarketTypeName
      - The last word (unix time of market slot start) must
      be a 10-digit integer divisible by 300 (i.e. all MarketSlots
      start at the top of 5 minutes)
      - More strictly, the last word must be the start of a
      MarketSlot for that MarketType (i.e. divisible by 3600
      for hourly markets)
      - The middle words have LeftRightDot format (GNodeAlias
      of the MarketMaker)
    Example: rt60gate5.d1.isone.ver.keene.1673539200

    """
    from gwmm.data_classes.market_type import MarketType

    try:
        x = v.split(".")
    except AttributeError:
        raise ValueError(f"{v} failed to split on '.'")
    slot_start = x[-1]
    if len(slot_start) != 10:
        raise ValueError(f"slot start {slot_start} not of length 10")
    try:
        slot_start = int(slot_start)
    except ValueError:
        raise ValueError(f"slot start {slot_start} not an int")
    if slot_start % 300 != 0:
        raise ValueError(f"slot start {slot_start} not a multiple of 300")

    market_type_name_lrd = ".".join(x[:-1])
    try:
        check_is_market_type_name_lrd_format(market_type_name_lrd)
    except ValueError as e:
        raise ValueError(f"e")

    market_type = MarketType.by_id[market_type_name_lrd.split(".")[0]]
    if not slot_start % (market_type.duration_minutes * 60) == 0:
        raise ValueError(
            f"market_slot_start_s mod {(market_type.duration_minutes * 60)} must be 0"
        )


class BidAck(BaseModel):
    """Bid ack.

    This is not a legally binding contract (see accepted.bid). Designed for a POST response.
    """

    BidIdx: int = Field(
        title="BidIdx",
    )
    BidUid: str = Field(
        title="BidUid",
    )
    MarketSlotName: str = Field(
        title="MarketSlotName",
    )
    TypeName: Literal["bid.ack"] = "bid.ack"
    Version: str = "000"

    @validator("BidUid")
    def _check_bid_uid(cls, v: str) -> str:
        try:
            check_is_uuid_canonical_textual(v)
        except ValueError as e:
            raise ValueError(
                f"BidUid failed UuidCanonicalTextual format validation: {e}"
            )
        return v

    @validator("MarketSlotName")
    def _check_market_slot_name(cls, v: str) -> str:
        try:
            check_is_market_slot_name_lrd_format(v)
        except ValueError as e:
            raise ValueError(
                f"MarketSlotName failed MarketSlotNameLrdFormat format validation: {e}"
            )
        return v

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
        """
        Given a Python class object, returns the serialized JSON type object
        """
        return tuple.as_type()

    @classmethod
    def type_to_tuple(cls, t: str) -> BidAck:
        """
        Given a serialized JSON type object, returns the Python class object
        """
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
