from fastapi import APIRouter, Depends, HTTPException

from app.core.security import get_user_info_by_token
from app.repositories import (
    get_pr_repo, PullRequestRepository,
    get_team_repo, TeamRepository,
    get_user_repo, UserRepository
)
from app.schemas import UserTokenData, PullRequestCreate, PullRequestGetResponse
from app.schemas.pull_request_schemas import GetPullRequest
from app.services import PullRequestService

router = APIRouter(
    tags=["PullRequest"],
    responses={404: {"description": "Not found"}},
)


@router.post("/create", response_model=PullRequestGetResponse, status_code=201)
async def create_pr(
    data: PullRequestCreate,
    current_user: UserTokenData = Depends(get_user_info_by_token),
    pr_repo: PullRequestRepository = Depends(get_pr_repo),
    team_repo: TeamRepository = Depends(get_team_repo),
    user_repo: UserRepository = Depends(get_user_repo),
):
    """Create a new pull request"""
    try:
        pr = await PullRequestService.create_pull_request(
            pr_repo=pr_repo,
            author_id=current_user.id,
            name=data.name,
            team_repo=team_repo,
            user_repo=user_repo,
        )
        return {
            "status": True,
            "message": "Pull Request created successfully",
            "pull_request": pr
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except NameError as e:
        raise HTTPException(status_code=409, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.post("/merge", response_model=PullRequestGetResponse)
async def merge_pr(
    data: GetPullRequest,
    current_user: UserTokenData = Depends(get_user_info_by_token),
    pr_repo: PullRequestRepository = Depends(get_pr_repo),
):
    """Merge a pull request (Placeholder endpoint)"""
    try:
        pr = await PullRequestService.merge_pull_request(
            pr_repo=pr_repo,
            pr_id=data.id,
            user_id=current_user.id
        )
        return {
            "status": True,
            "message": "Pull Request merged successfully",
            "pull_request": pr
        }
    except NameError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.post("/reassign", response_model=PullRequestGetResponse)
async def reassign_pr(
    data: GetPullRequest,
    current_user: UserTokenData = Depends(get_user_info_by_token),
    pr_repo: PullRequestRepository = Depends(get_pr_repo),
    team_repo: TeamRepository = Depends(get_team_repo),
    user_repo: UserRepository = Depends(get_user_repo),
):
    """Reassign reviewers for a pull request"""
    try:
        pr = await PullRequestService.reassign_pull_request(
            pr_repo=pr_repo,
            pr_id=data.id,
            user_id=current_user.id,
            team_repo=team_repo,
            user_repo=user_repo
        )
        return {
            "status": True,
            "message": "Pull Request reassigned successfully",
            "pull_request": pr
        }
    except NameError as e:
        raise HTTPException(status_code=409, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
