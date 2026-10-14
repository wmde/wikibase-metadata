"""Scheduled jobs that trigger backend endpoints."""

import os
import httpx

BACKEND_URL = "http://backend:8000"


async def _run_backend_job(endpoint: str) -> None:
    """Call an internal backend endpoint."""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{BACKEND_URL}/internal/{endpoint}",
            headers={
                "X-Scheduler-Token": os.environ["SCHEDULER_TOKEN"],
            },
        )
        response.raise_for_status()


async def run_update_missing_script_paths() -> None:
    """Run Update Missing Script Paths"""
    await _run_backend_job("update-missing-script-paths")


async def run_update_software_data() -> None:
    """Run Update Software Data"""
    await _run_backend_job("update-software-data")


async def run_update_out_of_date_cloud_instances() -> None:
    """Run Update Out Of Date Cloud Instances"""
    await _run_backend_job("update-out-of-date-cloud-instances")


async def run_update_missing_sparql_urls() -> None:
    """Run Update Missing SPARQL URLs"""
    await _run_backend_job("update-missing-sparql-urls")


async def run_update_out_of_date_connectivity_observations() -> None:
    """Run Update Out Of Date Connectivity Observations"""
    await _run_backend_job("update-out-of-date-connectivity-observations")


async def run_update_out_of_date_log_first_observations() -> None:
    """Run Update Out Of Date Log First Observations"""
    await _run_backend_job("update-out-of-date-log-first-observations")


async def run_update_out_of_date_log_last_observations() -> None:
    """Run Update Out Of Date Log Last Observations"""
    await _run_backend_job("update-out-of-date-log-last-observations")


async def run_update_out_of_date_recent_changes_observations() -> None:
    """Run Update Out Of Date Recent Changes Observations"""
    await _run_backend_job("update-out-of-date-recent-changes-observations")


async def run_update_out_of_date_property_observations() -> None:
    """Run Update Out Of Date Property Observations"""
    await _run_backend_job("update-out-of-date-property-observations")


async def run_update_out_of_date_quantity_observations() -> None:
    """Run Update Out Of Date Quantity Observations"""
    await _run_backend_job("update-out-of-date-quantity-observations")


async def run_update_out_of_date_software_observations() -> None:
    """Run Update Out Of Date Software Observations"""
    await _run_backend_job("update-out-of-date-software-observations")


async def run_update_out_of_date_stats_observations() -> None:
    """Run Update Out Of Date Stats Observations"""
    await _run_backend_job("update-out-of-date-stats-observations")


async def run_update_out_of_date_time_to_first_value_observations() -> None:
    """Run Update Out Of Date Time To First Value Observations"""
    await _run_backend_job("update-out-of-date-time-to-first-value-observations")


async def run_update_out_of_date_user_observations() -> None:
    """Run Update Out Of Date User Observations"""
    await _run_backend_job("update-out-of-date-user-observations")


async def run_update_out_of_date_external_identifier_observations() -> None:
    """Run Update Out Of Date External Identifier Observations"""
    await _run_backend_job("update-out-of-date-external-identifier-observations")
