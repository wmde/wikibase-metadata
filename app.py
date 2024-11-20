"""Main Application"""

from contextlib import asynccontextmanager
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from strawberry.fastapi import GraphQLRouter

from fetch_data import (
    update_out_of_date_connectivity_observations,
    update_out_of_date_log_first_observations,
    update_out_of_date_log_last_observations,
    update_out_of_date_property_observations,
    update_out_of_date_quantity_observations,
    update_out_of_date_software_observations,
    update_out_of_date_stats_observations,
    update_out_of_date_user_observations,
    update_software_data,
)
from model.strawberry import schema


# Set up the scheduler
scheduler = AsyncIOScheduler()

scheduler.add_job(
    update_out_of_date_connectivity_observations, CronTrigger(day_of_week=0, hour=0)
)
scheduler.add_job(
    update_out_of_date_log_first_observations, CronTrigger(day_of_week=0, hour=1)
)
scheduler.add_job(
    update_out_of_date_log_last_observations, CronTrigger(day_of_week=0, hour=2)
)
scheduler.add_job(
    update_out_of_date_property_observations, CronTrigger(day_of_week=0, hour=3)
)
scheduler.add_job(
    update_out_of_date_quantity_observations, CronTrigger(day_of_week=0, hour=4)
)
scheduler.add_job(
    update_out_of_date_software_observations, CronTrigger(day_of_week=0, hour=5)
)
scheduler.add_job(
    update_out_of_date_stats_observations, CronTrigger(day_of_week=0, hour=6)
)
scheduler.add_job(
    update_out_of_date_user_observations, CronTrigger(day_of_week=0, hour=7)
)
scheduler.add_job(update_software_data, IntervalTrigger(hours=2))


# Ensure the scheduler shuts down properly on application exit.
@asynccontextmanager
async def lifespan(
    app: FastAPI,
):  # pylint: disable=redefined-outer-name,unused-argument
    """Triggers at startup, yields, resumes at shutdown"""

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
