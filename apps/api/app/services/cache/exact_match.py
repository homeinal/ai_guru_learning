import hashlib
import json
from datetime import datetime, timedelta, timezone
from typing import Optional, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.db_models import QueryCache
from app.config import get_settings

settings = get_settings()


def generate_query_hash(query: str) -> str:
    """쿼리 문자열의 해시 생성 (정규화 후)"""
    # 소문자로 변환, 공백 정리
    normalized = " ".join(query.lower().strip().split())
    return hashlib.sha256(normalized.encode()).hexdigest()[:32]


async def get_cached_response(
    db: AsyncSession,
    query: str,
) -> Optional[Tuple[str, list]]:
    """
    캐시된 응답 조회

    Returns:
        (response, sources) 튜플 또는 None
    """
    query_hash = generate_query_hash(query)
    now = datetime.now(timezone.utc)

    result = await db.execute(
        select(QueryCache).where(
            QueryCache.query_hash == query_hash,
            QueryCache.expires_at > now,
        )
    )
    cache_entry = result.scalar_one_or_none()

    if cache_entry:
        # 히트 카운트 증가
        cache_entry.hit_count += 1
        await db.flush()

        sources = json.loads(cache_entry.sources) if cache_entry.sources else []
        return cache_entry.response, sources

    return None


async def save_to_cache(
    db: AsyncSession,
    query: str,
    response: str,
    sources: list = None,
) -> None:
    """응답을 캐시에 저장"""
    query_hash = generate_query_hash(query)
    now = datetime.now(timezone.utc)
    expires_at = now + timedelta(hours=settings.cache_ttl_hours)

    # 기존 캐시 확인 (만료된 것 포함)
    result = await db.execute(
        select(QueryCache).where(QueryCache.query_hash == query_hash)
    )
    existing = result.scalar_one_or_none()

    if existing:
        # 기존 캐시 업데이트
        existing.response = response
        existing.sources = json.dumps(sources) if sources else None
        existing.expires_at = expires_at
        existing.hit_count = 0
    else:
        # 새 캐시 생성
        cache_entry = QueryCache(
            query_hash=query_hash,
            query_text=query,
            response=response,
            sources=json.dumps(sources) if sources else None,
            expires_at=expires_at,
        )
        db.add(cache_entry)

    await db.flush()


async def invalidate_cache(db: AsyncSession, query: str) -> bool:
    """특정 쿼리 캐시 무효화"""
    query_hash = generate_query_hash(query)

    result = await db.execute(
        select(QueryCache).where(QueryCache.query_hash == query_hash)
    )
    cache_entry = result.scalar_one_or_none()

    if cache_entry:
        await db.delete(cache_entry)
        await db.flush()
        return True

    return False
