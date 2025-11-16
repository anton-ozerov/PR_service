import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

from app.database import Base


class ReviewerPullRequestAssignment(Base):
    __tablename__ = "reviewer_pull_request_assignment"

    user_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey(
            "user.id",
            name="reviewer_pr_assignment_user_id_fkey",
            ondelete="CASCADE",
        ),
        primary_key=True,
    )
    pr_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey(
            "pull_request.id",
            name="reviewer_pr_assignment_pr_id_fkey",
            ondelete="CASCADE",
        ),
        primary_key=True,
    )
