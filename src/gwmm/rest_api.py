from functools import lru_cache
from typing import Dict
from typing import List


from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.responses import FileResponse
from pydantic import ValidationError

import gwmm.config as config
from gwmm.utils import RestfulResponse
from gwmm.market_maker import MarketMaker

# Create FasatAPI instance
app = FastAPI()

mm = MarketMaker()


@lru_cache()
def get_settings():
    return mm.settings


@app.get("/")
async def main():
    return {"Hi": "There"}


# @app.get("/base-g-nodes/by-id/{g_node_id}", response_model=BasegnodeGt)
# async def get_base_g_node(g_node_id: str):
#     gn = await gnf.g_node_from_id(g_node_id)
#     return gn


# @app.post("/tavalidatorcert-algo-create/", response_model=RestfulResponse)
# async def tavalidatorcert_algo_create_received(
#     payload: TavalidatorcertAlgoCreate,
# ):
#     r = gnf.tavalidatorcert_algo_create_received(payload=payload)
#     if r.HttpStatusCode > 200:
#         raise HTTPException(
#             status_code=r.HttpStatusCode, detail=f"[{r.HttpStatusCode}]: {r.Note}"
#         )
#     return r
