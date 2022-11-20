from functools import lru_cache
from typing import Dict
from typing import List

import pendulum

# app_cache.py
from aiocache import Cache
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import status
from fastapi.responses import FileResponse
from pydantic import BaseModel
from pydantic import ValidationError

import gwmm.config as config
from gwmm.api_utils import MarketMakerApi
from gwmm.market_maker import MarketMaker
from gwmm.schemata import AtnBid
from gwmm.schemata import MarketMakerInfo
from gwmm.schemata import SimTimestep
from gwmm.utils import RestfulResponse


app = FastAPI()
cache = Cache(Cache.REDIS, endpoint="localhost", port=6379, namespace="main")


class SimTime:
    def __init__(self):
        pass

    async def get_time(self) -> int:
        return await cache.get("time", default=0)

    async def set_time(self, value: int) -> None:
        await cache.set("time", value)


sim_time = SimTime()


mm = MarketMakerApi()


@lru_cache()
def get_settings():
    return mm.settings


@app.get("/", response_model=MarketMakerInfo)
async def main():
    return mm.info


@app.get("/time/")
async def time():
    time = await sim_time.get_time()
    return {"TimeUnixS": time, "UTC": pendulum.from_timestamp(time).to_iso8601_string()}


@app.post(f"/sim-timestep/")
async def set_time(timestep: SimTimestep):
    await sim_time.set_time(timestep.TimeUnixS)
    return status.HTTP_200_OK


@app.post("/atn-bid/", response_model=RestfulResponse)
async def atn_bid_received(
    payload: AtnBid,
):
    r = mm.atn_bid(payload=payload)
    if r.HttpStatusCode > 200:
        raise HTTPException(
            status_code=r.HttpStatusCode, detail=f"[{r.HttpStatusCode}]: {r.Note}"
        )
    return r
