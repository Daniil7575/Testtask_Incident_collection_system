from typing import Any
from pydantic import BaseModel


# Pydantic schema for post find method
class SFindByKeyValue(BaseModel):
    filter_data: dict[str, str | int]


class SFindByKeyValueResponse(BaseModel):
    found_records: list[dict[str, Any]]
