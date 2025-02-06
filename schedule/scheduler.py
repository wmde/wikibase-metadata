"""Scheduler"""

from datetime import datetime
import os
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger

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
scheduler = AsyncIOScheduler()

scheduler.add_job(
    update_out_of_date_connectivity_observations,
    CronTrigger(day_of_week=0, hour=0),
    max_instances=1,
)
scheduler.add_job(
    update_out_of_date_log_first_observations,
    CronTrigger(day_of_week=0, hour=1),
    max_instances=1,
)
scheduler.add_job(
    update_out_of_date_log_last_observations,
    CronTrigger(day_of_week=0, hour=2),
    max_instances=1,
)
scheduler.add_job(
    update_out_of_date_property_observations,
    CronTrigger(day_of_week=0, hour=3),
    max_instances=1,
)
scheduler.add_job(
    update_out_of_date_quantity_observations,
    CronTrigger(day_of_week=0, hour=4),
    max_instances=1,
)
scheduler.add_job(
    update_out_of_date_software_observations,
    CronTrigger(day_of_week=0, hour=5),
    max_instances=1,
)
scheduler.add_job(
    update_out_of_date_stats_observations,
    CronTrigger(day_of_week=0, hour=6),
    max_instances=1,
)
scheduler.add_job(
    update_out_of_date_user_observations,
    CronTrigger(day_of_week=0, hour=7),
    max_instances=1,
)
scheduler.add_job(update_software_data, IntervalTrigger(hours=2), max_instances=1)


def hello_world():
    """Test Function"""
    print(f"Hello World - {os.getpid()} - {datetime.now()}")


scheduler.add_job(hello_world, IntervalTrigger(seconds=5), max_instances=1)
