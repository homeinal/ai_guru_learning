from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from typing import List

from app.db.neon import get_db
from app.models.db_models import User, Guru, user_gurus
from app.models.schemas import UserCreate, UserResponse, UserGuruUpdate, GuruResponse

router = APIRouter()


@router.post("/sync", response_model=UserResponse)
async def sync_user(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    """Google OAuth 로그인 시 사용자 동기화 (생성 또는 업데이트)"""
    # 기존 사용자 확인
    result = await db.execute(
        select(User).where(User.google_id == user_data.google_id)
    )
    user = result.scalar_one_or_none()

    if user:
        # 기존 사용자 업데이트
        user.email = user_data.email
        user.name = user_data.name
        user.avatar_url = user_data.avatar_url
    else:
        # 새 사용자 생성
        user = User(
            google_id=user_data.google_id,
            email=user_data.email,
            name=user_data.name,
            avatar_url=user_data.avatar_url,
        )
        db.add(user)

    await db.flush()
    await db.refresh(user)
    return user


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: str, db: AsyncSession = Depends(get_db)):
    """사용자 정보 조회"""
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


@router.get("/{user_id}/gurus", response_model=List[GuruResponse])
async def get_user_gurus(user_id: str, db: AsyncSession = Depends(get_db)):
    """사용자가 팔로우하는 Guru 목록 조회"""
    result = await db.execute(
        select(User)
        .options(selectinload(User.followed_gurus))
        .where(User.id == user_id)
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user.followed_gurus


@router.put("/{user_id}/gurus", response_model=List[GuruResponse])
async def update_user_gurus(
    user_id: str,
    guru_update: UserGuruUpdate,
    db: AsyncSession = Depends(get_db),
):
    """사용자 관심 Guru 업데이트"""
    # 사용자 조회
    result = await db.execute(
        select(User)
        .options(selectinload(User.followed_gurus))
        .where(User.id == user_id)
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Guru 목록 조회
    guru_result = await db.execute(
        select(Guru).where(Guru.id.in_(guru_update.guru_ids))
    )
    gurus = guru_result.scalars().all()

    # 관계 업데이트
    user.followed_gurus = list(gurus)
    await db.flush()

    return user.followed_gurus


@router.get("/by-google/{google_id}", response_model=UserResponse)
async def get_user_by_google_id(google_id: str, db: AsyncSession = Depends(get_db)):
    """Google ID로 사용자 조회"""
    result = await db.execute(select(User).where(User.google_id == google_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user
