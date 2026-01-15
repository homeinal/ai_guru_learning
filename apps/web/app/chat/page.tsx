"use client";

import { useState, useRef, useEffect } from "react";
import { useSession } from "next-auth/react";
import { sendChatMessage, ChatMessage, getChatStats } from "@/lib/api-client";
import { ChatInput } from "@/components/chat/ChatInput";
import { ChatMessageBubble } from "@/components/chat/ChatMessage";

export default function ChatPage() {
  const { data: session } = useSession();
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [stats, setStats] = useState<{ document_count: number } | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    getChatStats()
      .then(setStats)
      .catch(() => setStats({ document_count: 0 }));
  }, []);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSendMessage = async (query: string) => {
    if (!query.trim() || isLoading) return;

    // 사용자 메시지 추가
    const userMessage: ChatMessage = {
      id: Date.now().toString(),
      role: "user",
      content: query,
      created_at: new Date().toISOString(),
    };
    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);
    setError(null);

    try {
      const response = await sendChatMessage(query, session?.user?.id);
      setMessages((prev) => [...prev, response.message]);
    } catch (err) {
      setError("메시지 전송에 실패했습니다. 다시 시도해주세요.");
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-[calc(100vh-64px)]">
      {/* Header */}
      <div className="border-b border-gray-200 bg-white px-4 py-3">
        <div className="max-w-3xl mx-auto flex justify-between items-center">
          <div>
            <h1 className="text-lg font-semibold text-gray-900">RAG 챗봇</h1>
            <p className="text-sm text-gray-500">
              Arxiv 논문 기반 AI 트렌드 Q&A
            </p>
          </div>
          {stats && (
            <div className="text-xs text-gray-400">
              {stats.document_count > 0
                ? `${stats.document_count}개 문서 인덱싱됨`
                : "문서 준비 중..."}
            </div>
          )}
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto px-4 py-6">
        <div className="max-w-3xl mx-auto space-y-6">
          {messages.length === 0 ? (
            <div className="text-center py-12">
              <div className="text-4xl mb-4">💬</div>
              <h2 className="text-xl font-semibold text-gray-900 mb-2">
                AI 트렌드에 대해 물어보세요
              </h2>
              <p className="text-gray-500 mb-6">
                Arxiv 논문을 기반으로 최신 AI 연구 동향을 알려드립니다
              </p>
              <div className="flex flex-wrap justify-center gap-2">
                {[
                  "Transformer 아키텍처란?",
                  "최신 LLM 트렌드",
                  "RAG 시스템 설명해줘",
                  "Attention mechanism이 뭐야?",
                ].map((suggestion) => (
                  <button
                    key={suggestion}
                    onClick={() => handleSendMessage(suggestion)}
                    className="px-3 py-1.5 text-sm bg-gray-100 text-gray-700 rounded-full hover:bg-gray-200 transition-colors"
                  >
                    {suggestion}
                  </button>
                ))}
              </div>
            </div>
          ) : (
            messages.map((message) => (
              <ChatMessageBubble key={message.id} message={message} />
            ))
          )}

          {isLoading && (
            <div className="flex items-center gap-2 text-gray-500">
              <div className="flex gap-1">
                <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" />
                <span
                  className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"
                  style={{ animationDelay: "0.2s" }}
                />
                <span
                  className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"
                  style={{ animationDelay: "0.4s" }}
                />
              </div>
              <span className="text-sm">답변 생성 중...</span>
            </div>
          )}

          {error && (
            <div className="bg-red-50 text-red-600 p-3 rounded-lg text-sm">
              {error}
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>
      </div>

      {/* Input */}
      <div className="border-t border-gray-200 bg-white px-4 py-4">
        <div className="max-w-3xl mx-auto">
          <ChatInput onSend={handleSendMessage} disabled={isLoading} />
        </div>
      </div>
    </div>
  );
}
