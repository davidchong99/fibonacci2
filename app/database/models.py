from typing import List

from pydantic import field_validator
from sqlalchemy import ARRAY, Column, Numeric
from sqlmodel import SQLModel, Field


# Table to store blacklist
class Blacklist(SQLModel, table=True):
    black_list: int = Field(
        default=None, sa_column=Column(Numeric, primary_key=True, autoincrement=False)
    )

    @field_validator("black_list", mode="after")
    def validate_blacklist_is_positive(cls, value: int) -> int:
        if not isinstance(value, int):
            raise ValueError("black_list must be an integer")
        if value <= 0:
            raise ValueError("black_list must be a positive number")
        return value


# Table to store results
class Results(SQLModel, table=True):
    input: int = Field(
        default=None, sa_column=Column(Numeric, primary_key=True, autoincrement=False)
    )
    result: List[int] = Field(sa_column=Column(ARRAY(Numeric)))
