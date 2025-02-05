from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, Depends, Query, status, HTTPException
from fastapi.responses import PlainTextResponse
from sqlmodel import Session

from app.database.database import create_db_and_tables, engine, get_session
from app.database.models import Blacklist
from app import service
from app.dto import SequenceResponse, PagedResponse, BlackListResponse


@asynccontextmanager
async def _app_lifespan(_: FastAPI) -> AsyncGenerator[None, None]:
    """
    Governs startup & shutdown of the app as recommended

    Args:
        _: the FastAPI app
    """
    create_db_and_tables()
    yield


def create_app() -> FastAPI:
    """
    Creates FastAPI app instance.
    Mounts routers, and adds a root endpoint.
    """

    # Create API
    app = FastAPI(title="Fibonacci API", version="1.0.0", lifespan=_app_lifespan)

    @app.get(
        "/{nterm}",
        response_model=SequenceResponse,
    )
    def get_fibonacci_sequence(
        nterm: int,
        session: Session = Depends(get_session),
    ) -> SequenceResponse:
        return service.get_fibonacci_sequence(nterm, session)

    @app.get(
        "/{nterm}/paged",
        response_model=PagedResponse,
    )
    def get_paged_fibonacci_sequence(
        nterm: int,
        page_number: int = Query(ge=0, description="Page number starting from 0"),
        session: Session = Depends(get_session),
    ):
        try:
            return service.get_paged_fibonacci_sequence(nterm, session, page_number)
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e),
            )

    @app.post(
        "/blacklist",
        response_model=BlackListResponse,
        status_code=status.HTTP_201_CREATED,
    )
    def add_blacklist(
        new_blacklist: Blacklist,
        session: Session = Depends(get_session),
    ):
        try:
            return service.add_blacklist(new_blacklist, session)
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e),
            )

    @app.delete(
        "/blacklist/{blacklist}",
        response_model=BlackListResponse,
    )
    def delete_blacklist(
        blacklist: int,
        session: Session = Depends(get_session),
    ):
        old_blacklist = Blacklist(black_list=blacklist)
        try:
            return service.delete_blacklist(old_blacklist, session)
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e),
            )

    @app.get("/", response_class=PlainTextResponse)
    async def get_root():
        return "Root ..."

    return app
