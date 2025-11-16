from fastapi import APIRouter

router = APIRouter(
    tags=["health"],
    responses={404: {"description": "Not found"}},
)


@router.get("/check", status_code=200)
async def health_check():
    """Health check endpoint to verify service is running"""
    return {
        "status": True,
        "message": "Service is healthy and running"
    }
