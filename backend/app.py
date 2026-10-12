"""Main Application"""

# pylint: disable=import-outside-toplevel
import os
from typing import Optional
from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from strawberry.fastapi import GraphQLRouter

from export_csv import export_metric_csv
from model.strawberry import schema
from resolvers.authentication import authenticate_token

app = FastAPI()


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


@app.get("/csv/metrics")
async def metric_csv(authorization: Optional[str] = None):
    """Quantity CSV"""

    if authorization is None:
        return PlainTextResponse("Authorization Missing", 403)

    try:
        authenticate_token(authorization)
    except AssertionError:
        return PlainTextResponse("Authorization Failed", 403)

    return await export_metric_csv()


@app.post("/internal/update-missing-script-paths")
async def update_missing_script_paths_endpoint(
    x_scheduler_token: str = Header(),
):
    """Scheduler - Update Missing Script Paths"""
    if x_scheduler_token != os.environ["SCHEDULER_TOKEN"]:
        raise HTTPException(status_code=403, detail="Forbidden")

    # These have to imported here to avoid circular imports error on app startup
    from resolvers.update import update_missing_script_paths

    result = await update_missing_script_paths()

    return {
        "success": result.success,
        "failure": result.failure,
        "total": result.total,
    }


@app.post("/internal/update_software_data")
async def update_software_data_endpoint(
    x_scheduler_token: str = Header(),
):
    """Scheduler - Update Software Data"""
    if x_scheduler_token != os.environ["SCHEDULER_TOKEN"]:
        raise HTTPException(status_code=403, detail="Forbidden")

    from resolvers.update import update_software_data

    result = await update_software_data()

    return {
        "success": result.success,
        "failure": result.failure,
        "total": result.total,
    }


@app.post("/internal/update_out_of_date_cloud_instances")
async def update_out_of_date_cloud_instances_endpoint(
    x_scheduler_token: str = Header(),
):
    """Scheduler - Update Out of Date Cloud Instances"""

    if x_scheduler_token != os.environ["SCHEDULER_TOKEN"]:
        raise HTTPException(status_code=403, detail="Forbidden")

    from resolvers.update import update_out_of_date_cloud_instances

    result = await update_out_of_date_cloud_instances()

    return {
        "success": result.success,
        "failure": result.failure,
        "total": result.total,
    }


@app.post("/internal/update_missing_sparql_urls")
async def update_missing_sparql_urls_endpoint(
    x_scheduler_token: str = Header(),
):
    """Scheduler - Update Missing SparQL URLs"""

    if x_scheduler_token != os.environ["SCHEDULER_TOKEN"]:
        raise HTTPException(status_code=403, detail="Forbidden")

    from resolvers.update import update_missing_sparql_urls

    result = await update_missing_sparql_urls()

    return {
        "success": result.success,
        "failure": result.failure,
        "total": result.total,
    }


@app.post("/internal/update_out_of_date_connectivity_observations")
async def update_out_of_date_connectivity_observations_endpoint(
    x_scheduler_token: str = Header(),
):
    """Scheduler - Update Out of Date Connectivity Observations"""

    if x_scheduler_token != os.environ["SCHEDULER_TOKEN"]:
        raise HTTPException(status_code=403, detail="Forbidden")

    from fetch_data import update_out_of_date_connectivity_observations

    result = await update_out_of_date_connectivity_observations()

    return {
        "success": result.success,
        "failure": result.failure,
        "total": result.total,
    }


@app.post("/internal/update_out_of_date_log_first_observations")
async def update_out_of_date_log_first_observations_endpoint(
    x_scheduler_token: str = Header(),
):
    """Scheduler - Update Out of Date Log First Observations"""

    if x_scheduler_token != os.environ["SCHEDULER_TOKEN"]:
        raise HTTPException(status_code=403, detail="Forbidden")

    from fetch_data import update_out_of_date_log_first_observations

    result = await update_out_of_date_log_first_observations()

    return {
        "success": result.success,
        "failure": result.failure,
        "total": result.total,
    }


@app.post("/internal/update_out_of_date_log_last_observations")
async def update_out_of_date_log_last_observations_endpoint(
    x_scheduler_token: str = Header(),
):
    """Scheduler - Update Out of Date Log Last Observations"""

    if x_scheduler_token != os.environ["SCHEDULER_TOKEN"]:
        raise HTTPException(status_code=403, detail="Forbidden")

    from fetch_data import update_out_of_date_log_last_observations

    result = await update_out_of_date_log_last_observations()

    return {
        "success": result.success,
        "failure": result.failure,
        "total": result.total,
    }


