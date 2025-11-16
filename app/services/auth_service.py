from app.core.config import lprint
from app.core.security import PasswordUtils, create_jwt_token
from app.repositories.user_repository import UserRepository
from app.schemas import UserTokenData, UserOutWithPassword


class AuthService:
    @classmethod
    async def authenticate_user(cls,
                                username: str, password: str,
                                user_repo: UserRepository) -> dict | None:
        try:
            user = await user_repo.get_user_by_username(username)
            if not user:
                lprint.info(f"Authenticate: user not found by "
                            f"username={username}")
                return None
            if not PasswordUtils.verify_password(
                    password=password,
                    stored_hash=user.hashed_password):
                lprint.info(f"Authenticate: invalid password for user"
                            f" username={username}")
                return None
            lprint.debug("User authenticated:", username)
            token = await cls._create_access_token(user)
            return {"user_id": str(user.id), **token, "user_role": user.role}
        except Exception as e:
            lprint.error(f"Authenticate error for username={username}: {e}")
            return None

    @classmethod
    async def _create_access_token(cls, user: UserOutWithPassword
                                   ) -> dict[str, str]:
        payload = UserTokenData.model_validate(user.model_dump(mode="json"))
        lprint.debug("Payload: ", payload)
        access = create_jwt_token(data=payload)

        return {"access_token": access}
