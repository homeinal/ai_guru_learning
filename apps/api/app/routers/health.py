from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health_check():
    """헬스체크 엔드포인트 (Render 슬립 방지용)"""
    return {"status": "healthy", "service": "ai-learning-tracker-api"}
