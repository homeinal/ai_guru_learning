from typing import List, Dict, Any
from app.db.chroma import get_collection
from app.services.llm.openai_client import get_embeddings
import uuid


async def add_documents(
    documents: List[Dict[str, Any]],
    batch_size: int = 100,
) -> int:
    """
    문서들을 ChromaDB에 추가

    Args:
        documents: 문서 리스트, 각 문서는 다음을 포함:
            - content: 문서 내용 (필수)
            - title: 제목
            - url: 출처 URL
            - type: 문서 유형 (arxiv, huggingface 등)

    Returns:
        추가된 문서 수
    """
    collection = get_collection()
    added_count = 0

    # 배치 처리
    for i in range(0, len(documents), batch_size):
        batch = documents[i : i + batch_size]

        ids = []
        contents = []
        metadatas = []

        for doc in batch:
            doc_id = doc.get("id") or str(uuid.uuid4())
            ids.append(doc_id)
            contents.append(doc["content"])
            metadatas.append({
                "title": doc.get("title", ""),
                "url": doc.get("url", ""),
                "type": doc.get("type", "unknown"),
            })

        # 임베딩 생성
        embeddings = await get_embeddings(contents)

        # ChromaDB에 추가
        collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=contents,
            metadatas=metadatas,
        )

        added_count += len(batch)

    return added_count


async def update_document(
    doc_id: str,
    content: str,
    metadata: Dict[str, Any] = None,
) -> bool:
    """문서 업데이트"""
    collection = get_collection()

    # 임베딩 생성
    embeddings = await get_embeddings([content])

    collection.update(
        ids=[doc_id],
        embeddings=embeddings,
        documents=[content],
        metadatas=[metadata] if metadata else None,
    )

    return True


def delete_document(doc_id: str) -> bool:
    """문서 삭제"""
    collection = get_collection()
    collection.delete(ids=[doc_id])
    return True


def get_document_count() -> int:
    """현재 저장된 문서 수"""
    collection = get_collection()
    return collection.count()
