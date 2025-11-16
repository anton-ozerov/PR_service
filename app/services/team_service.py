from app.repositories import TeamRepository
from app.schemas import TeamOut


class TeamService:
    @classmethod
    async def get_team(cls, team_id: str,
                       team_repo: TeamRepository) -> TeamOut:
        team = await team_repo.get_team_by_id(team_id=team_id)
        if not team:
            raise ValueError("Team not found")

        return team

    @classmethod
    async def add_team(cls, team_name: str,
                       team_repo: TeamRepository) -> TeamOut:
        if await team_repo.get_team_by_name(team_name=team_name):
            raise ValueError("Team with this name already exists")

        team = await team_repo.add_team(team_name=team_name)
        if not team:
            raise Exception("Failed to add team")

        return team
