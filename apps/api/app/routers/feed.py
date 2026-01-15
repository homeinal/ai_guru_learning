from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from sqlalchemy.orm import selectinload
from typing import List, Optional

from app.db.neon import get_db
from app.models.db_models import User, Guru, GuruPost
from app.models.schemas import GuruResponse, PostResponse, FeedResponse

router = APIRouter()


@router.get("/gurus", response_model=List[GuruResponse])
async def get_all_gurus(db: AsyncSession = Depends(get_db)):
    """모든 Guru 목록 조회"""
    result = await db.execute(select(Guru).order_by(Guru.name))
    gurus = result.scalars().all()
    return gurus


@router.get("", response_model=FeedResponse)
async def get_feed(
    user_id: Optional[str] = Query(None),
    guru_ids: Optional[str] = Query(None, description="콤마로 구분된 guru_id 목록"),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
):
    """
    피드 조회
    - user_id가 있으면 해당 사용자가 팔로우하는 Guru의 포스트
    - guru_ids가 있으면 해당 Guru들의 포스트
    - 둘 다 없으면 전체 포스트
    """
    # 필터링할 Guru ID 결정
    filter_guru_ids = []

    if user_id:
        # 사용자의 팔로우 Guru 조회
        result = await db.execute(
            select(User)
            .options(selectinload(User.followed_gurus))
            .where(User.id == user_id)
        )
        user = result.scalar_one_or_none()
        if user:
            filter_guru_ids = [g.id for g in user.followed_gurus]
    elif guru_ids:
        filter_guru_ids = [gid.strip() for gid in guru_ids.split(",")]

    # 포스트 쿼리 빌드
    query = select(GuruPost).options(selectinload(GuruPost.guru))

    if filter_guru_ids:
        query = query.where(GuruPost.guru_id.in_(filter_guru_ids))

    # 총 개수 조회
    count_query = select(GuruPost)
    if filter_guru_ids:
        count_query = count_query.where(GuruPost.guru_id.in_(filter_guru_ids))
    count_result = await db.execute(count_query)
    total = len(count_result.scalars().all())

    # 페이지네이션 적용
    query = query.order_by(desc(GuruPost.posted_at)).offset(offset).limit(limit)
    result = await db.execute(query)
    posts = result.scalars().all()

    return FeedResponse(
        posts=posts,
        total=total,
        has_more=(offset + len(posts)) < total,
    )


@router.get("/guru/{guru_id}/posts", response_model=List[PostResponse])
async def get_guru_posts(
    guru_id: str,
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
):
    """특정 Guru의 포스트 조회"""
    result = await db.execute(
        select(GuruPost)
        .options(selectinload(GuruPost.guru))
        .where(GuruPost.guru_id == guru_id)
        .order_by(desc(GuruPost.posted_at))
        .offset(offset)
        .limit(limit)
    )
    posts = result.scalars().all()
    return posts
