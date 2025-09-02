"""Main Application"""

from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse, PlainTextResponse
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

app.include_router(GraphQLRouter(schema=schema), prefix="/graphql")


# Serve the built frontend from the Vite `dist` directory.
DIST_DIR = (Path(__file__).resolve().parent / "dist").resolve()

# Mount assets (e.g., /assets/*) and any other static files referenced by absolute paths
assets_dir = DIST_DIR / "assets"
if assets_dir.exists():
    app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")

# Serve root index.html
@app.get("/", include_in_schema=False)
async def serve_index():
    index_file = DIST_DIR / "index.html"
    if index_file.exists():
        return FileResponse(index_file)
    return PlainTextResponse("Frontend build not found", status_code=404)

# Serve additional top-level files like /vite.svg if present
@app.get("/vite.svg", include_in_schema=False)
async def serve_vite_svg():
    svg_file = DIST_DIR / "vite.svg"
    if svg_file.exists():
        return FileResponse(svg_file)
    return PlainTextResponse("Not found", status_code=404)

# SPA fallback: route any unmatched, non-API GET path to index.html
@app.get("/{full_path:path}", include_in_schema=False)
async def spa_fallback(full_path: str, request: Request):
    # Let API and docs paths 404 naturally; otherwise serve the SPA
    if full_path.startswith(("graphql", "docs", "redoc", "openapi.json")):
        return PlainTextResponse("Not found", status_code=404)
    index_file = DIST_DIR / "index.html"
    if index_file.exists():
        return FileResponse(index_file)
    return PlainTextResponse("Frontend build not found", status_code=404)
