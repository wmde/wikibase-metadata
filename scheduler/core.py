"""Dedicated APScheduler process with health endpoint"""

import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger

from config import enable_scheduler
from logger import logger

from fetch_data import (
    update_out_of_date_connectivity_observations,
    update_out_of_date_external_identifier_observations,
    update_out_of_date_log_first_observations,
    update_out_of_date_log_last_observations,
    update_out_of_date_property_observations,
    update_out_of_date_quantity_observations,
    update_out_of_date_recent_changes_observations,
    update_out_of_date_software_observations,
    update_out_of_date_stats_observations,
    update_out_of_date_time_to_first_value_observations,
    update_out_of_date_user_observations,
    update_software_data,
    update_out_of_date_cloud_instances,
)

from resolvers.update import (
    update_missing_script_paths,
    update_missing_sparql_urls,
)

def create_scheduler() -> AsyncIOScheduler:
    """Create a scheduler"""

    scheduler = AsyncIOScheduler(timezone="UTC")

    job_defaults = {
        "max_instances": 1,
        "coalesce": True,
        "misfire_grace_time": 3600,
    }

    scheduler.add_job(
        update_software_data,
        IntervalTrigger(hours=2),
        **job_defaults
    )

    scheduler.add_job(
        update_out_of_date_cloud_instances,
        CronTrigger(
            day_of_week=6,
            hour=20,
        ),
        **job_defaults,
    )

    scheduler.add_job(
        update_missing_script_paths,
        CronTrigger(
            day_of_week=6,
            hour=22,
        ),
        **job_defaults,
    )

    scheduler.add_job(
        update_missing_sparql_urls,
        CronTrigger(
            day_of_week=6,
            hour=23,
        ),
        **job_defaults,
    )

    scheduler.add_job(
        update_out_of_date_connectivity_observations,
        CronTrigger(
            day_of_week=0,
            hour=0,
        ),
        **job_defaults,
)

    scheduler.add_job(
        update_out_of_date_log_first_observations,
        CronTrigger(
            day_of_week=0,
            hour=1,
        ),
        **job_defaults,
    )

    scheduler.add_job(
        update_out_of_date_log_last_observations,
        CronTrigger(
            day_of_week=0,
            hour=2,
        ),
        **job_defaults,
)

    scheduler.add_job(
        update_out_of_date_recent_changes_observations,
        CronTrigger(
            day_of_week=0,
            hour=3,
        ),
        **job_defaults,
)

    scheduler.add_job(
        update_out_of_date_property_observations,
        CronTrigger(
            day_of_week=0,
            hour=4,
        ),
        **job_defaults,
    )

    scheduler.add_job(
        update_out_of_date_quantity_observations,
        CronTrigger(
            day_of_week=0,
            hour=5,
        ),
        **job_defaults,
    )

    scheduler.add_job(
        update_out_of_date_software_observations,
        CronTrigger(
            day_of_week=0,
            hour=6,
        ),
        **job_defaults,
    )

    scheduler.add_job(
        update_out_of_date_stats_observations,
        CronTrigger(
            day_of_week=0,
            hour=7,
        ),
        **job_defaults,
    )

    scheduler.add_job(
        update_out_of_date_time_to_first_value_observations,
        CronTrigger(
            day_of_week=0,
            hour=8,
        ),
        **job_defaults,
    )

    scheduler.add_job(
        update_out_of_date_user_observations,
        CronTrigger(
            day_of_week=0,
            hour=9,
        ),
        **job_defaults,
    )

    scheduler.add_job(
        update_out_of_date_external_identifier_observations,
        CronTrigger(
            day_of_week=0,
            hour=10,
        ),
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
            "Content-Length: 7\r\n"
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

    if not enable_scheduler:
        logger.info("Scheduler disabled via config")
        return

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
