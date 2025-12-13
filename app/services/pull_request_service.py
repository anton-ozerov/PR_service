from random import shuffle as rnd_shuffle

from app.core.config import COUNT_REVIEWERS_FOR_PR
from app.repositories import TeamRepository, UserRepository
from app.repositories.pull_request_repository import PullRequestRepository
from app.schemas import PullRequestOut


class PullRequestService:
    @classmethod
    async def get_pull_request_by_id(cls, pr_repo: PullRequestRepository, pr_id: str
                                     ) -> PullRequestOut:
        pr = await pr_repo.get_pull_request_by_id(pr_id=pr_id)
        if not pr:
            raise ValueError("Pull Request not found")
        return pr

    @classmethod
    async def _get_pull_request_by_name_and_author(
        cls,
        pr_repo: PullRequestRepository,
        name: str,
        author_id: str
    ) -> PullRequestOut | None:
        pr = await pr_repo.get_pull_request_by_name_and_author(
            name=name,
            author_id=author_id
        )
        if not pr:
            return None
        return pr

    @classmethod
    async def _get_reviewers(cls, user_id: str, team_repo: TeamRepository,
                             user_repo: UserRepository,
                             exclude_reviewers: list[str] | None,
                             need_count_reviewers: int = COUNT_REVIEWERS_FOR_PR
                             ) -> list[str]:
        if exclude_reviewers is None:
            exclude_reviewers = []
        user = await user_repo.get_user_by_id(user_id=user_id)
        if not user:
            raise ValueError("User not found")

        team = await team_repo.get_team_by_id(team_id=user.team_id)
        if not team:
            raise ValueError("Team not found")

        reviewers = set()
        team_members = team.members
        rnd_shuffle(team_members)

        for member in team_members:
            if (member.is_active and member.id != user_id and
                    member.id not in exclude_reviewers):
                reviewers.add(member.id)
                if len(reviewers) >= need_count_reviewers:
                    break

        return list(reviewers)


    @classmethod
    async def create_pull_request(cls, name: str, author_id: str,
                                  pr_repo: PullRequestRepository,
                                  team_repo: TeamRepository,
                                  user_repo: UserRepository) -> PullRequestOut:
        if await cls._get_pull_request_by_name_and_author(
                pr_repo=pr_repo, name=name, author_id=author_id):
            raise NameError("Pull Request with the same name already "
                            "exists for this author")

        reviewers = await cls._get_reviewers(user_id=author_id,
                                             team_repo=team_repo,
                                             user_repo=user_repo,
                                             exclude_reviewers=None)

        pr = await pr_repo.create_pull_request(name=name,
                                               author_id=author_id,
                                               reviewers=reviewers)
        if not pr:
            raise Exception("Failed to create Pull Request")

        return pr

    @classmethod
    async def merge_pull_request(cls, pr_repo: PullRequestRepository,
                                 pr_id: str, user_id: str) -> PullRequestOut:
        pr = await pr_repo.merge_pull_request(pr_id=pr_id, user_id=user_id)
        if not pr:
            raise ValueError("Pull Request not found")

        return pr

    @classmethod
    async def reassign_pull_request(cls, pr_id: str, user_id: str,
                                    pr_repo: PullRequestRepository,
                                    team_repo: TeamRepository,
                                    user_repo: UserRepository) -> PullRequestOut:
        pr_have = await pr_repo.get_pull_request_by_id(pr_id=pr_id)
        if not pr_have:
            raise ValueError("Pull Request not found")
        already_reviewers = [reviewer.id for reviewer in pr_have.reviewers]
        already_reviewers.append(pr_have.author_id)
        available_members = await cls._get_reviewers(
            user_id=user_id,
            team_repo=team_repo,
            user_repo=user_repo,
            exclude_reviewers=already_reviewers,
            need_count_reviewers=1
        )
        if not available_members:
            raise NameError("No available team members to assign as reviewers")
        pr = await pr_repo.reassign_pull_request(pr_id=pr_id,
                                                 user_id=user_id,
                                                 change_to_user_id=available_members[0])
        return pr
