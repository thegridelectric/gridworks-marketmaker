from typing import Dict

from pydantic import BaseModel

from gwmm.enums import BidPriceUnit
from gwmm.enums import BidQuantityUnit
from gwmm.enums import MarketTypeAlias
from gwmm.enums import RecognizedCurrencyUnit


class MarketType:
    by_id: Dict[MarketTypeAlias, "MarketType"] = {}

    def __new__(cls, alias: MarketTypeAlias, *args, **kwargs) -> "MarketType":  # type: ignore
        try:
            return cls.by_id[alias]
        except KeyError:
            instance = super().__new__(cls)
            cls.by_id[alias] = instance
            return instance

    def __init__(
        self,
        alias: MarketTypeAlias,
        duration_minutes: int,
        gate_closing_minutes: int,
        price_unit: BidPriceUnit = BidPriceUnit.USDPerMWh,
        quantity_unit: BidQuantityUnit = BidQuantityUnit.AvgMW,
        currency_unit: RecognizedCurrencyUnit = RecognizedCurrencyUnit.USD,
    ):
        self.alias = alias
        self.duration_minutes = duration_minutes
        self.gate_closing_minutes = gate_closing_minutes
        self.price_unit = price_unit
        self.quantity_unit = quantity_unit
        self.currency_unit = currency_unit

    def __repr__(self) -> str:
        s = f"MarketType {self.alias}: duration {self.duration_minutes} m, gate closing {self.gate_closing_minutes} m, {self.price_unit.value}, {self.quantity_unit.value}"
        return s


Rt5Gate5 = MarketType(
    alias=MarketTypeAlias.rt5gate5, duration_minutes=5, gate_closing_minutes=5
)

Rt15Gate5 = MarketType(
    alias=MarketTypeAlias.rt15gate5, duration_minutes=15, gate_closing_minutes=5
)

Rt30Gate5 = MarketType(
    alias=MarketTypeAlias.rt30gate5, duration_minutes=30, gate_closing_minutes=5
)

Rt60Gate5 = MarketType(
    alias=MarketTypeAlias.rt60gate5, duration_minutes=60, gate_closing_minutes=5
)

Rt60Gate30 = MarketType(
    alias=MarketTypeAlias.rt60gate30, duration_minutes=60, gate_closing_minutes=30
)

Rt60Gate30B = MarketType(
    alias=MarketTypeAlias.rt60gate30b,
    duration_minutes=60,
    gate_closing_minutes=30,
    quantity_unit=BidQuantityUnit.AvgkW,
)

Da60 = MarketType(
    alias=MarketTypeAlias.da60, duration_minutes=60, gate_closing_minutes=1440
)
