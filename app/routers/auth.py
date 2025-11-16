from fastapi import APIRouter, HTTPException, Depends

from app.repositories import UserRepository, get_user_repo
from app.schemas import UserLogin, LoginUserResponse
from app.services import AuthService

router = APIRouter(
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)


@router.post("/login", response_model=LoginUserResponse)
async def login(user_in: UserLogin,
                user_repo: UserRepository = Depends(get_user_repo)):
    """Вход пользователя по логину и паролю, получение JWT токена"""
    res = await AuthService.authenticate_user(username=user_in.username,
                                              password=user_in.password,
                                              user_repo=user_repo)
    if not res:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {
        "status": True,
        "message": "Login successful",
        "access_token": res["access_token"],
        "token_type": "bearer",
        "user_id": res["user_id"],
        "user_role": res["user_role"],
    }
