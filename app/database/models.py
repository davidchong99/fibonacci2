from typing import List

from sqlalchemy import ARRAY, Column, Integer
from sqlmodel import SQLModel, Field


class Blacklist(SQLModel, table=True):
    black_list: int = Field(default=None, primary_key=True)


class Results(SQLModel, table=True):
    input: int = Field(default=None, primary_key=True)
    result: List[int] = Field(sa_column=Column(ARRAY(Integer)))
