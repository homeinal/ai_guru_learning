# AI Learning Tracker

AI Guru들의 인사이트와 최신 AI 트렌드를 한눈에 파악할 수 있는 웹 서비스입니다.

## 주요 기능

- **Guru 피드**: Andrew Ng, Yann LeCun 등 AI 리더들의 Threads 포스트 피드
- **RAG 챗봇**: Arxiv 논문 기반 AI 트렌드 Q&A
- **Google OAuth**: 로그인하여 관심 Guru 저장

## 기술 스택

| 영역 | 기술 |
|------|------|
| Frontend | Next.js 14 (App Router) |
| Backend | FastAPI |
| Database | Neon (PostgreSQL) |
| Vector DB | ChromaDB |
| LLM | OpenAI API |
| 인증 | NextAuth.js (Google OAuth) |
| 배포 | Vercel (Frontend) + Render (Backend) |

## 프로젝트 구조

```
ai-learning-tracker/
├── apps/
│   ├── web/          # Next.js 프론트엔드
│   └── api/          # FastAPI 백엔드
├── packages/
│   └── shared/       # 공유 타입
├── workers/          # 배치 작업 (Phase 2+)
└── mcp/              # MCP 서버 연동 (Phase 2+)
```

## 로컬 개발 환경 설정

### 1. 사전 요구사항

- Node.js 20+
- Python 3.11+
- pnpm

### 2. 환경 변수 설정

```bash
# 루트 디렉토리
cp .env.example .env

# Frontend
cp apps/web/.env.example apps/web/.env.local

# Backend
cp apps/api/.env.example apps/api/.env
```

각 `.env` 파일에 실제 값을 입력하세요:
- **Google OAuth**: [Google Cloud Console](https://console.cloud.google.com/)에서 발급
- **OpenAI API Key**: [OpenAI Platform](https://platform.openai.com/)에서 발급
- **Neon PostgreSQL**: [Neon](https://neon.tech/)에서 생성

### 3. 의존성 설치

```bash
# Frontend
cd apps/web
pnpm install

# Backend
cd apps/api
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 4. 데이터베이스 초기화 및 시드

```bash
cd apps/api

# 테이블 생성 및 Guru 시드 데이터
python -m scripts.seed_data

# RAG 문서 시드 (선택)
python -m scripts.seed_rag
```

### 5. 개발 서버 실행

```bash
# Backend (터미널 1)
cd apps/api
uvicorn app.main:app --reload --port 8000

# Frontend (터미널 2)
cd apps/web
pnpm dev
```

- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Docker로 실행 (대안)

```bash
docker-compose up --build
```

## 배포

### Frontend (Vercel)

1. Vercel에 GitHub 리포지토리 연결
2. Root Directory: `apps/web`
3. 환경 변수 설정

### Backend (Render)

1. Render에 GitHub 리포지토리 연결
2. `apps/api/render.yaml` 사용
3. 환경 변수 설정
4. ChromaDB용 Disk 연결

## Phase별 구현 현황

- [x] **Phase 1**: MVP (RAG 챗봇, Guru 피드, OAuth, 캐시)
- [ ] **Phase 2**: LLM Router + MCP 연동
- [ ] **Phase 3**: Analytics 대시보드
- [ ] **Phase 4**: 셀프 러닝 루프

## 라이선스

MIT
