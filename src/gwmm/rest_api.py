from functools import lru_cache
from typing import Dict
from typing import List

from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.responses import FileResponse
from pydantic import ValidationError

import gwmm.config as config
from gwmm.market_maker import MarketMaker
from gwmm.schemata import AtnBid
from gwmm.schemata import MarketMakerInfo
from gwmm.utils import RestfulResponse


# Create FasatAPI instance
app = FastAPI()

mm = MarketMaker()


@lru_cache()
def get_settings():
    return mm.settings


@app.get("/", response_model=MarketMakerInfo)
async def main():
    return mm.info


@app.post("/bid/", response_model=RestfulResponse)
async def tavalidatorcert_algo_create_received(
    payload: AtnBid,
):
    r = mm.atn_bid(payload=payload)
    if r.HttpStatusCode > 200:
        raise HTTPException(
            status_code=r.HttpStatusCode, detail=f"[{r.HttpStatusCode}]: {r.Note}"
        )
    return r
