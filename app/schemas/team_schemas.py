from uuid import UUID

from pydantic import BaseModel, Field, field_validator

from app.schemas import UserOut, SimpleResponse


class TeamCreate(BaseModel):
    name: str = Field(
        ...,
        min_length=3,
        max_length=50,
        description="Name of the team",
    )


class TeamOut(TeamCreate):
    id: UUID | str = Field(
        ...,
        description="Unique identifier of the team in UUID format",
    )
    members: list[UserOut] = Field(
        ...,
        description="List of users who are members of the team",
    )

    @field_validator("id")
    @classmethod
    def _validate_id_is_uuid(cls, v: str) -> str:
        v = UUID(str(v))
        return str(v)


class GetTeamResponse(SimpleResponse):
    team: TeamOut = Field(
        ...,
        description="Team data",
    )
