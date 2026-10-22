# gridworks-marketmaker

The MarketMaker runs a market at one node of the grid and states its
prices. The one deployed today is a stopgap for the Keene constraint
market in ISO New England: at the top of every hour it publishes the
cleared price for the hour's `rt60gate5` slot (real-time energy, 60-minute
slots, gate closing 5 minutes before the slot), as the registered GNode
`hw1.isone.me.versant.keene`. LeafTransactiveNodes clear their dispatch
contracts against that price, and the journal keeps it as the settled
price series.

The price is ISO-NE's current 5-minute real-time locational marginal
price at Keene Rd (location 43790), fetched a few seconds before the
hour, plus the Versant Rate A-1 total-delivery price for the hour
(`src/gwmm/tariff.py`). If ISO-NE does not answer in time the maker
publishes the last price it published and raises a `Critical` glitch.

The maker receives bids and drops them. The ack that makes a bid a
contract, the market book and the clearing are the full maker's job.

## What it speaks

Two Sema words, from the versioned vocabulary of JSON-Schema contracts
for GridWorks boundaries, canonical at
[`thegridelectric/sema`](https://github.com/thegridelectric/sema):
`latest.price` and `glitch`, listed in `src/gwmm/sema_seed_request.yaml`.
Both go out as broadcasts on the maker's publish exchange:

```
rjb.<maker-alias-lrh>.mm.latest-price
rjb.<maker-alias-lrh>.mm.glitch
```

An MQTT-native subscriber hears the price as
`rjb/<maker-alias-lrh>/mm/latest-price`.

## Running

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
sibling `../sema` checkout; never edit the snapshot by hand. `service/`
has the systemd unit and the shell aliases a box login uses.
