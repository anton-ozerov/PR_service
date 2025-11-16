import uuid
from typing import Optional, TYPE_CHECKING

from sqlalchemy import text, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, ENUM
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.database import Base
from app.database.models import TimestampMixin
from app.enums import PRStatus

if TYPE_CHECKING:
    from app.database.models import User


class PullRequest(Base, TimestampMixin):
    __tablename__ = "pull_request"

    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    name: Mapped[Optional[str]] = mapped_column(
        String(70),
        nullable=True,
    )
    status: Mapped[PRStatus] = mapped_column(
        ENUM(PRStatus,
             name="pull_request_status_enum",
             create_constraint=True),
        default=PRStatus.OPEN,
        nullable=False,
    )

    author_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey(
            "user.id",
            name="pull_request_author_id_fkey",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    author: Mapped["User"] = relationship(
        back_populates="pull_requests",
    )

    reviewers: Mapped[list["User"]] = relationship(
        back_populates="pull_requests_as_reviewer",
        secondary="reviewer_pull_request_assignment",
    )
