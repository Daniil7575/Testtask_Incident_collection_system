import uuid
from typing import Any

from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class Problem(Base):
    __tablename__ = "problem"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4())
    hash_value: Mapped[str]
    header: Mapped[dict[str, Any]] = mapped_column(JSONB)
    body: Mapped[dict[str, Any]] = mapped_column(JSONB)
