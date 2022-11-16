from enum import auto
from typing import List

from fastapi_utils.enums import StrEnum


class RecognizedCurrencyUnit(StrEnum):
    UNKNOWN = auto()
    USD = auto()
    GBP = auto()

    @classmethod
    def default(cls) -> "RecognizedCurrencyUnit":
        return cls.UNKNOWN

    @classmethod
    def values(cls) -> List[str]:
        return [elt.value for elt in cls]
