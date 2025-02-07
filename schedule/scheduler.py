"""Scheduler"""

import asyncio
from datetime import datetime
import os
import time
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from config import jobs_db_connection_string

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


# Set up the scheduler
scheduler = AsyncIOScheduler(
    jobstores={"default": SQLAlchemyJobStore(url=jobs_db_connection_string)}
)

scheduler.add_job(
    update_out_of_date_connectivity_observations,
    id="update_out_of_date_connectivity_observations",
    trigger=CronTrigger(day_of_week=0, hour=0),
    replace_existing=True,
)
scheduler.add_job(
    update_out_of_date_log_first_observations,
    id="update_out_of_date_log_first_observations",
    trigger=CronTrigger(day_of_week=0, hour=1),
    replace_existing=True,
)
scheduler.add_job(
    update_out_of_date_log_last_observations,
    id="update_out_of_date_log_last_observations",
    trigger=CronTrigger(day_of_week=0, hour=2),
    replace_existing=True,
)
scheduler.add_job(
    update_out_of_date_property_observations,
    id="update_out_of_date_property_observations",
    trigger=CronTrigger(day_of_week=0, hour=3),
    replace_existing=True,
)
scheduler.add_job(
    update_out_of_date_quantity_observations,
    id="update_out_of_date_quantity_observations",
    trigger=CronTrigger(day_of_week=0, hour=4),
    replace_existing=True,
)
scheduler.add_job(
    update_out_of_date_software_observations,
    id="update_out_of_date_software_observations",
    trigger=CronTrigger(day_of_week=0, hour=5),
    replace_existing=True,
)
scheduler.add_job(
    update_out_of_date_stats_observations,
    id="update_out_of_date_stats_observations",
    trigger=CronTrigger(day_of_week=0, hour=6),
    replace_existing=True,
)
scheduler.add_job(
    update_out_of_date_user_observations,
    id="update_out_of_date_user_observations",
    trigger=CronTrigger(day_of_week=0, hour=7),
    replace_existing=True,
)
scheduler.add_job(
    update_software_data,
    id="update_software_data",
    trigger=IntervalTrigger(hours=2),
    replace_existing=True,
)


async def hello_world():
    """Test Function"""

    print(f"Hello World start - {os.getpid()} - {datetime.now()}")
    await asyncio.to_thread(time.sleep, 1)
    print(f"Hello World end - {os.getpid()} - {datetime.now()}")


scheduler.add_job(
    hello_world,
    id="hello_world",
    trigger=IntervalTrigger(seconds=5),
    replace_existing=True,
)
