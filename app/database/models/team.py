import uuid
from typing import List, TYPE_CHECKING

from sqlalchemy import String, text
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.database.models import TimestampMixin

if TYPE_CHECKING:
    from app.database.models import User


class Team(Base, TimestampMixin):
    __tablename__ = 'team'

    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    name: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        index=True,
        nullable=False,
    )

    members: Mapped[List["User"]] = relationship(
        back_populates="team",
    )
