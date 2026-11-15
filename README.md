# gridworks-marketmaker

The MarketMaker runs one market at one node of the grid and states its price. The market it runs today is the Keene constraint market in ISO New England, where the houses of the fleet buy their heat's electricity hour by hour. At the top of every hour it publishes the cleared price for the hour that just opened: the wholesale price at the market's pricing node in its energy, congestion and loss parts, plus the delivery price the houses' tariff charges for that hour, with the tariff named. The houses' transactive nodes clear their dispatch contracts against that price, and the journal keeps the series as the settled price of the market.

When the wholesale price cannot be fetched in time, the maker still publishes the hour, at the last wholesale price it published with the hour's own delivery price, and raises a critical fault so a person is paged. A maker that starts partway through an hour publishes nothing for that hour, because a house clears against a price only at the top of the hour, when its bid is in.

Bids addressed to the maker are received and dropped. The acknowledgement that makes a bid a contract, the market book and the clearing belong to the full maker, which extends this one.

## What it speaks

Two Sema words, from the versioned vocabulary of JSON-Schema contracts
for GridWorks boundaries, canonical at
[`thegridelectric/sema`](https://github.com/thegridelectric/sema), and
listed in the seed `src/gwmm/sema_seed_request.yaml`:

- `latest.price`: the cleared price of one slot, named by the market's
  product, the maker's alias and the slot's start, in its parts under
  the named tariff.
- `glitch`: how the maker reports a fault, such as a slot published at
  a stale wholesale price.

Both go out as broadcasts on the maker's own exchange; an MQTT-native
subscriber hears the price as `rjb/<maker-alias-lrh>/mm/latest-price`.

## Where the price comes from

The wholesale part is ISO New England's five-minute real-time
locational marginal price at the market's pricing node for the hour's
first interval, fetched over ISO-NE's web services once ISO-NE posts
it, about 25 s into the hour. The delivery part is the fleet's
time-of-use tariff, Versant Rate A-1 "Home Eco Rate with Bonus Meter"
(page 6.1.1, Seventeenth Revision, in the [BHD consolidated tariff
effective 2026-10-26](https://www.versantpower.com/docs/default-source/business-rates-bhd/10-26-26-update/versantpower-bhd-tariffs-2026-10-26.pdf?sfvrsn=41600df1_1)),
a hand-kept copy in `src/gwmm/tariff.py` until a tariff word states it. The price-forecast service prices delivery from the
same table, so a forecast and the published price agree on it.

## Running

One process, the maker, run as a systemd unit on its own box with the
identity of the registered GNode it is. `service/` has the unit and the
shell aliases a box login uses. The maker keeps no state: a restart
begins cold.

```
cp template.env .env     # fill in the broker and the ISO-NE account
uv sync --all-groups
uv run gwmm show         # the price the maker would publish for the open slot
uv run gwmm rabbit       # run the maker
./ci.sh                  # what CI runs: lint, types, tests
```

The broker test needs `GWMM_TEST_RABBIT_URL` (the dev broker's `d1__1`
vhost) and self-skips without it. `scripts/regen_sema_snapshot.sh`
regenerates the vendored Sema snapshot under `src/gwmm/sema` from a
sibling `../sema` checkout; never edit the snapshot by hand.
