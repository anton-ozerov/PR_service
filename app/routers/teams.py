from fastapi import APIRouter, Depends, HTTPException

from app.core.security import PermissionChecker, get_user_info_by_token
from app.enums import UserRoleEnum
from app.repositories import get_team_repo, TeamRepository
from app.schemas import UserTokenData, GetTeamResponse, TeamCreate
from app.services.team_service import TeamService

router = APIRouter(
    tags=["team"],
    responses={404: {"description": "Not found"}},
)


@router.get("/get", response_model=GetTeamResponse)
async def get_team(
    current_user: UserTokenData = Depends(get_user_info_by_token),
    team_repo: TeamRepository = Depends(get_team_repo),
):
    try:
        team = await TeamService.get_team(
            team_id=current_user.team_id,
            team_repo=team_repo,
        )
        return {
            "status": True,
            "message": f"Team '{current_user.team_id}' retrieved successfully",
            "team": team,
        }
    except ValueError:
        raise HTTPException(status_code=404, detail="Team not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/get/{team_id}", response_model=GetTeamResponse)
@PermissionChecker([UserRoleEnum.ADMIN,])
async def get_team_by_id(
    team_id: str,
    current_user: UserTokenData = Depends(get_user_info_by_token),
    team_repo: TeamRepository = Depends(get_team_repo),
):
    """Get team by ID (Admin only)"""
    try:
        team = await TeamService.get_team(
            team_id=team_id,
            team_repo=team_repo,
        )
        return {
            "status": True,
            "message": f"Team '{team_id}' retrieved successfully",
            "team": team,
        }
    except ValueError:
        raise HTTPException(status_code=404, detail="Team not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.post("/add", response_model=GetTeamResponse, status_code=201)
@PermissionChecker([UserRoleEnum.ADMIN,])
async def add_team(
    data: TeamCreate,
    current_user: UserTokenData = Depends(get_user_info_by_token),
    team_repo: TeamRepository = Depends(get_team_repo),
):
    """Add team (Admin only)"""
    try:
        new_team = await TeamService.add_team(
            team_name=data.name,
            team_repo=team_repo,
        )
        return {
            "status": True,
            "message": "Team added successfully",
            "team": new_team,
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
