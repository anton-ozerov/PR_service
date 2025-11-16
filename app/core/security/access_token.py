from datetime import timedelta, datetime, UTC

import jwt
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer

from app.core.config import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    SECRET_KEY, ALGORITHM, lprint,
)
from app.schemas import UserTokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def create_jwt_token(data: UserTokenData) -> str:
    to_encode = data.model_dump()

    time_now = datetime.now(UTC)
    to_encode.update({"iat": time_now})
    expire = time_now + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    lprint.debug(to_encode)
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    lprint.debug("JWT token created:", encoded_jwt)
    return encoded_jwt


def decode_jwt_token(
        token: str | None = Depends(oauth2_scheme),
) -> dict:
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is required",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        # потом можно сделать автообновление токена
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate token",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_user_info_by_token(
        payload: dict = Depends(decode_jwt_token)
) -> UserTokenData:
    """Получение информации о пользователе из токена"""
    user_data = UserTokenData.model_validate(payload)
    return user_data
