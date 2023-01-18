"""Type market.maker.info, version 000"""
import json
from typing import Any
from typing import Dict
from typing import List
from typing import Literal

from gridworks.errors import SchemaError
from pydantic import BaseModel
from pydantic import Field
from pydantic import validator

from gwmm.types.market_type_gt import MarketTypeGt
from gwmm.types.market_type_gt import MarketTypeGt_Maker


def check_is_left_right_dot(v: str) -> None:
    """
    LeftRightDot format: Lowercase alphanumeric words separated by periods,
    most significant word (on the left) starting with an alphabet character.

    Raises:
        ValueError: if not LeftRightDot format
    """
    from typing import List

    try:
        x: List[str] = v.split(".")
    except:
        raise ValueError(f"Failed to seperate {v} into words with split'.'")
    first_word = x[0]
    first_char = first_word[0]
    if not first_char.isalpha():
        raise ValueError(f"Most significant word of {v} must start with alphabet char.")
    for word in x:
        if not word.isalnum():
            raise ValueError(f"words of {v} split by by '.' must be alphanumeric.")
    if not v.islower():
        raise ValueError(f"All characters of {v} must be lowercase.")


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


class MarketMakerInfo(BaseModel):
    """ """

    GNodeAlias: str = Field(
        title="GNodeAlias",
    )
    MarketTypeList: List[MarketTypeGt] = Field(
        title="MarketTypeList",
    )
    SampleMarketName: str = Field(
        title="SampleMarketName",
    )
    SampleMarketSlotName: str = Field(
        title="SampleMarketSlotName",
    )
    TypeName: Literal["market.maker.info"] = "market.maker.info"
    Version: str = "000"

    @validator("GNodeAlias")
    def _check_g_node_alias(cls, v: str) -> str:
        try:
            check_is_left_right_dot(v)
        except ValueError as e:
            raise ValueError(f"GNodeAlias failed LeftRightDot format validation: {e}")
        return v

    @validator("MarketTypeList")
    def _check_market_type_list(cls, v: List) -> List:
        for elt in v:
            if not isinstance(elt, MarketTypeGt):
                raise ValueError(
                    f"elt {elt} of MarketTypeList must have type MarketTypeGt."
                )
        return v

    @validator("SampleMarketSlotName")
    def _check_sample_market_slot_name(cls, v: str) -> str:
        try:
            check_is_market_slot_name_lrd_format(v)
        except ValueError as e:
            raise ValueError(
                f"SampleMarketSlotName failed MarketSlotNameLrdFormat format validation: {e}"
            )
        return v

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
        """
        Given a Python class object, returns the serialized JSON type object
        """
        return tuple.as_type()

    @classmethod
    def type_to_tuple(cls, t: str) -> MarketMakerInfo:
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
