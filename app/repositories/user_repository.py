from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.config import lprint
from app.database import User, get_async_session, PullRequest
from app.schemas import UserOutWithPassword, UserOut, PullRequestOut


async def get_user_repo(session: AsyncSession = Depends(get_async_session)):
    return UserRepository(session)


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_by_username(self, username: str
                                   ) -> UserOutWithPassword | None:
        result = await self.session.execute(
            select(User)
            .where(User.username == username)
            .options(selectinload(User.team))
        )
        user = result.scalars().first()
        if user:
            lprint.info("User found by username:", user.username)
            return UserOutWithPassword.model_validate(
                user,
                from_attributes=True,
            )
        return None

    async def get_user_by_id(self, user_id: str) -> UserOutWithPassword | None:
        result = await self.session.execute(
            select(User)
            .where(User.id == user_id)
            .options(selectinload(User.team))
        )
        user = result.scalars().first()
        if user:
            lprint.info("User found by ID:", user.id)
            return UserOutWithPassword.model_validate(
                user,
                from_attributes=True,
            )
        return None

    async def update_user(self, user: UserOutWithPassword) -> UserOut | None:
        result = await self.session.execute(
            select(User)
            .where(User.id == user.id)
            .options(selectinload(User.team))
        )
        user_db = result.scalars().one_or_none()
        if user_db:
            try:
                for field, value in user.model_dump(exclude_unset=True).items():
                    setattr(user_db, field, value)
                await self.session.commit()
                await self.session.refresh(user_db)
                lprint.info("User updated:", user.id)
                return UserOut.model_validate(
                    user_db,
                    from_attributes=True,
                )
            except Exception as e:
                lprint.error(f"Error updating user {user.id}: {str(e)}")
                await self.session.rollback()
                return None
        else:
            lprint.warning("User not found for update:", user.id)
            return None

    async def get_user_prs_when_reviewer(self, user_id: str
                                         ) -> list[PullRequestOut] | None:
        result = await self.session.execute(
            select(User)
            .where(User.id == user_id)
            .options(
                selectinload(User.team),
                selectinload(User.pull_requests_as_reviewer)
                .selectinload(PullRequest.reviewers),
            )
        )
        user = result.scalars().first()
        if not user:
            lprint.warning("User not found for review:", user_id)
            return None

        prs = []
        for pr in user.pull_requests_as_reviewer:
            prs.append(
                PullRequestOut
                .model_validate(pr, from_attributes=True)
                .model_dump(mode="json")
            )
        return prs
