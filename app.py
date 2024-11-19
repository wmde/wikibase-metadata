"""Main Application"""

from contextlib import asynccontextmanager
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from strawberry.fastapi import GraphQLRouter

from fetch_data.out_of_date.update_out_of_date import (
    update_out_of_date_connectivity_observations,
    update_out_of_date_log_first_observations,
    update_out_of_date_log_last_observations,
    update_out_of_date_property_observations,
    update_out_of_date_quantity_observations,
    update_out_of_date_software_observations,
    update_out_of_date_stats_observations,
    update_out_of_date_user_observations,
)
from model.strawberry import schema


# Set up the scheduler
scheduler = AsyncIOScheduler()

start_min = 14

scheduler.add_job(
    update_out_of_date_connectivity_observations, CronTrigger(minute=0 + start_min)
)
scheduler.add_job(
    update_out_of_date_log_first_observations, CronTrigger(minute=5 + start_min)
)
scheduler.add_job(
    update_out_of_date_log_last_observations, CronTrigger(minute=10 + start_min)
)
scheduler.add_job(
    update_out_of_date_property_observations, CronTrigger(minute=15 + start_min)
)
scheduler.add_job(
    update_out_of_date_quantity_observations, CronTrigger(minute=20 + start_min)
)
scheduler.add_job(
    update_out_of_date_software_observations, CronTrigger(minute=25 + start_min)
)
scheduler.add_job(
    update_out_of_date_stats_observations, CronTrigger(minute=30 + start_min)
)
scheduler.add_job(
    update_out_of_date_user_observations, CronTrigger(minute=35 + start_min)
)


# Ensure the scheduler shuts down properly on application exit.
@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler.start()
    yield
    scheduler.shutdown()


app = FastAPI(lifespan=lifespan)


origins = ["http://localhost", "http://0.0.0.0", "http://127.0.0.1"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    """Root"""
    return {"Hello": "World"}


app.include_router(GraphQLRouter(schema=schema), prefix="/graphql")
