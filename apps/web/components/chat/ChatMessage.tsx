import { ChatMessage } from "@/lib/api-client";

interface ChatMessageBubbleProps {
  message: ChatMessage;
}

export function ChatMessageBubble({ message }: ChatMessageBubbleProps) {
  const isUser = message.role === "user";

  return (
    <div className={`flex ${isUser ? "justify-end" : "justify-start"}`}>
      <div
        className={`max-w-[85%] ${
          isUser
            ? "bg-primary-600 text-white rounded-2xl rounded-br-md"
            : "bg-white border border-gray-200 text-gray-800 rounded-2xl rounded-bl-md"
        } px-4 py-3 shadow-sm`}
      >
        {/* Content */}
        <div className="whitespace-pre-wrap leading-relaxed">
          {message.content}
        </div>

        {/* Sources (assistant only) */}
        {!isUser && message.sources && message.sources.length > 0 && (
          <div className="mt-3 pt-3 border-t border-gray-100">
            <div className="text-xs text-gray-500 mb-2">참고 자료:</div>
            <div className="space-y-1">
              {message.sources.map((source, index) => (
                <div
                  key={index}
                  className="flex items-center gap-2 text-xs text-gray-600"
                >
                  <span
                    className={`px-1.5 py-0.5 rounded text-[10px] font-medium ${
                      source.type === "arxiv"
                        ? "bg-red-100 text-red-700"
                        : source.type === "huggingface"
                        ? "bg-yellow-100 text-yellow-700"
                        : "bg-gray-100 text-gray-600"
                    }`}
                  >
                    {source.type}
                  </span>
                  {source.url ? (
                    <a
                      href={source.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="hover:text-primary-600 truncate"
                    >
                      {source.title}
                    </a>
                  ) : (
                    <span className="truncate">{source.title}</span>
                  )}
                  {source.relevance_score && (
                    <span className="text-gray-400">
                      ({Math.round(source.relevance_score * 100)}%)
                    </span>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
