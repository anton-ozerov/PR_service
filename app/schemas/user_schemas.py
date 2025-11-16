from uuid import UUID

from pydantic import BaseModel, Field, field_validator

from app.enums import UserRoleEnum
from app.schemas import SimpleResponse


class UserTokenData(BaseModel):
    id: str | UUID = Field(
        ...,
        description="Unique identifier of the user in UUID format"
    )
    role: UserRoleEnum = Field(
        ...,
        description="Role of the user in the system"
    )
    team_id: str | UUID | None = Field(
        None,
        description="Identifier of the team the user belongs to"
    )

    @field_validator("id", "team_id")
    @classmethod
    def _validate_id_is_uuid(cls, v: str) -> str:
        if v is not None:
            v = str(UUID(str(v)))
        return v


class UserLogin(BaseModel):
    username: str = Field(
        ..., min_length=3, max_length=150,
        description="Username of the user"
    )
    password: str = Field(
        ..., min_length=3, max_length=128,
        description="Password of the user"
    )


class UserOut(UserTokenData):
    username: str = Field(
        ...,
        description="Username of the user"
    )
    is_active: bool = Field(
        ...,
        description="Indicates if the user is active"
    )
    team_id: str | UUID | None = Field(
        None,
        description="Identifier of the team the user belongs to"
    )

    @field_validator("team_id")
    @classmethod
    def _validate_team_id_is_uuid(cls, v: str | None) -> str | None:
        if v is not None:
            UUID(str(v))
            v = str(v)
        return v


class UserOutWithPassword(UserOut):
    hashed_password: str


class LoginUserResponse(SimpleResponse):
    access_token: str = Field(
        ...,
        description="JWT access token"
    )
    token_type: str = Field(
        ...,
        description="Type of the token, typically 'bearer'"
    )
    user_id: UUID | str = Field(
        ...,
        description="Unique identifier of the user"
    )
    user_role: UserRoleEnum = Field(
        ...,
        description="Role of the user in the system"
    )

    @field_validator("user_id")
    @classmethod
    def _validate_user_id_is_uuid(cls, v: str) -> str:
        v = UUID(str(v))
        return str(v)


class UserSetIsActive(BaseModel):
    user_id: UUID | str = Field(
        ...,
        description="Unique identifier of the user to be updated"
    )
    is_active: bool = Field(
        ...,
        description="Indicates whether the user should be active or inactive"
    )

    @field_validator("user_id")
    @classmethod
    def _validate_user_id_is_uuid(cls, v: str) -> str:
        v = UUID(str(v))
        return str(v)


class UserSetIsActiveResponse(SimpleResponse):
    user: UserOut = Field(
        ...,
        description="The updated user object"
    )


class UserReviewPRsResponse(SimpleResponse):
    user_id: UUID | str = Field(
        ...,
        description="Unique identifier of the user"
    )
    reviews_in: list[dict] = Field(
        ...,
        description="List of pull requests assigned to the user for review"
    )

    @field_validator("user_id")
    @classmethod
    def _validate_user_id_is_uuid(cls, v: str) -> str:
        v = UUID(str(v))
        return str(v)
