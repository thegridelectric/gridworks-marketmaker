"""MarketMaker"""

import logging
import math
import random
import time
import uuid
from typing import Dict
from typing import List

import dotenv
import pendulum

import gwmm.config as config
import gwmm.utils as utils
from gwmm.data_classes.market_type import Rt60Gate30B
from gwmm.enums import MarketPriceUnit
from gwmm.enums import MarketTypeName
from gwmm.enums import MessageCategory
from gwmm.enums import UniverseType
from gwmm.market_maker_base import MarketMakerBase
from gwmm.schemata import AtnBid
from gwmm.schemata import LatestPrice_Maker
from gwmm.schemata import MarketBook
from gwmm.schemata import MarketMakerInfo_Maker
from gwmm.schemata import MarketPrice
from gwmm.schemata import MarketSlot
from gwmm.schemata import MarketSlot_Maker
from gwmm.schemata import MarketTypeGt
from gwmm.schemata import MarketTypeGt_Maker
from gwmm.schemata import ReceivedBid
from gwmm.schemata import SimTimestep
from gwmm.schemata.price_quantity_unitless import PriceQuantityUnitless
from gwmm.utils import RestfulResponse


LOG_FORMAT = (
    "%(levelname) -10s %(sasctime)s %(name) -30s %(funcName) "
    "-35s %(lineno) -5d: %(message)s"
)
LOGGER = logging.getLogger(__name__)

LOGGER.setLevel(logging.INFO)


