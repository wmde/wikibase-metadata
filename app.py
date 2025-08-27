"""Main Application"""

from contextlib import asynccontextmanager
import os
import uuid
from fastapi import BackgroundTasks, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import pandas
from strawberry.fastapi import GraphQLRouter

from model.strawberry import schema
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


@app.get("/csv/quantity")
def quantity_csv(background_tasks: BackgroundTasks):
    """Quantity CSV"""

    df = pandas.DataFrame([{"row": i, "v": "test"} for i in range(2000000)])
    filename = f"{uuid.uuid4()}.csv"
    df.to_csv(filename)
    del df

    def iterfile():
        with open(filename, "rb") as f:
            while chunk := f.read(CHUNK_SIZE):
                yield chunk

    background_tasks.add_task(os.remove, filename)

    headers = {"Content-Disposition": 'attachment; filename="quantity_data.csv"'}
    return StreamingResponse(iterfile(), headers=headers, media_type="text/csv")
    # return FileResponse(filename, filename='quantity_data.csv', media_type='text/csv')
