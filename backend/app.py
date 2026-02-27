"""Main Application"""

from contextlib import asynccontextmanager
from typing import Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from strawberry.fastapi import GraphQLRouter

from export_csv import export_metric_csv
from model.strawberry import schema
from resolvers.authentication import authenticate_token
from schedule import scheduler
from data.database_connection import get_async_session


# Ensure the scheduler shuts down properly on application exit.
@asynccontextmanager
# pylint: disable-next=redefined-outer-name,unused-argument
async def lifespan(app: FastAPI):
    """Triggers at startup, yields, resumes at shutdown"""

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


async def get_context():
    """Get database session context"""
    async with get_async_session() as session:
        yield {"db": session}


app.include_router(
    GraphQLRouter(schema=schema, context_getter=get_context), prefix="/graphql"
)


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
