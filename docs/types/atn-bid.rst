AtnBid
==========================
Python pydantic class corresponding to  json type ```atn.bid```.

.. autoclass:: gwmm.types.AtnBid
    :members:

**BidderAlias**:
    - Description:
    - Format: LeftRightDot

**BidderGNodeInstanceId**:
    - Description:
    - Format: UuidCanonicalTextual

**MarketSlotName**:
    - Description:
    - Format: MarketSlotNameLrdFormat

**PqPairs**:
    - Description: Price Quantity Pairs. The list of Price Quantity Pairs making up the bid. The units are provided by the AtnBid.PriceUnit and AtnBid.QuantityUnit.

**InjectionIsPositive**:
    - Description:

**PriceUnit**:
    - Description:

**QuantityUnit**:
    - Description:

**SignedMarketFeeTxn**:
    - Description:
    - Format: AlgoMsgPackEncoded

.. autoclass:: gwmm.types.atn_bid.check_is_uuid_canonical_textual
    :members:


.. autoclass:: gwmm.types.atn_bid.check_is_left_right_dot
    :members:


.. autoclass:: gwmm.types.atn_bid.check_is_market_slot_name_lrd_format
    :members:


.. autoclass:: gwmm.types.atn_bid.check_is_algo_address_string_format
    :members:


.. autoclass:: gwmm.types.AtnBid_Maker
    :members:
