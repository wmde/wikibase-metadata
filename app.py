"""Main Application"""

from contextlib import asynccontextmanager
from fastapi import BackgroundTasks, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from starlette.requests import Request
from strawberry.fastapi import GraphQLRouter

from export_csv import export_quantity_csv
from model.strawberry import schema
from resolvers.authentication import authenticate_request
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

CHUNK_SIZE = 1024 * 1024


@app.get("/csv/quantity", response_class=StreamingResponse)
async def quantity_csv(request: Request, background_tasks: BackgroundTasks):
    """Quantity CSV"""

    # authenticate_request(request)

    return await export_quantity_csv(background_tasks)
