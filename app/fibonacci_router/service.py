from sqlmodel import Session, select

from app.database.models import Blacklist
from app.database.utils import read_blacklist_from_db, read_result_from_db, save_result_to_db
from app.fibonacci_router.dto import BlackListResponse, SequenceResponse, PagedResponse

PAGE_SIZE = 100


def fibonacci(nterm: int) -> list:
    a = 0
    b = 1
    result = [a]
    while b <= nterm:
        result.append(b)
        a, b = b, a + b

    return result


def get_fibonacci_sequence(nterm: int, session: Session) -> SequenceResponse:
    # Retrieve saved results if available
    saved_result = read_result_from_db(nterm, session)

    if saved_result:
        return SequenceResponse(sequence=saved_result)

    # Perform calculation if there is no stored results
    result = fibonacci(nterm)

    # Save results in db for future use
    save_result_to_db(nterm, result, session)

    # Read the current black list from Postgres
    current_blacklist = read_blacklist_from_db(session)

    # Filter the blacklisted number from the sequence
    result = [x for x in result if x not in current_blacklist]

    return SequenceResponse(sequence=result)


def get_paged_fibonacci_sequence(
    nterm: int, session: Session, page_number: int = 0
) -> PagedResponse:
    # Retrieve saved results if available
    saved_result = read_result_from_db(nterm, session)

    if saved_result:
        result = saved_result
    else:
        result = fibonacci(nterm)
        save_result_to_db(nterm, result, session)

    # Read the current black list from Postgres
    current_blacklist = read_blacklist_from_db(session)

    # Filter the blacklisted number from the sequence
    result = [x for x in result if x not in current_blacklist]

    # If the result length is more than 100, split it into pages
    total_pages = 1
    if len(result) > PAGE_SIZE:
        total_pages = int(len(result) / PAGE_SIZE + 1)

    pages = []
    for i in range(total_pages):
        pages.append(result[i * PAGE_SIZE : (i + 1) * PAGE_SIZE])

    # Check for out of bounds page number
    if page_number >= total_pages:
        raise ValueError("Page number out of bounds")

    return PagedResponse(
        page_number=page_number,
        total_pages=total_pages,
        sequence=pages[page_number],
    )


def add_blacklist(to_be_added: Blacklist, session: Session) -> BlackListResponse:
    # Read the current black list from Postgres
    current_blacklist = read_blacklist_from_db(session)

    # Add new blacklist if it does not exist in the current blacklist
    if to_be_added.black_list not in current_blacklist:
        new_blacklist = Blacklist.model_validate(to_be_added)
        session.add(new_blacklist)
        session.commit()
        current_blacklist.append(new_blacklist.black_list)
    else:
        raise ValueError("Blacklist already exists")

    return BlackListResponse(blacklists=current_blacklist)


def delete_blacklist(to_be_deleted: Blacklist, session: Session) -> BlackListResponse:
    # Read the current black list from Postgres
    current_blacklist = read_blacklist_from_db(session)

    # Delete the blacklist if it exists in the current blacklist
    if to_be_deleted.black_list in current_blacklist:
        statement = select(Blacklist).where(
            Blacklist.black_list == to_be_deleted.black_list
        )
        results = session.exec(statement)
        blacklist = results.one()

        session.delete(blacklist)
        session.commit()
        current_blacklist.remove(blacklist.black_list)
    else:
        raise ValueError("Blacklist does not exist")

    return BlackListResponse(blacklists=current_blacklist)
