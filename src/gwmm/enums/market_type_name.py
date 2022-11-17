from enum import auto
from typing import List

from fastapi_utils.enums import StrEnum


class MarketTypeName(StrEnum):
    unknown = auto()
    rt5gate5 = auto()
    rt60gate5 = auto()
    da60 = auto()
    rt60gate30 = auto()
    rt15gate5 = auto()
    rt30gate5 = auto()
    rt60gate30b = auto()

    @classmethod
    def default(cls) -> "MarketTypeName":
        return cls.unknown

    @classmethod
    def values(cls) -> List[str]:
        return [elt.value for elt in cls]