@app.post("/internal/update_out_of_date_recent_changes_observations")
async def update_out_of_date_recent_changes_observations_endpoint(
    x_scheduler_token: str = Header(),
):
    """Scheduler - Update Out of Date Recent Changes Observations"""

    if x_scheduler_token != os.environ["SCHEDULER_TOKEN"]:
        raise HTTPException(status_code=403, detail="Forbidden")

    from fetch_data import update_out_of_date_recent_changes_observations

    result = await update_out_of_date_recent_changes_observations()

    return {
        "success": result.success,
        "failure": result.failure,
        "total": result.total,
    }


@app.post("/internal/update_out_of_date_property_observations")
async def update_out_of_date_property_observations_endpoint(
    x_scheduler_token: str = Header(),
):
    """Scheduler - Update Out of Date Property Observations"""

    if x_scheduler_token != os.environ["SCHEDULER_TOKEN"]:
        raise HTTPException(status_code=403, detail="Forbidden")

    from fetch_data import update_out_of_date_property_observations

    result = await update_out_of_date_property_observations()

    return {
        "success": result.success,
        "failure": result.failure,
        "total": result.total,
    }


@app.post("/internal/update_out_of_date_quantity_observations")
async def update_out_of_date_quantity_observations_endpoint(
    x_scheduler_token: str = Header(),
):
    """Scheduler - Update Out of Date Quantity Observations"""

    if x_scheduler_token != os.environ["SCHEDULER_TOKEN"]:
        raise HTTPException(status_code=403, detail="Forbidden")

    from fetch_data import update_out_of_date_quantity_observations

    result = await update_out_of_date_quantity_observations()

    return {
        "success": result.success,
        "failure": result.failure,
        "total": result.total,
    }


@app.post("/internal/update_out_of_date_software_observations")
async def update_out_of_date_software_observations_endpoint(
    x_scheduler_token: str = Header(),
):
    """Scheduler - Update Out of Date Software Observations"""

    if x_scheduler_token != os.environ["SCHEDULER_TOKEN"]:
        raise HTTPException(status_code=403, detail="Forbidden")

    from fetch_data import update_out_of_date_software_observations

    result = await update_out_of_date_software_observations()

    return {
        "success": result.success,
        "failure": result.failure,
        "total": result.total,
    }


@app.post("/internal/update_out_of_date_stats_observations")
async def update_out_of_date_stats_observations_endpoint(
    x_scheduler_token: str = Header(),
):
    """Scheduler - Update Out of Date Stats Observations"""

    if x_scheduler_token != os.environ["SCHEDULER_TOKEN"]:
        raise HTTPException(status_code=403, detail="Forbidden")

    from fetch_data import update_out_of_date_stats_observations

    result = await update_out_of_date_stats_observations()

    return {
        "success": result.success,
        "failure": result.failure,
        "total": result.total,
    }


@app.post("/internal/update_out_of_date_time_to_first_value_observations")
async def update_out_of_date_time_to_first_value_observations_endpoint(
    x_scheduler_token: str = Header(),
):
    """Scheduler - Update Out of Date Time to First Value Observations"""

    if x_scheduler_token != os.environ["SCHEDULER_TOKEN"]:
        raise HTTPException(status_code=403, detail="Forbidden")

    from fetch_data import update_out_of_date_time_to_first_value_observations

    result = await update_out_of_date_time_to_first_value_observations()

    return {
        "success": result.success,
        "failure": result.failure,
        "total": result.total,
    }


@app.post("/internal/update_out_of_date_user_observations")
async def update_out_of_date_user_observations_endpoint(
    x_scheduler_token: str = Header(),
):
    """Scheduler - Update Out of Date User Observations"""

    if x_scheduler_token != os.environ["SCHEDULER_TOKEN"]:
        raise HTTPException(status_code=403, detail="Forbidden")

    from fetch_data import update_out_of_date_user_observations

    result = await update_out_of_date_user_observations()

    return {
        "success": result.success,
        "failure": result.failure,
        "total": result.total,
    }


@app.post("/internal/update_out_of_date_external_identifier_observations")
async def update_out_of_date_external_identifier_observations_endpoint(
    x_scheduler_token: str = Header(),
):
    """Scheduler - Update Out of Date External Identifier Observations"""

    if x_scheduler_token != os.environ["SCHEDULER_TOKEN"]:
        raise HTTPException(status_code=403, detail="Forbidden")

    from fetch_data import update_out_of_date_external_identifier_observations

    result = await update_out_of_date_external_identifier_observations()

    return {
        "success": result.success,
        "failure": result.failure,
        "total": result.total,
    }
