from fastapi import APIRouter, Depends

router = APIRouter(
    prefix="/health",
    tags=["health"]
)

@router.get("/")
async def health_check():
    return {"status": "healthy"}