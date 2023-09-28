from typing import Any

import sqlalchemy as sa
from sqlalchemy import or_
from sqlalchemy.ext.asyncio import AsyncSession

from src.incident.models import Problem


async def add_problem_to_db(
    problem_hash: str, header: dict, body: dict, session: AsyncSession
) -> dict[str, str]:
    """
    Add problem to db.

    :param problem_hash: A hash value of header + body dict.
    :param header: A header wich will be added.
    :param body: A body wich will be added.
    :param session: Sqlalchemy session.
    :returns: A dict with hash value from Problem model.
    """
    stmt = (
        sa.insert(Problem)
        .values(hash_value=problem_hash, header=header, body=body)
        .returning(Problem.hash_value)
    )
    new_problem = await session.execute(stmt)
    await session.commit()
    return new_problem.mappings().one()


async def filter_by_json_key_value(
    filter_key_val_pair: tuple[str, str], session: AsyncSession
) -> list[dict[str, Any]]:
    """
    Find all records with given json key and value.

    :param filter_key_val_pair: Json key-value pair
    that the search will be performed on.
    :param session: Sqlalchemy session.
    :returns: A list with found by given key-value pair Problems presented by dicts.
    """
    filter_key, filter_value = filter_key_val_pair
    stmt = sa.select(
        Problem.id, Problem.hash_value, Problem.body, Problem.header
    ).where(
        or_(
            # Search in json field with given key and given value
            Problem.header.op("->>")(filter_key) == filter_value,
            Problem.body.op("->>")(filter_key) == filter_value,
        )
    )
    filtered_json = await session.execute(stmt)
    filtered_json = filtered_json.mappings().all()
    return filtered_json


async def find_all(session: AsyncSession, **filter_by) -> list[dict[str, Any]]:
    """
    Find all records with given filter.

    :param session: Sqlalchemy session.
    :param **filter_by: Filter keyword arguments.
    ::
        :keyword hash_value: Find problems by hash_value column.
        :keyword hash_value value: A hash value of problem body and header.
    :returns: A list with found by given hash Problems presented by dicts.
    """
    stmt = sa.select(
        Problem.id, Problem.hash_value, Problem.body, Problem.header
    ).filter_by(**filter_by)
    filtered_json = await session.execute(stmt)
    filtered_json = filtered_json.mappings().all()
    return filtered_json
