from openai import AsyncOpenAI
from typing import List
from app.config import get_settings

settings = get_settings()
client = AsyncOpenAI(api_key=settings.openai_api_key)


async def get_embedding(text: str) -> List[float]:
    """텍스트의 임베딩 벡터 생성"""
    response = await client.embeddings.create(
        model=settings.openai_embedding_model,
        input=text,
    )
    return response.data[0].embedding


async def get_embeddings(texts: List[str]) -> List[List[float]]:
    """여러 텍스트의 임베딩 벡터 배치 생성"""
    response = await client.embeddings.create(
        model=settings.openai_embedding_model,
        input=texts,
    )
    return [item.embedding for item in response.data]


async def generate_response(
    query: str,
    context: str,
    system_prompt: str = None,
) -> str:
    """RAG 응답 생성"""
    if not system_prompt:
        system_prompt = """당신은 AI 분야 전문가입니다. 제공된 컨텍스트를 기반으로 사용자의 질문에 정확하고 도움이 되는 답변을 제공하세요.

규칙:
1. 컨텍스트에 있는 정보만 사용하세요.
2. 컨텍스트에 관련 정보가 없으면 솔직히 모른다고 말하세요.
3. 답변은 한국어로 작성하세요.
4. 기술적 용어는 영어로 유지하되 설명을 추가하세요.
5. 가능하면 논문이나 출처를 언급하세요."""

    messages = [
        {"role": "system", "content": system_prompt},
        {
            "role": "user",
            "content": f"""컨텍스트:
{context}

질문: {query}

위 컨텍스트를 바탕으로 질문에 답변해주세요.""",
        },
    ]

    response = await client.chat.completions.create(
        model=settings.openai_chat_model,
        messages=messages,
        temperature=0.7,
        max_tokens=1024,
    )

    return response.choices[0].message.content
