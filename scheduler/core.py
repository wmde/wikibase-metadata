"""Dedicated APScheduler process with health endpoint"""

import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger

from .jobs import (
    run_update_software_data,
    run_update_out_of_date_cloud_instances,
    run_update_missing_script_paths,
    run_update_missing_sparql_urls,
    run_update_out_of_date_connectivity_observations,
    run_update_out_of_date_log_first_observations,
    run_update_out_of_date_log_last_observations,
    run_update_out_of_date_recent_changes_observations,
    run_update_out_of_date_property_observations,
    run_update_out_of_date_quantity_observations,
    run_update_out_of_date_software_observations,
    run_update_out_of_date_stats_observations,
    run_update_out_of_date_time_to_first_value_observations,
    run_update_out_of_date_user_observations,
    run_update_out_of_date_external_identifier_observations
)
from logger import logger

def create_scheduler() -> AsyncIOScheduler:
    """Create a scheduler"""

    scheduler = AsyncIOScheduler(timezone="UTC")

    job_defaults = {
        "max_instances": 1,
        "coalesce": True,
        "misfire_grace_time": 3600,
    }

    scheduler.add_job(
        run_update_software_data,
        IntervalTrigger(hours=2),
        id="update_software_data",
        **job_defaults,
    )

    scheduler.add_job(
        run_update_out_of_date_cloud_instances,
        CronTrigger(
            day_of_week=6,
            hour=20,
        ),
        id="update_out_of_date_cloud_instances",
        **job_defaults,
    )

    scheduler.add_job(
        run_update_missing_script_paths,
        CronTrigger(
            day_of_week=6, 
            hour=22
        ),
        id="update_missing_script_paths",
        **job_defaults,
    )

    scheduler.add_job(
        run_update_missing_sparql_urls,
        CronTrigger(
            day_of_week=6,
            hour=23,
        ),
        id="update_missing_sparql_urls",
        **job_defaults,
    )

    scheduler.add_job(
        run_update_out_of_date_connectivity_observations,
        CronTrigger(
            day_of_week=0,
            hour=0,
        ),
        id="update_out_of_date_connectivity_observations",
        **job_defaults,
)

    scheduler.add_job(
        run_update_out_of_date_log_first_observations,
        CronTrigger(
            day_of_week=0,
            hour=1,
        ),
        id="update_out_of_date_log_first_observations",
        **job_defaults,
    )

    scheduler.add_job(
        run_update_out_of_date_log_last_observations,
        CronTrigger(
            day_of_week=0,
            hour=2,
        ),
        id="update_out_of_date_log_last_observations",
        **job_defaults,
)

    scheduler.add_job(
        run_update_out_of_date_recent_changes_observations,
        CronTrigger(
            day_of_week=0,
            hour=3,
        ),
        id="update_out_of_date_recent_changes_observations",
        **job_defaults,
)

    scheduler.add_job(
        run_update_out_of_date_property_observations,
        CronTrigger(
            day_of_week=0,
            hour=4,
        ),
        id="update_out_of_date_property_observations",
        **job_defaults,
    )

    scheduler.add_job(
        run_update_out_of_date_quantity_observations,
        CronTrigger(
            day_of_week=0,
            hour=5,
        ),
        id="update_out_of_date_quantity_observations",
        **job_defaults,
    )

    scheduler.add_job(
        run_update_out_of_date_software_observations,
        CronTrigger(
            day_of_week=0,
            hour=6,
        ),
        id="update_out_of_date_software_observations",
        **job_defaults,
    )

    scheduler.add_job(
        run_update_out_of_date_stats_observations,
        CronTrigger(
            day_of_week=0,
            hour=7,
        ),
        id="update_out_of_date_stats_observations",
        **job_defaults,
    )

    scheduler.add_job(
        run_update_out_of_date_time_to_first_value_observations,
        CronTrigger(
            day_of_week=0,
            hour=8,
        ),
        id="update_out_of_date_time_to_first_value_observations",
        **job_defaults,
    )

    scheduler.add_job(
        run_update_out_of_date_user_observations,
        CronTrigger(
            day_of_week=0,
            hour=9,
        ),
        id="update_out_of_date_user_observations",
        **job_defaults,
    )

    scheduler.add_job(
        run_update_out_of_date_external_identifier_observations,
        CronTrigger(
            day_of_week=0,
            hour=10,
        ),
        id="update_out_of_date_external_identifier_observations",
        **job_defaults,
    )

    return scheduler

async def health_handler(_reader, writer, scheduler: AsyncIOScheduler):
    """Check the health of the scheduler"""

    if scheduler and scheduler.running:
        response = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: text/plain\r\n"
            "Content-Length: 2\r\n"
            "\r\n"
            "OK"
        )
    else:
        response = (
            "HTTP/1.1 503 Service Unavailable\r\n"
            "Content-Type: text/plain\r\n"
            "Content-Length: 9\r\n"
            "\r\n"
            "UNHEALTHY"
        )

    writer.write(response.encode())
    await writer.drain()
    writer.close()

async def start_health_server(scheduler: AsyncIOScheduler):
    """Starts an HTTP server to check health of scheduler"""

    async def handler(reader, writer):
        await health_handler(reader, writer, scheduler)

    server = await asyncio.start_server(handler, "0.0.0.0", 8081)
    logger.info("Health endpoint listening on :8081")
    return server

async def run_scheduler():
    """Run the scheduler and health server"""

    scheduler = create_scheduler()
    scheduler.start()

    logger.info("Scheduler started successfully")

    server = await start_health_server(scheduler)

    async with server:
        try:
            await server.serve_forever()
        except (KeyboardInterrupt, SystemExit):
            logger.info("Shutting down scheduler...")
            scheduler.shutdown()