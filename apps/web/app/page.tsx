import Link from "next/link";

export default function HomePage() {
  return (
    <div className="flex flex-col items-center justify-center min-h-[calc(100vh-64px)] px-4">
      <div className="max-w-2xl text-center">
        <h1 className="text-4xl font-bold text-gray-900 mb-4">
          AI Learning Tracker
        </h1>
        <p className="text-xl text-gray-600 mb-8">
          AI Guru들의 인사이트와 최신 AI 트렌드를 한눈에 파악하세요
        </p>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-8">
          <Link
            href="/feed"
            className="p-6 bg-white rounded-xl shadow-md hover:shadow-lg transition-shadow border border-gray-100"
          >
            <div className="text-2xl mb-2">📡</div>
            <h2 className="text-lg font-semibold text-gray-900 mb-1">
              Guru 피드
            </h2>
            <p className="text-sm text-gray-500">
              Andrew Ng, Yann LeCun 등 AI 리더들의 최신 글
            </p>
          </Link>

          <Link
            href="/chat"
            className="p-6 bg-white rounded-xl shadow-md hover:shadow-lg transition-shadow border border-gray-100"
          >
            <div className="text-2xl mb-2">💬</div>
            <h2 className="text-lg font-semibold text-gray-900 mb-1">
              RAG 챗봇
            </h2>
            <p className="text-sm text-gray-500">
              Arxiv 논문 기반 AI 트렌드 Q&A
            </p>
          </Link>
        </div>

        <p className="text-sm text-gray-400">
          Google 계정으로 로그인하여 관심 Guru를 설정하세요
        </p>
      </div>
    </div>
  );
}
