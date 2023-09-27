import hashlib
import json
from typing import Optional

import orjson
import sqlalchemy as sa
from fastapi import APIRouter, Depends, Request, Body
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.incident.models import Problem

router = APIRouter(tags=["Incident"])


@router.post("/problems")
async def add_problem(
    request: Request,
    body: dict = Body(),
    session: AsyncSession = Depends(get_async_session),
):
    header = {key: request.headers.get(key) for key in sorted(request.headers)}
    body = await request.json()
    body = {key: body[key] for key in body}
    hash_value = hashlib.md5(orjson.dumps({"header": header, "body": body})).hexdigest()
