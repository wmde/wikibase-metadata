"""Main Application"""

from contextlib import asynccontextmanager
from typing import Optional
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse, PlainTextResponse
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


# Serve the built frontend from the Vite `dist` directory.
DIST_DIR = (Path(__file__).resolve().parent / "dist").resolve()

# Mount assets (e.g., /assets/*) referenced by the built app
assets_dir = DIST_DIR / "assets"
if assets_dir.exists():
    app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")


@app.get("/{filename}.svg", include_in_schema=False)
async def serve_top_level_svg(filename: str):
    """Serve any top-level SVG from the built dist (e.g., /github.svg, /wmde.svg)"""
    svg_file = DIST_DIR / f"{filename}.svg"
    if svg_file.exists():
        return FileResponse(svg_file)
    return PlainTextResponse("Not found", status_code=404)


@app.get("/{full_path:path}", include_in_schema=False)
async def spa_handler(full_path: str):
    """SPA handler: serve index.html for root and any unmatched, non-API GET path"""
    # Let API and docs paths 404 naturally; otherwise serve the SPA
    if full_path.startswith(("graphql", "docs", "redoc", "openapi.json")):
        return PlainTextResponse("Not found", status_code=404)
    index_file = DIST_DIR / "index.html"
    if index_file.exists():
        return FileResponse(index_file)
    return PlainTextResponse("Frontend build not found", status_code=404)
