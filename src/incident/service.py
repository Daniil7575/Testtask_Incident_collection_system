from src.incident.models import Problem
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import cast, String, Integer ,or_
from src.incident.models import Problem
import sqlalchemy as sa


async def add_problem_to_db(
    problem_hash: str, header: dict, body: dict, session: AsyncSession
) -> dict[str, str]:
    """
    Add problem to db.

    :param problem_hash: A hash value of header + body dict.
    :param header: A header wich will be added.
    :param body: A body wich will be added.
    :param session: Sqlalchemy session.
    :returns: A dict with hash_value from Problem model.
    """
    stmt = (
        sa.insert(Problem)
        .values(hash_value=problem_hash, header=header, body=body)
        .returning(Problem.hash_value)
    )
    new_problem = await session.execute(stmt)
    await session.commit()
    return new_problem.mappings().one()


async def filter_in_json(filter_key_val_pair, session: AsyncSession):
    # TODO: docstring
    """
    Find all records with given json key and value.

    :param filter_key_val_pair: Json key value pair by wich searching will 
    """
    print(filter_key_val_pair)
    filter_key, filter_value = filter_key_val_pair
    stmt = sa.select(
        Problem.id, Problem.hash_value, Problem.body, Problem.header
    ).where(
        or_(
            # Search in json field with given key
            cast(Problem.header.op("->>")(filter_key), Integer) == filter_value,
            cast(Problem.body.op("->>")(filter_key), Integer) == filter_value,
        )
    )
    filtered_json = await session.execute(stmt)
    filtered_json = filtered_json.mappings().all()
    print(filtered_json)
    return filtered_json


async def find_all(filter_key, filter_value, session: AsyncSession):
    pass