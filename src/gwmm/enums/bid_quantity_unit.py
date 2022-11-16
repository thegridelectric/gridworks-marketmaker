from enum import auto
from typing import List

from fastapi_utils.enums import StrEnum


class BidQuantityUnit(StrEnum):
    AvgMW = auto()
    AvgkW = auto()

    @classmethod
    def default(cls) -> "BidQuantityUnit":
        return cls.AvgMW

    @classmethod
    def values(cls) -> List[str]:
        return [elt.value for elt in cls]
