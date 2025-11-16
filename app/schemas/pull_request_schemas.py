from uuid import UUID

from pydantic import Field, BaseModel, field_validator

from app.enums import PRStatus
from app.schemas import UserOut, SimpleResponse


class PullRequestCreate(BaseModel):
    name: str = Field(
        ...,
        min_length=3,
        max_length=70,
        description="Name of the pull request",
    )


class GetPullRequest(BaseModel):
    id: str | UUID = Field(
        ...,
        description="Unique identifier of the pull request in UUID format",
    )

    @field_validator("id")
    @classmethod
    def _validate_ids_are_uuid(cls, v: str) -> str:
        v = UUID(str(v))
        return str(v)


class PullRequestOut(PullRequestCreate, GetPullRequest):
    author_id: str | UUID = Field(
        ...,
        description="Unique identifier of the author of the "
                    "pull request in UUID format",
    )
    status: PRStatus = Field(
        ...,
        description="Status of the pull request",
    )
    reviewers: list[UserOut] = Field(
        ...,
        description="List of reviewers assigned to the pull request",
    )

    @field_validator("author_id")
    @classmethod
    def _validate_ids_are_uuid(cls, v: str) -> str:
        v = UUID(str(v))
        return str(v)


class PullRequestGetResponse(SimpleResponse):
    pull_request: PullRequestOut = Field(
        ...,
        description="Details of the created pull request",
    )
