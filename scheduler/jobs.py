import httpx
import os

async def run_update_missing_script_paths():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://backend:8000/internal/update-missing-script-paths",
            headers={
                "X-Scheduler-Token": os.environ["SCHEDULER_TOKEN"],
            },
        )

        print(response.status_code)
        print(response.text)

        response.raise_for_status()

# update_out_of_date_cloud_instances