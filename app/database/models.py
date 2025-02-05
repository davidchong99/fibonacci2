from sqlmodel import SQLModel, Field


class Blacklist(SQLModel, table=True):
    black_list: int = Field(default=None, primary_key=True)
