from app.repositories import UserRepository
from app.schemas import UserOut


class UserService:
    @classmethod
    async def set_is_active(
        cls,
        user_repo: UserRepository,
        user_id: str,
        is_active: bool
    ) -> UserOut:
        user = await user_repo.get_user_by_id(user_id=user_id)
        if not user:
            raise ValueError("User not found")

        user.is_active = is_active
        updated_user = await user_repo.update_user(user=user)
        if not updated_user:
            raise Exception("Failed to update user active status")

        return updated_user

    @classmethod
    async def get_user_review(
        cls,
        user_repo: UserRepository,
        user_id: str
    ) -> dict:
        user_prs = await user_repo.get_user_prs_when_reviewer(user_id=user_id)
        return {"user_id": user_id, "prs": user_prs}
