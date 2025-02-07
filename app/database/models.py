from typing import List

from pydantic import PositiveInt
from sqlalchemy import ARRAY, Column, Numeric
from sqlmodel import SQLModel, Field


# Table to store blacklist
class Blacklist(SQLModel, table=True):
    black_list: PositiveInt = Field(
        default=None, sa_column=Column(Numeric, primary_key=True, autoincrement=False)
    )


# Table to store results
class Results(SQLModel, table=True):
    input: PositiveInt = Field(
        default=None, sa_column=Column(Numeric, primary_key=True, autoincrement=False)
    )
    result: List[PositiveInt] = Field(sa_column=Column(ARRAY(Numeric)))
