from pydantic import BaseModel


class SequenceResponse(BaseModel):
    sequence: list[int]


class PagedResponse(BaseModel):
    page_number: int
    total_pages: int
    sequence: list[int]


class BlackListResponse(BaseModel):
    blacklists: list[int]
