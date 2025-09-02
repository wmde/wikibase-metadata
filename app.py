"""Main Application"""

from contextlib import asynccontextmanager
from typing import Optional
from fastapi import BackgroundTasks, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse, StreamingResponse
from strawberry.fastapi import GraphQLRouter

from export_csv import export_metric_csv
from model.strawberry import schema
from resolvers.authentication import authenticate_token
from schedule import scheduler


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


app.include_router(GraphQLRouter(schema=schema), prefix="/graphql")


@app.get("/csv/metrics", response_class=StreamingResponse)
async def metric_csv(
    background_tasks: BackgroundTasks, authorization: Optional[str] = None
) -> StreamingResponse:
    """Quantity CSV"""

    try:
        assert authorization is not None
    except AssertionError:
        return PlainTextResponse("Authorization Missing", 403)

    try:
        authenticate_token(authorization)
    except AssertionError:
        return PlainTextResponse("Authorization Failed", 403)

    return await export_metric_csv(background_tasks)
