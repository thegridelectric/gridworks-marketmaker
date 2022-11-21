# app_db.py
import dotenv
from fastapi import FastAPI
from fastapi import status
from tortoise import Model
from tortoise import fields
from tortoise.contrib.fastapi import register_tortoise

import gwmm.config as config


settings: config.Settings = config.Settings(_env_file=dotenv.find_dotenv())


class SimTimeModel(Model):
    value = fields.IntField(default=0)


app = FastAPI()

# increases the count variable in the sim_time object by 1
@app.post("/increment")
async def increment():
    sim_time, is_created = await SimTimeModel.get_or_create(id=1)
    sim_time.value += 1  # it's better do it in transaction
    await sim_time.save()
    return status.HTTP_200_OK


# returns a json containing the current count from the sim_time object
@app.get("/report")
async def report():
    sim_time, is_created = await SimTimeModel.get_or_create(id=1)
    return {"count": sim_time.value}


# resets the count in the sim_time object to 0
@app.post("/reset")
async def reset():
    sim_time, is_created = await SimTimeModel.get_or_create(id=1)
    sim_time.value = 0
    await sim_time.save()
    return status.HTTP_200_OK


register_tortoise(
    app,
    db_url=f"postgres://test_user:test_pass@{settings.public.mmdb_endpoint}:5432/test_db",  # Don't expose login/pass in src, use environment variables
    modules={"models": ["app_db"]},
    generate_schemas=True,
    add_exception_handlers=True,
)
