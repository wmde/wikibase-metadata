"""Main Application"""

from typing import Optional
from fastapi import FastAPI
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
