import uuid
from typing import List, Optional, TYPE_CHECKING

from sqlalchemy import Boolean, ForeignKey, String, text
from sqlalchemy.dialects.postgresql import ENUM, UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.database.models import TimestampMixin
from app.enums import UserRoleEnum

if TYPE_CHECKING:
    from app.database.models import PullRequest
    from app.database.models import Team


class User(Base, TimestampMixin):
    __tablename__ = "user"

    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    username: Mapped[str] = mapped_column(
        String(150),
        unique=True,
        nullable=False,
    )
    hashed_password: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )
    role: Mapped[UserRoleEnum] = mapped_column(
        ENUM(UserRoleEnum, name="user_role_enum", create_constraint=True),
        default=UserRoleEnum.USER,
        nullable=False,
    )

    team_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey(
            "team.id",
            name="user_team_id_fkey",
            ondelete="SET NULL",
        ),
        nullable=True,
    )

    team: Mapped[Optional["Team"]] = relationship(
        back_populates="members",
    )
    pull_requests: Mapped[List["PullRequest"]] = relationship(
        back_populates="author",
    )
    pull_requests_as_reviewer: Mapped[List["PullRequest"]] = relationship(
        back_populates="reviewers",
        secondary="reviewer_pull_request_assignment",
    )
