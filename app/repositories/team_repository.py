from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.config import lprint
from app.database import Team, get_async_session
from app.schemas import TeamOut


async def get_team_repo(session: AsyncSession = Depends(get_async_session)):
    return TeamRepository(session)


class TeamRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_team_by_id(self, team_id: str) -> TeamOut | None:
        result = await self.session.execute(
            select(Team)
            .where(Team.id == team_id)
            .options(
                selectinload(Team.members)
            )
        )
        team = result.scalars().first()
        if team:
            lprint.info(f"Team found by ID: {team_id}")
            return TeamOut.model_validate(
                team,
                from_attributes=True,
            )
        return None

    async def get_team_by_name(self, team_name: str) -> TeamOut | None:
        result = await self.session.execute(
            select(Team)
            .where(Team.name == team_name)
            .options(
                selectinload(Team.members)
            )
        )
        team = result.scalars().first()
        if team:
            lprint.info(f"Team found by name: {team_name}")
            return TeamOut.model_validate(
                team,
                from_attributes=True,
            )
        return None

    async def add_team(self, team_name: str) -> TeamOut | None:
        try:
            new_team = Team(
                name=team_name,
            )
            self.session.add(new_team)
            await self.session.commit()
            await self.session.refresh(new_team)

            lprint.info(f"Team added: {new_team.id}")
            team_data = {
                "id": new_team.id,
                "name": new_team.name,
                "members": [],
            }
            return TeamOut.model_validate(team_data)
        except Exception as e:
            lprint.error(f"Error adding team: {str(e)}")
            return None

    async def get_team_members_to_review(self, team_id: str) -> list[str]:
        result = await self.session.execute(
            select(Team)
            .where(Team.id == team_id)
            .options(
                selectinload(Team.members)
            )
        )
        team = result.scalars().first()
        if not team:
            lprint.error(f"Team not found for ID: {team_id}")
            raise ValueError("Team not found")

        member_ids = [str(member.id) for member in team.members]
        lprint.info(f"Team members retrieved for team ID {team_id}: {member_ids}")
        return member_ids
