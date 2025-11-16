from fastapi import APIRouter, HTTPException, Depends

from app.core.security import PermissionChecker, get_user_info_by_token
from app.enums import UserRoleEnum
from app.repositories import UserRepository, get_user_repo
from app.schemas import (
    UserSetIsActive, UserSetIsActiveResponse,
    UserTokenData, UserReviewPRsResponse
)
from app.services import UserService

router = APIRouter(
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@router.post("/setIsActive", response_model=UserSetIsActiveResponse)
@PermissionChecker([UserRoleEnum.ADMIN,])
async def set_is_active(
        data: UserSetIsActive,
        user_repo: UserRepository = Depends(get_user_repo),
        current_user: UserTokenData = Depends(get_user_info_by_token)
):
    """Set user active status (Admin only)"""
    try:
        user = await UserService.set_is_active(
            user_repo=user_repo,
            user_id=data.user_id,
            is_active=data.is_active,
        )

        return {
            "status": True,
            "message": f"User '{data.user_id}' active status set "
                       f"to {data.is_active}",
            "user": user
        }
    except ValueError:
        raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/getReview/{user_id}", response_model=UserReviewPRsResponse)
@PermissionChecker([UserRoleEnum.ADMIN,])
async def get_review_of_user(
        user_id: str,
        current_user: UserTokenData = Depends(get_user_info_by_token),
        user_repo: UserRepository = Depends(get_user_repo),
):
    """Get review of specified user (Admin only)"""
    try:
        prs = await UserService.get_user_review(
            user_repo=user_repo,
            user_id=user_id,
        )
        if prs is None:
            raise HTTPException(status_code=404, detail="User not found")
        return {
            "status": True,
            "message": f"Review data for user '{user_id}' retrieved successfully",
            "user_id": prs["user_id"],
            "reviews_in": prs["prs"],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/getReview", response_model=UserReviewPRsResponse)
async def get_review(
        current_user: UserTokenData = Depends(get_user_info_by_token),
        user_repo: UserRepository = Depends(get_user_repo),
):
    try:
        prs = await UserService.get_user_review(
            user_repo=user_repo,
            user_id=current_user.id,
        )
        if prs is None:
            raise HTTPException(status_code=404, detail="User not found")
        return {
            "status": True,
            "message": f"Review data for user '{current_user.id}'"
                       f" retrieved successfully",
            "user_id": prs["user_id"],
            "reviews_in": prs["prs"],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