class MarketMaker(MarketMakerBase):
    def __init__(
        self,
        settings: config.Settings = config.Settings(_env_file=dotenv.find_dotenv()),
    ):

        super().__init__(settings=settings)
        self.universe_type = UniverseType(self.settings.universe_type_value)
        self.mm_type: MarketTypeGt = MarketTypeGt_Maker.dc_to_tuple(Rt60Gate30B)
        self.market_types: List[MarketTypeGt] = [self.mm_type]

        self.market_type_names: List[MarketTypeName] = list(
            map(lambda x: x.Name, self.market_types)
        )
        sample_market = self.market_types[0]
        sample_market_name = f"{sample_market.Name}.{self.alias}"
        sample_market_slot_name = f"{sample_market_name}.1577836800"
        self.info = MarketMakerInfo_Maker(
            g_node_alias=self.alias,
            market_type_list=self.market_types,
            sample_market_name=sample_market_name,
            sample_market_slot_name=sample_market_slot_name,
        ).tuple

        self.slot_books: Dict[MarketTypeName, Dict[int, MarketBook]] = {
            self.mm_type.Name: {}
        }

        self.clearing_price: Dict[MarketTypeName, Dict[int, MarketPrice]] = {
            self.mm_type.Name: {}
        }
        LOGGER.info("MarketMaker initialized")

    def new_timestep(self, payload: SimTimestep) -> None:
        LOGGER.info(f"Got timestep. Time is now {self.time_utc_str()}")
        if self.latest_time_unix_s in self.slot_books[self.mm_type.Name].keys():
            book: MarketBook = self.slot_books[self.mm_type.Name][
                self.latest_time_unix_s
            ]
            try:
                self.clear_market(book)
            except:
                LOGGER.warning(f"failure with mm.clear_market(book) for book = {book}")
            LOGGER.info("Broadcasting Market Book")
            self.send_message(
                payload=book,
                message_category=MessageCategory.RabbitJsonBroadcast,
                radio_channel=self.mm_type.Name,
            )
        try:
            self.broadcast_latest_prices()
        except:
            LOGGER.warning("Failure: mm.broadcast_latest_prices()")
        try:
            self.update_slot_books()
        except:
            LOGGER.warning("Failure: mm.update_slot_books()")

    def timestep_received_again(self, payload: SimTimestep) -> None:
        LOGGER.info("Received timestep again")
        self.broadcast_latest_prices()

    def check_market_creds(self, payload: AtnBid) -> RestfulResponse:
        """
        payload.MarketFeeTxId needs to be a transaction id for a payment
        from the bidder's Algo address to the MarketMaker. Linking the bidder's
        GNodeInstance to the bidder's Algo address can be checked with a call
        to the World registry.

        The Market fee has to be sufficient (comparable to gas).

        The transaction has to have happened within a reasonable time (last hour).

        The bidder's Algo address must own a single TaTradingRights, and that
        must be the current TaTradingRights for the corresponding TerminalAsset.

        Most of this will be tucked into axioms checked by Bid_Maker, which
        will run for the bid generator as well and hopefully catch a lot of
        the mistakes before the bid is submitted.

        Args:
            payload (Bid): _description_

        Returns:
            RestfulResponse: HttpStatusCode 200 if everything checks out,
            otherwise 422 with Note explaining why.
        """
        tx_id = payload.MarketFeeTxId
        return RestfulResponse(Note="Has TaTradingRights; paid market fee")

    def atn_bid(self, payload: AtnBid) -> RestfulResponse:
        ts_ns = int(self.latest_time_unix_s * 10**9)
        if self.universe_type == UniverseType.Dev:
            ts_ns += random.uniform(-(10**6), 10**6)
        rr = self.check_market_creds(payload)
        if rr.HttpStatusCode > 200:
            return rr
        msn = payload.MarketSlotName
        slot: MarketSlot = utils.market_slot_from_name(msn)

        if slot.Type not in self.market_types:
            return RestfulResponse(
                Note=f"MarketType {slot.Type} not served by {self.alias}!",
                HttpStatusCode=422,
            )
        if slot.MarketMakerAlias != self.alias:
            return RestfulResponse(
                Note=f"{payload.MarketSlotName} not run by {self.alias}!",
                HttpStatusCode=422,
            )
        if slot.StartUnixS - self.latest_time_unix_s < slot.Type.DurationMinutes * 60:
            return RestfulResponse(
                Note=f"Missed gate closing. Bid not accepted",
                HttpStatusCode=422,
            )
        # this should be sharpened by checking that there are no MarketMakers
        # between the two - but that requires some GNodeTree mechanics in the MarketMaker
        if not payload.BidderAlias.startswith(self.alias):
            return RestfulResponse(
                Note=f"MarketMaker {self.alias} not an ancestor of {payload.BidderAlias}!"
            )
        # Move the following into AtnBid_Maker axioms:
        if payload.PriceUnit != slot.Type.PriceUnit:
            return RestfulResponse(
                Note=f"PriceUnit {payload.PriceUnit} must match market type "
                f"{slot.Type.Name} price_unit {slot.Type.PriceUnit}",
                HttpStatusCode=422,
            )
        if payload.QuantityUnit != slot.Type.QuantityUnit:
            return RestfulResponse(
                Note=f"QuantityUnit {payload.QuantityUnit} must match market type "
                f"{slot.Type} quantity_unit {slot.Type.QuantityUnit}",
                HttpStatusCode=422,
            )
        bid_list = payload.BidList
        if payload.InjectionIsPositive:
            demand_bid_list: List[PriceQuantityUnitless] = []
            for gen_pq in payload.BidList:
                demand_pq = PriceQuantityUnitless(
                    PriceTimes1000=gen_pq.PriceTimes1000,
                    QuantityTimes1000=-gen_pq.QuantityTimes1000,
                )
                demand_bid_list.append(demand_pq)
            bid_list = demand_bid_list
        rb = ReceivedBid(
            BidderAlias=payload.BidderAlias, BidList=bid_list, ReceivedTimeUnixNs=ts_ns
        )
        self.slot_books[slot.Type.Name][slot.StartUnixS].Bids.append(rb)
        friendly = pendulum.from_timestamp(ts_ns / 10**9).to_iso8601_string()
        return RestfulResponse(
            Note=f"Bid added to MarketBook! Received time {ts_ns} ns ({friendly})"
        )

    def broadcast_latest_prices(self) -> None:
        for market_type in self.market_types:
            starts: List[int] = list(self.slot_books[market_type.Name].keys())
            if len(starts) > 0:
                t = self.latest_time_unix_s
                latest_market_start = max(list(filter(lambda x: x <= t, starts)))
                slot = MarketSlot(
                    Type=market_type,
                    MarketMakerAlias=self.alias,
                    StartUnixS=latest_market_start,
                )
                slot_name = utils.name_from_market_slot(slot)

                try:
                    this_market_cp_dict: Dict[int, MarketPrice] = self.clearing_price[
                        market_type.Name
                    ]
                except:
                    raise Exception(
                        f"Expected to have clearing prices for {market_type.Name}!"
                    )
                try:
                    latest_market_price = this_market_cp_dict[slot.StartUnixS]
                except:
                    raise Exception(
                        f"Expected to have clearing prices for {slot_name}!"
                    )

                if slot.Type.PriceUnit != latest_market_price.Unit:
                    raise Exception(
                        f"Got slot.Type.PriceUnit {slot.Type.PriceUnit} "
                        f" and latest_market_price.Unit {latest_market_price.Unit}!"
                    )

                payload = LatestPrice_Maker(
                    from_g_node_alias=self.alias,
                    from_g_node_instance_id=self.settings.g_node_instance_id,
                    price_times1000=latest_market_price.ValueTimes1000,
                    price_unit=slot.Type.PriceUnit,
                    market_slot_name=slot_name,
                    message_id=str(uuid.uuid4()),
                    irl_time_utc=pendulum.from_timestamp(
                        time.time()
                    ).to_iso8601_string(),
                ).tuple
                LOGGER.info(
                    "Broadcasting price: "
                    f"{round(latest_market_price.ValueTimes1000 / 1000, 3)}"
                    f" {latest_market_price.Unit.value}"
                )
                self.send_message(
                    payload=payload,
                    message_category=MessageCategory.RabbitJsonBroadcast,
                    radio_channel=market_type.Name,
                )

    ###################
    # Managing books
    ###################

    def dev_solve_for_clearing_price(self, book: MarketBook) -> MarketPrice:

        return MarketPrice(
            ValueTimes1000=35354,
            Unit=MarketPriceUnit.USDPerMWh,
        )

    def solve_for_clearing_price(self, book: MarketBook) -> MarketPrice:
        if self.universe_type == UniverseType.Dev:
            return self.dev_solve_for_clearing_price(book)
        else:
            raise NotImplementedError

    def create_market_contracts(self, book: MarketBook, clearing_price: MarketPrice):
        pass

    def clear_market(self, book: MarketBook):
        price = self.solve_for_clearing_price(book)
        self.create_market_contracts(book, price)
        self.clearing_price[book.Slot.Type.Name][book.Slot.StartUnixS] = price

    def update_slot_books(self):
        for market_type in self.market_types:
            t = self.latest_time_unix_s
            gc_delta = market_type.GateClosingMinutes * 60
            market_delta = market_type.DurationMinutes * 60
            latest = math.floor(t / market_delta)
            next_to_open = math.ceil((t + gc_delta) / market_delta)
            for i in range(latest, next_to_open + 1):
                slot_start = i * market_delta
                slot = MarketSlot(
                    Type=market_type,
                    MarketMakerAlias=self.alias,
                    StartUnixS=slot_start,
                )
                if slot_start not in self.slot_books[market_type.Name].keys():
                    new_book = MarketBook(
                        Slot=slot,
                        Bids=[],
                    )
                    self.slot_books[market_type.Name][slot_start] = new_book

    ###################
    # helpers
    ###################

    def latest_market_slot_name(self, market_type: MarketTypeGt) -> str:
        return f"{market_type.Name}.{self.alias}.{self.latest_slot_start(market_type)}"

    def latest_slot_start(self, market_type: MarketTypeGt) -> int:
        t = self.latest_time_unix_s
        market_delta = market_type.DurationMinutes * 60
        return math.floor(t / market_delta) * market_delta

    def last_slot_start(self, market_type: MarketTypeGt) -> int:
        if int(self.latest_time_unix_s) == self.latest_slot_start(market_type):
            return self.latest_slot_start(market_type) - self.market_slot_duration_s(
                market_type
            )
        else:
            return self.latest_slot_start(market_type)

    def next_slot_start(self, market_type: MarketTypeGt) -> int:
        return self.last_slot_start(market_type) + self.market_slot_duration_s(
            market_type
        )

    def market_slot_duration_s(self, market_type: MarketTypeGt) -> int:
        return market_type.DurationMinutes * 60
