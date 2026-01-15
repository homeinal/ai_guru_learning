"""
RAG용 샘플 문서 시드 스크립트
사용법: python -m scripts.seed_rag
"""

import asyncio
from app.services.rag.embedder import add_documents, get_document_count
from app.db.chroma import reset_collection


# AI 관련 샘플 문서 (실제 서비스에서는 Arxiv에서 가져옴)
SAMPLE_DOCUMENTS = [
    {
        "id": "doc-transformer",
        "title": "Attention Is All You Need",
        "type": "arxiv",
        "url": "https://arxiv.org/abs/1706.03762",
        "content": """Transformer는 2017년 Google에서 발표한 혁신적인 신경망 아키텍처입니다.
        기존 RNN/LSTM의 순차적 처리 방식을 버리고, Self-Attention 메커니즘을 통해
        시퀀스 전체를 한 번에 처리합니다. 이를 통해 병렬 처리가 가능해지고,
        장거리 의존성을 더 잘 학습할 수 있게 되었습니다.

        주요 구성 요소:
        1. Multi-Head Attention: 여러 개의 attention을 병렬로 수행
        2. Position-wise Feed Forward: 각 위치별로 적용되는 완전연결층
        3. Positional Encoding: 위치 정보를 임베딩에 추가

        Transformer는 BERT, GPT, T5 등 현대 NLP 모델의 기반이 되었습니다.""",
    },
    {
        "id": "doc-gpt",
        "title": "Language Models are Few-Shot Learners (GPT-3)",
        "type": "arxiv",
        "url": "https://arxiv.org/abs/2005.14165",
        "content": """GPT-3는 OpenAI에서 개발한 1750억 파라미터 규모의 대규모 언어 모델입니다.
        Few-shot learning 능력을 보여주며, 별도의 fine-tuning 없이도
        다양한 NLP 태스크를 수행할 수 있습니다.

        주요 특징:
        1. Autoregressive 모델: 다음 토큰을 예측하는 방식으로 학습
        2. In-context Learning: 프롬프트에 예시를 제공하면 태스크 학습
        3. Emergent Abilities: 규모가 커지면서 새로운 능력이 나타남

        GPT-3는 ChatGPT, GPT-4로 이어지는 LLM 혁명의 시작점이 되었습니다.""",
    },
    {
        "id": "doc-bert",
        "title": "BERT: Pre-training of Deep Bidirectional Transformers",
        "type": "arxiv",
        "url": "https://arxiv.org/abs/1810.04805",
        "content": """BERT는 Google에서 2018년 발표한 양방향 Transformer 모델입니다.
        Masked Language Modeling(MLM)과 Next Sentence Prediction(NSP)으로 사전학습합니다.

        GPT와의 차이점:
        - GPT: 단방향 (왼쪽에서 오른쪽으로만 context 참조)
        - BERT: 양방향 (전체 context 참조)

        BERT의 혁신:
        1. 사전학습-미세조정 패러다임 정립
        2. 다양한 NLP 태스크에서 SOTA 달성
        3. 검색 엔진, 챗봇 등 실제 서비스에 널리 활용""",
    },
    {
        "id": "doc-rag",
        "title": "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks",
        "type": "arxiv",
        "url": "https://arxiv.org/abs/2005.11401",
        "content": """RAG(Retrieval-Augmented Generation)는 검색과 생성을 결합한 기술입니다.
        LLM의 hallucination 문제를 해결하고, 최신 정보를 반영할 수 있습니다.

        RAG 파이프라인:
        1. Query: 사용자 질문 입력
        2. Retrieve: 벡터 DB에서 관련 문서 검색
        3. Augment: 검색된 문서를 컨텍스트로 추가
        4. Generate: LLM이 컨텍스트 기반으로 응답 생성

        장점:
        - 최신 정보 반영 가능
        - 출처 제공으로 신뢰성 향상
        - LLM 지식의 한계 극복""",
    },
    {
        "id": "doc-diffusion",
        "title": "Denoising Diffusion Probabilistic Models",
        "type": "arxiv",
        "url": "https://arxiv.org/abs/2006.11239",
        "content": """Diffusion 모델은 이미지 생성 분야에서 GAN을 대체한 혁신적인 기술입니다.
        Stable Diffusion, DALL-E, Midjourney 등의 기반이 됩니다.

        작동 원리:
        1. Forward Process: 이미지에 점진적으로 노이즈 추가
        2. Reverse Process: 노이즈에서 원본 이미지 복원 학습

        장점:
        - GAN보다 안정적인 학습
        - 다양한 이미지 생성 가능
        - Text-to-Image에 매우 효과적""",
    },
    {
        "id": "doc-llama",
        "title": "LLaMA: Open and Efficient Foundation Language Models",
        "type": "arxiv",
        "url": "https://arxiv.org/abs/2302.13971",
        "content": """LLaMA는 Meta에서 공개한 오픈소스 대규모 언어 모델입니다.
        7B, 13B, 33B, 65B 파라미터 버전으로 제공됩니다.

        특징:
        1. 효율성: GPT-3보다 작은 규모로 비슷한 성능
        2. 오픈소스: 연구 목적으로 공개
        3. Chinchilla 스케일링: 토큰 수를 늘려 효율적 학습

        LLaMA는 오픈소스 LLM 생태계의 촉매제가 되었으며,
        Alpaca, Vicuna 등 다양한 파생 모델이 등장했습니다.""",
    },
    {
        "id": "doc-moe",
        "title": "Mixture of Experts (MoE) Architecture",
        "type": "arxiv",
        "url": "https://arxiv.org/abs/2101.03961",
        "content": """Mixture of Experts(MoE)는 조건부 계산을 통해 모델 효율성을 높이는 기술입니다.
        GPT-4, Mixtral 등 최신 모델에서 활용됩니다.

        작동 원리:
        1. 여러 개의 Expert 네트워크 준비
        2. Router가 입력에 따라 적절한 Expert 선택
        3. 선택된 Expert만 활성화되어 계산

        장점:
        - 파라미터 대비 효율적인 계산
        - 전문화된 Expert로 성능 향상
        - 스케일업에 유리""",
    },
    {
        "id": "doc-rlhf",
        "title": "Training Language Models with Human Feedback (RLHF)",
        "type": "arxiv",
        "url": "https://arxiv.org/abs/2203.02155",
        "content": """RLHF는 인간 피드백을 통해 언어 모델을 정렬하는 기술입니다.
        ChatGPT의 핵심 기술로, LLM을 유용하고 안전하게 만듭니다.

        RLHF 프로세스:
        1. SFT(Supervised Fine-Tuning): 시연 데이터로 미세조정
        2. Reward Model: 인간 선호도 학습
        3. PPO: 강화학습으로 정책 최적화

        대안 기술:
        - DPO(Direct Preference Optimization): Reward Model 없이 직접 최적화
        - RLAIF: AI 피드백 활용""",
    },
]


async def main():
    print("🚀 RAG 문서 시드 시작...")

    # 기존 컬렉션 초기화 (선택적)
    # reset_collection()

    # 문서 추가
    count = await add_documents(SAMPLE_DOCUMENTS)
    print(f"✅ {count}개 문서 추가됨")

    # 총 문서 수 확인
    total = get_document_count()
    print(f"📊 총 문서 수: {total}")


if __name__ == "__main__":
    asyncio.run(main())
