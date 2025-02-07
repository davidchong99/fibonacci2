from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI
from typing_extensions import AsyncGenerator
from fastapi.responses import PlainTextResponse
from app.database.models import Blacklist, Results
from app.database.database import create_db_and_tables
from app.env import SETTINGS
from app.fibonacci_router import fibonacci


@asynccontextmanager
async def _app_lifespan(_: FastAPI) -> AsyncGenerator[None, None]:
    """
    Governs startup & shutdown of the app as recommended

    Args:
        _: the FastAPI app
    """
    # Create database tables before app starts
    create_db_and_tables()
    yield


app = FastAPI(title="Fibonacci API", version="1.0.0", lifespan=_app_lifespan)

app.include_router(fibonacci.router)


@app.get("/", response_class=PlainTextResponse)
def get_root():
    return "Root ..."


if __name__ == "__main__":
    # Start server
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=SETTINGS.server_port,
        log_level=SETTINGS.server_log_level,
    )
