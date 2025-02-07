from fastapi import APIRouter, Depends, Query, status, HTTPException
from sqlmodel import Session

from app.database.database import get_session
from app.database.models import Blacklist
from app.fibonacci_router import service
from app.fibonacci_router.dto import SequenceResponse, PagedResponse, BlackListResponse

router = APIRouter()


@router.get(
    "/{nterm}",
    response_model=SequenceResponse,
)
def get_fibonacci_sequence(
    nterm: int,
    session: Session = Depends(get_session),
) -> SequenceResponse:
    return service.get_fibonacci_sequence(nterm, session)


@router.get(
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


@router.post(
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


@router.delete(
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
