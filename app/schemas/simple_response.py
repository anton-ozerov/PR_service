from pydantic import BaseModel, Field


class SimpleResponse(BaseModel):
    message: str = Field(
        ...,
        description="Detailed message about the operation result"
    )
    status: bool = Field(
        ...,
        description="Indicates success (true) or failure (false)"
    )
