import hashlib

import orjson
from fastapi import APIRouter, Body, Depends, Request
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.incident.schemas import (
    SAddProblemResponse,
    SFindByFilterResponse,
    SFindByKeyValue,
)
from src.incident.service import add_problem_to_db, filter_by_json_key_value, find_all

router = APIRouter(tags=["Incident"])


@router.post(
    "/problems", response_class=ORJSONResponse, response_model=SAddProblemResponse
)
async def add_problem(
    request: Request,
    body: dict = Body(),
    session: AsyncSession = Depends(get_async_session),
):
    """
    Add header, body and their hash value in to db.

    :returns: A hash str.
    """
    header = {key: request.headers.get(key) for key in sorted(request.headers)}

    # A body param is needed for sending request with body from swagger UI.
    # In other case, below construction will be used (but it has no data validation).
    # body = orjson.loads(await request.body())

    body = {key: body[key] for key in sorted(body)}
    hash_value = hashlib.md5(orjson.dumps({"header": header, "body": body})).hexdigest()

    # The return value from the database is necessary
    # because it guarantees that this record has been created.
    hash_value_to_return = await add_problem_to_db(hash_value, header, body, session)
    return hash_value_to_return


@router.post(
    "/find", response_model=SFindByFilterResponse, response_class=ORJSONResponse
)
async def find_by_key_val(
    filter_key_val_pair: SFindByKeyValue,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Find Problem records with given json key and value.

    :param filter_key_val_pair: A request body param with dict
    as key-value pair by which records will be searched.
    :returns: A dict with "result" as a key and list with 
    found by given key-value pair Problems presented by dicts as value.
    """
    # Convert input dict to tuple and take only first key-value pair.
    filter_key_val_pair = tuple(filter_key_val_pair.filter_by.items())[0]

    # Convert input json key and value to string type.
    filter_key_val_pair = tuple(map(lambda value: str(value), filter_key_val_pair))
    a = await filter_by_json_key_value(filter_key_val_pair, session)
    return {"result": a}


@router.get(
    "/find", response_class=ORJSONResponse, response_model=SFindByFilterResponse
)
async def get_problems_by_hash(
    h: str, session: AsyncSession = Depends(get_async_session)
):
    """
    Find Problem records wuth given hash.

    :param h: A query param with hash value by which records will be searched.
    :returns: A dict with "result" as a key and list with 
    found by given key-value pair Problems presented by dicts as value
    """
    problems = await find_all(session, hash_value=h)
    return {"result": problems}
