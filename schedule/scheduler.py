"""Scheduler"""

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
    update_out_of_date_cloud_instances,
)


# Set up the scheduler
scheduler = AsyncIOScheduler()

scheduler.add_job(
    update_out_of_date_connectivity_observations, IntervalTrigger(minutes=5)
)
scheduler.add_job(
    update_out_of_date_log_first_observations, IntervalTrigger(minutes=5)
)
scheduler.add_job(
    update_out_of_date_log_last_observations, IntervalTrigger(minutes=5)
)
scheduler.add_job(
    update_out_of_date_property_observations, IntervalTrigger(minutes=5)
)
scheduler.add_job(
    update_out_of_date_quantity_observations, IntervalTrigger(minutes=5)
)
scheduler.add_job(
    update_out_of_date_software_observations, IntervalTrigger(minutes=5)
)
scheduler.add_job(
    update_out_of_date_stats_observations, IntervalTrigger(minutes=5)
)
scheduler.add_job(update_out_of_date_user_observations, IntervalTrigger(minutes=5))
scheduler.add_job(update_software_data, IntervalTrigger(hours=2))

scheduler.add_job(
    update_out_of_date_cloud_instances,
    CronTrigger(day_of_week=6, hour=20),  # before data pulls
)
