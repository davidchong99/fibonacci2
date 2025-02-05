from sqlmodel import select, Session
from app.database.models import Blacklist


# Utility function to read current blacklist from postgres
def read_blacklist(session: Session) -> list:
    statement = select(Blacklist)
    results = session.exec(statement)
    current_blacklist = [result.black_list for result in results.all()]
    return current_blacklist
