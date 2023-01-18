

SDK for `gridworks-atn <https://pypi.org/project/gridworks-atn/>`_  Types
===========================================================================

The Python classes enumerated below provide an interpretation of gridworks-atn
type instances (serialized JSON) as Python objects. Types are the building
blocks for all GridWorks APIs. You can read more about how they work
`here <https://gridworks.readthedocs.io/en/latest/api-sdk-abi.html>`_, and
examine their API specifications `here <apis/types.html>`_.
The Python classes below also come with methods for translating back and
forth between type instances and Python objects.


.. automodule:: gwmm.types

.. toctree::
   :maxdepth: 1
   :caption: TYPE SDKS

    AcceptedBid  <types/accepted-bid>
    AtnBid  <types/atn-bid>
    GNodeGt  <types/g-node-gt>
    HeartbeatA  <types/heartbeat-a>
    LatestPrice  <types/latest-price>
    MarketBook  <types/market-book>
    MarketMakerInfo  <types/market-maker-info>
    MarketPrice  <types/market-price>
    MarketSlot  <types/market-slot>
    MarketTypeGt  <types/market-type-gt>
    PriceQuantity  <types/price-quantity>
    PriceQuantityUnitless  <types/price-quantity-unitless>
    Ready  <types/ready>
    SimTimestep  <types/sim-timestep>
