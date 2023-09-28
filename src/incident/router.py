import hashlib
import json
from typing import Optional

import orjson
import sqlalchemy as sa
from fastapi import APIRouter, Body, Depends, Request
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.incident.models import Problem
from src.incident.service import add_problem_to_db, find_all, filter_in_json
from src.incident.schemas import SFindByKeyValue, SFindByKeyValueResponse

router = APIRouter(tags=["Incident"])


@router.post("/problems", response_class=ORJSONResponse)
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
    # In other case, below construction will be used.
    # body = orjson.loads(await request.body())

    body = {key: body[key] for key in sorted(body)}
    hash_value = hashlib.md5(orjson.dumps({"header": header, "body": body})).hexdigest()

    # The return value from the database is necessary
    # because it guarantees that this record has been created.
    hash_value_to_return = await add_problem_to_db(hash_value, header, body, session)
    return hash_value_to_return["hash_value"]


@router.post(
    "/find",
    # response_model=SFindByKeyValueResponse,
    response_class=ORJSONResponse
)
async def find_by_key_val(
    filter_key_val_pair: SFindByKeyValue,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Find records with given json key and value.
    """
    # Convert input dict to tuple.
    filter_key_val_pair = tuple(filter_key_val_pair.filter_data.items())[0]

    # Convert input json key and value to string type.
    filter_key_val_pair = tuple(
        map(lambda value: str(value), filter_key_val_pair)
    )
    a = await filter_in_json(filter_key_val_pair, session)
    # return {"found_records": a}
