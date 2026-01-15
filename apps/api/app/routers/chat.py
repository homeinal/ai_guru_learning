from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timezone
import uuid

from app.db.neon import get_db
from app.models.schemas import ChatRequest, ChatResponse, ChatMessageResponse, ChatSource
from app.services.cache.exact_match import get_cached_response, save_to_cache
from app.services.rag.retriever import retrieve_documents, format_context
from app.services.llm.openai_client import generate_response
from app.services.rag.embedder import get_document_count

router = APIRouter()


@router.post("", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    RAG 챗봇 질의 처리

    1. Exact Match 캐시 확인
    2. 캐시 미스 시 RAG 검색 + 응답 생성
    3. 응답 캐시 저장
    """
    query = request.query.strip()

    if not query:
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    # 1. 캐시 확인
    cached = await get_cached_response(db, query)

    if cached:
        response_text, sources = cached
        return ChatResponse(
            message=ChatMessageResponse(
                id=str(uuid.uuid4()),
                role="assistant",
                content=response_text,
                sources=[ChatSource(**s) for s in sources],
                created_at=datetime.now(timezone.utc),
            ),
            cached=True,
        )

    # 2. RAG 검색
    documents = await retrieve_documents(query, top_k=5)

    # 소스 정보 추출
    sources = []
    for doc in documents:
        metadata = doc.get("metadata", {})
        sources.append({
            "title": metadata.get("title", "Unknown"),
            "url": metadata.get("url"),
            "type": metadata.get("type", "unknown"),
            "relevance_score": doc.get("score"),
        })

    # 3. 응답 생성
    if documents:
        context = format_context(documents)
        response_text = await generate_response(query, context)
    else:
        # 문서가 없는 경우
        doc_count = get_document_count()
        if doc_count == 0:
            response_text = (
                "죄송합니다. 현재 검색할 수 있는 문서가 없습니다. "
                "데이터베이스에 문서가 아직 인덱싱되지 않았습니다."
            )
        else:
            response_text = (
                "죄송합니다. 질문과 관련된 문서를 찾을 수 없습니다. "
                "다른 방식으로 질문해 주시거나, 더 구체적인 키워드를 사용해 보세요."
            )

    # 4. 캐시 저장
    await save_to_cache(db, query, response_text, sources)

    return ChatResponse(
        message=ChatMessageResponse(
            id=str(uuid.uuid4()),
            role="assistant",
            content=response_text,
            sources=[ChatSource(**s) for s in sources],
            created_at=datetime.now(timezone.utc),
        ),
        cached=False,
    )


@router.get("/stats")
async def get_chat_stats(db: AsyncSession = Depends(get_db)):
    """챗봇 통계 조회"""
    doc_count = get_document_count()

    return {
        "document_count": doc_count,
        "status": "ready" if doc_count > 0 else "no_documents",
    }
