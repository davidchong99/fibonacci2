from pydantic import BaseModel

# Use Pydantic to validate inputs and API response


class SequenceResponse(BaseModel):
    sequence: list[int]


class PagedResponse(BaseModel):
    page_number: int
    total_pages: int
    sequence: list[int]


class BlackListResponse(BaseModel):
    blacklists: list[int]
