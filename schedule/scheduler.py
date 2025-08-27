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
    update_out_of_date_external_identifier_observations,
    update_out_of_date_url_observations,
    update_out_of_date_recent_changes_observations,
    update_out_of_date_software_observations,
    update_out_of_date_stats_observations,
    update_out_of_date_user_observations,
    update_software_data,
    update_out_of_date_cloud_instances,
)
from resolvers.update import update_missing_script_paths, update_missing_sparql_urls


# Set up the scheduler
scheduler = AsyncIOScheduler()

# intervals
scheduler.add_job(update_software_data, IntervalTrigger(hours=2))

# crons
scheduler.add_job(
    update_out_of_date_cloud_instances,
    CronTrigger(day_of_week=6, hour=20),  # before data pulls
)
scheduler.add_job(
    update_missing_script_paths,
    CronTrigger(day_of_week=6, hour=22),  # before data pulls
)
scheduler.add_job(
    update_missing_sparql_urls,
    CronTrigger(day_of_week=6, hour=23),  # before data pulls
)
scheduler.add_job(
    update_out_of_date_connectivity_observations,
    CronTrigger(day_of_week=0, hour=0),
)
scheduler.add_job(
    update_out_of_date_log_first_observations,
    CronTrigger(day_of_week=0, hour=1, minute=0),
)
scheduler.add_job(
    update_out_of_date_log_last_observations,
    CronTrigger(day_of_week=0, hour=1, minute=40),
)
scheduler.add_job(
    update_out_of_date_recent_changes_observations,
    CronTrigger(day_of_week=0, hour=2, minute=20),
)
scheduler.add_job(
    update_out_of_date_property_observations,
    CronTrigger(day_of_week=0, hour=3),
)
scheduler.add_job(
    update_out_of_date_quantity_observations,
    CronTrigger(day_of_week=0, hour=4),
)
scheduler.add_job(
    update_out_of_date_external_identifier_observations,
    CronTrigger(day_of_week=0, hour=4, minute=20),
)
scheduler.add_job(
    update_out_of_date_url_observations,
    CronTrigger(day_of_week=0, hour=4, minute=40),
)
scheduler.add_job(
    update_out_of_date_software_observations,
    CronTrigger(day_of_week=0, hour=5),
)
scheduler.add_job(
    update_out_of_date_stats_observations,
    CronTrigger(day_of_week=0, hour=6),
)
scheduler.add_job(
    update_out_of_date_user_observations,
    CronTrigger(day_of_week=0, hour=7),
)
