from typing import List

from sqlalchemy import ARRAY, Column, Numeric
from sqlmodel import SQLModel, Field


class Blacklist(SQLModel, table=True):
    black_list: int = Field(
        default=None, sa_column=Column(Numeric, primary_key=True, autoincrement=False)
    )


class Results(SQLModel, table=True):
    input: int = Field(
        default=None, sa_column=Column(Numeric, primary_key=True, autoincrement=False)
    )
    result: List[int] = Field(sa_column=Column(ARRAY(Numeric)))
