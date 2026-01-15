"""
샘플 데이터 시드 스크립트
사용법: python -m scripts.seed_data
"""

import asyncio
from datetime import datetime, timedelta, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.neon import async_session_maker, init_db
from app.models.db_models import Guru, GuruPost


# AI Guru 샘플 데이터
GURUS = [
    {
        "id": "guru-andrew-ng",
        "name": "Andrew Ng",
        "threads_handle": "andrewng",
        "bio": "DeepLearning.AI 창립자, Coursera 공동창립자. AI 교육과 연구의 선구자.",
        "avatar_url": None,
    },
    {
        "id": "guru-yann-lecun",
        "name": "Yann LeCun",
        "threads_handle": "ylecun",
        "bio": "Meta Chief AI Scientist. 딥러닝의 아버지 중 한 명, CNN 개발자.",
        "avatar_url": None,
    },
    {
        "id": "guru-andrej-karpathy",
        "name": "Andrej Karpathy",
        "threads_handle": "karpathy",
        "bio": "전 Tesla AI Director, OpenAI 공동창립. AI 교육 유튜버.",
        "avatar_url": None,
    },
    {
        "id": "guru-jim-fan",
        "name": "Jim Fan",
        "threads_handle": "drjimfan",
        "bio": "NVIDIA Senior Research Scientist. Embodied AI, Foundation Models 연구.",
        "avatar_url": None,
    },
    {
        "id": "guru-fei-fei-li",
        "name": "Fei-Fei Li",
        "threads_handle": "drfeifei",
        "bio": "Stanford HAI 공동디렉터. ImageNet 창시자, Computer Vision 선구자.",
        "avatar_url": None,
    },
    {
        "id": "guru-demis-hassabis",
        "name": "Demis Hassabis",
        "threads_handle": "demaboroboais",
        "bio": "Google DeepMind CEO. AlphaGo, AlphaFold 개발 주도.",
        "avatar_url": None,
    },
]

# 샘플 포스트 데이터
SAMPLE_POSTS = [
    # Andrew Ng
    {
        "guru_id": "guru-andrew-ng",
        "content": "AI를 배우는 가장 좋은 방법은 직접 프로젝트를 만들어보는 것입니다. 이론만 공부하지 말고, 작은 것부터 시작해서 실제로 구현해보세요. 실패해도 괜찮습니다. 그 과정에서 배우는 것이 가장 중요합니다.",
        "posted_at": datetime.now(timezone.utc) - timedelta(hours=2),
    },
    {
        "guru_id": "guru-andrew-ng",
        "content": "LLM 시대에 프롬프트 엔지니어링은 새로운 프로그래밍 스킬입니다. 좋은 프롬프트를 작성하는 능력이 AI 활용 능력을 결정짓습니다.",
        "posted_at": datetime.now(timezone.utc) - timedelta(days=1),
    },
    # Yann LeCun
    {
        "guru_id": "guru-yann-lecun",
        "content": "현재 LLM은 실제로 '이해'하지 않습니다. 패턴 매칭을 매우 잘 할 뿐입니다. AGI로 가려면 world model이 필요합니다. Self-supervised learning이 그 열쇠가 될 것입니다.",
        "posted_at": datetime.now(timezone.utc) - timedelta(hours=5),
    },
    {
        "guru_id": "guru-yann-lecun",
        "content": "Autoregressive LLM의 한계: 한 번 실수하면 복구가 어렵습니다. 인간은 계획하고, 수정하고, 되돌아갑니다. 미래의 AI 시스템은 이런 능력이 필요합니다.",
        "posted_at": datetime.now(timezone.utc) - timedelta(days=2),
    },
    # Andrej Karpathy
    {
        "guru_id": "guru-andrej-karpathy",
        "content": "소프트웨어 2.0: 더 이상 규칙을 직접 코딩하지 않습니다. 대신 데이터와 신경망 아키텍처를 설계하고, 학습이 프로그램을 작성합니다. 이것이 새로운 프로그래밍 패러다임입니다.",
        "posted_at": datetime.now(timezone.utc) - timedelta(hours=8),
    },
    {
        "guru_id": "guru-andrej-karpathy",
        "content": "GPT 같은 모델을 처음부터 구현해보세요. 논문만 읽는 것과 직접 구현하는 것은 완전히 다른 경험입니다. 진정한 이해는 구현에서 옵니다.",
        "posted_at": datetime.now(timezone.utc) - timedelta(days=1, hours=12),
    },
    # Jim Fan
    {
        "guru_id": "guru-jim-fan",
        "content": "Foundation Models + Robotics = 새로운 가능성. 언어로 로봇을 제어하는 시대가 오고 있습니다. Generalist agent의 시대가 열리고 있습니다.",
        "posted_at": datetime.now(timezone.utc) - timedelta(hours=3),
    },
    {
        "guru_id": "guru-jim-fan",
        "content": "Minecraft에서 학습한 AI가 실제 세계의 로봇을 제어할 수 있을까요? 놀랍게도, 시뮬레이션에서 학습한 정책이 실제 세계로 transfer되고 있습니다.",
        "posted_at": datetime.now(timezone.utc) - timedelta(days=3),
    },
    # Fei-Fei Li
    {
        "guru_id": "guru-fei-fei-li",
        "content": "AI는 도구입니다. 인간을 대체하는 것이 아니라 인간의 능력을 확장하는 것입니다. Human-centered AI를 설계해야 합니다.",
        "posted_at": datetime.now(timezone.utc) - timedelta(hours=10),
    },
    # Demis Hassabis
    {
        "guru_id": "guru-demis-hassabis",
        "content": "AlphaFold가 증명했듯이, AI는 과학 연구를 가속화할 수 있습니다. 다음 목표는 신약 개발, 재료 과학, 그리고 에너지 문제 해결입니다.",
        "posted_at": datetime.now(timezone.utc) - timedelta(days=1, hours=6),
    },
]


async def seed_gurus(session: AsyncSession):
    """Guru 시드 데이터 삽입"""
    for guru_data in GURUS:
        guru = Guru(**guru_data)
        session.add(guru)
    await session.flush()
    print(f"✅ {len(GURUS)}명의 Guru 추가됨")


async def seed_posts(session: AsyncSession):
    """포스트 시드 데이터 삽입"""
    for post_data in SAMPLE_POSTS:
        post = GuruPost(**post_data)
        session.add(post)
    await session.flush()
    print(f"✅ {len(SAMPLE_POSTS)}개의 포스트 추가됨")


async def main():
    print("🚀 시드 데이터 삽입 시작...")

    # DB 초기화
    await init_db()

    async with async_session_maker() as session:
        try:
            await seed_gurus(session)
            await seed_posts(session)
            await session.commit()
            print("✅ 시드 데이터 삽입 완료!")
        except Exception as e:
            await session.rollback()
            print(f"❌ 에러 발생: {e}")
            raise


if __name__ == "__main__":
    asyncio.run(main())
