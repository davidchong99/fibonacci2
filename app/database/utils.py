from sqlalchemy.exc import NoResultFound
from sqlmodel import select, Session
from app.database.models import Blacklist, Results


# Utility function to read current blacklist from postgres
def read_blacklist(session: Session) -> list:
    statement = select(Blacklist)
    results = session.exec(statement)
    current_blacklist = [result.black_list for result in results.all()]
    return current_blacklist


def save_result_to_db(input: int, result: list[int], session: Session) -> None:
    new_result = Results(input=input, result=result)
    session.add(new_result)
    session.commit()


def read_result_from_db(input: int, session: Session) -> list[int] | None:
    try:
        statement = select(Results).where(Results.input == input)
        results = session.exec(statement)
        result = results.one()
    except NoResultFound:
        return None

    return result.result
