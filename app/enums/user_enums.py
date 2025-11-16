import enum


class UserRoleEnum(str, enum.Enum):
    ADMIN = "ADMIN"
    USER = "USER"
