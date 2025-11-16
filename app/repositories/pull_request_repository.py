import uuid

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.config import lprint
from app.database import PullRequest, get_async_session, ReviewerPullRequestAssignment
from app.enums import PRStatus
from app.schemas import PullRequestOut


async def get_pr_repo(session: AsyncSession = Depends(get_async_session)):
    return PullRequestRepository(session)


class PullRequestRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_pull_request_by_id(self, pr_id: str) -> PullRequestOut:
        result = await self.session.execute(
            select(PullRequest)
            .where(PullRequest.id == pr_id)
            .options(
                selectinload(PullRequest.reviewers)
            )
        )
        pr = result.scalars().first()
        if not pr:
            raise ValueError("Pull Request not found")
        return PullRequestOut.model_validate(
            pr,
            from_attributes=True,
        )

    async def create_pull_request(self, name: str, author_id: str, reviewers: list[str]
                                  ) -> PullRequestOut:
        new_pr_id = uuid.uuid4()
        new_reviewers_pr_assignments = []
        for reviewer_id in reviewers:
            assignment = ReviewerPullRequestAssignment(
                pr_id=new_pr_id,
                user_id=reviewer_id,
            )
            new_reviewers_pr_assignments.append(assignment)
            self.session.add(assignment)
        new_pr = PullRequest(id=new_pr_id, name=name, author_id=author_id)
        self.session.add(new_pr)
        await self.session.commit()

        return await self.get_pull_request_by_id(pr_id=str(new_pr_id))

    async def get_pull_request_by_name_and_author(self, name: str, author_id: str
                                                  ) -> PullRequestOut | None:
        result = await self.session.execute(
            select(PullRequest)
            .where(PullRequest.name == name)
            .where(PullRequest.author_id == author_id)
            .options(
                selectinload(PullRequest.reviewers)
            )
        )
        pr = result.scalars().first()
        if not pr:
            return None
        return PullRequestOut.model_validate(
            pr,
            from_attributes=True,
        )

    async def merge_pull_request(self, pr_id: str, user_id: str
                                 ) -> PullRequestOut | None:
        result = await self.session.execute(
            select(PullRequest)
            .where(PullRequest.id == pr_id)
            .options(
                selectinload(PullRequest.reviewers)
            )
        )
        pr = result.scalars().first()
        if not pr:
            raise ValueError("Pull Request not found")
        if all(str(reviewer.id) != user_id for reviewer in pr.reviewers):
            raise NameError("User is not a reviewer of this Pull Request")
        if pr.status != PRStatus.MERGED:
            pr.status = PRStatus.MERGED
            await self.session.commit()

        return await self.get_pull_request_by_id(pr_id=pr_id)

    async def reassign_pull_request(self, pr_id: str, user_id: str,
                                    change_to_user_id: str
                                    ) -> PullRequestOut | None:
        result = await self.session.execute(
            select(PullRequest)
            .where(PullRequest.id == pr_id)
            .options(
                selectinload(PullRequest.reviewers)
            )
        )
        pr = result.scalars().first()
        if not pr:
            raise ValueError("Pull Request not found")
        if pr.status == PRStatus.MERGED:
            raise NameError("Cannot reassign reviewers for a merged Pull Request")
        lprint.debug([reviewer.id for reviewer in pr.reviewers])
        for reviewer in pr.reviewers:
            if str(reviewer.id) == user_id:
                break
        else:
            raise NameError("User is not a reviewer of this Pull Request")

        result = await self.session.execute(
            select(ReviewerPullRequestAssignment)
            .where(
                ReviewerPullRequestAssignment.pr_id == pr_id,
                ReviewerPullRequestAssignment.user_id == user_id
            )
        )
        pr_rev_assignment = result.scalars().first()
        pr_rev_assignment.user_id = uuid.UUID(change_to_user_id)
        await self.session.commit()

        return await self.get_pull_request_by_id(pr_id=pr_id)
