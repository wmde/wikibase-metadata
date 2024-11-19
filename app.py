"""Main Application"""

from contextlib import asynccontextmanager
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from strawberry.fastapi import GraphQLRouter

from fetch_data.out_of_date.update_out_of_date import (
    update_out_of_date_stats_observations,
)
from model.strawberry import schema


# Set up the scheduler
scheduler = AsyncIOScheduler()
# four_minute_trigger = IntervalTrigger(minutes=4)
hourly_trigger = CronTrigger(minute=6)  # every hour
scheduler.add_job(update_out_of_date_stats_observations, hourly_trigger)


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
