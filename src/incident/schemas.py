from typing import Any

from pydantic import BaseModel


# Pydantic schema for post find method.
class SFindByKeyValue(BaseModel):
    filter_by: dict[str, str | int]

    model_config = {
        "json_schema_extra": {"examples": [{"filter_by": {"key": "value"}}]}
    }


# Response schema for founded Problem records.
class SFindByFilterResponse(BaseModel):
    result: list[dict[str, Any]]


# Response schema for added Problem record.
class SAddProblemResponse(BaseModel):
    hash_value: str
