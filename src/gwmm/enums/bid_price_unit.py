from enum import auto
from typing import List

from fastapi_utils.enums import StrEnum


class BidPriceUnit(StrEnum):
    USDPerMWh = auto()

    @classmethod
    def default(cls) -> "BidPriceUnit":
        return cls.USDPerMWh

    @classmethod
    def values(cls) -> List[str]:
        return [elt.value for elt in cls]
