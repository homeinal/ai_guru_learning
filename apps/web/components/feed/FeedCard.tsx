import Image from "next/image";
import { formatDistanceToNow } from "@/lib/utils";

interface Guru {
  id: string;
  name: string;
  threads_handle: string;
  avatar_url?: string;
}

interface Post {
  id: string;
  guru_id: string;
  content: string;
  threads_url?: string;
  posted_at: string;
  guru?: Guru;
}

interface FeedCardProps {
  post: Post;
}

export function FeedCard({ post }: FeedCardProps) {
  const guru = post.guru;

  return (
    <article className="bg-white rounded-xl shadow-sm border border-gray-100 p-5 hover:shadow-md transition-shadow">
      {/* Header */}
      <div className="flex items-center gap-3 mb-3">
        {guru?.avatar_url ? (
          <Image
            src={guru.avatar_url}
            alt={guru.name}
            width={40}
            height={40}
            className="rounded-full"
          />
        ) : (
          <div className="w-10 h-10 rounded-full bg-gradient-to-br from-primary-400 to-primary-600 flex items-center justify-center text-white font-semibold">
            {guru?.name?.charAt(0) || "?"}
          </div>
        )}

        <div className="flex-1">
          <div className="font-semibold text-gray-900">
            {guru?.name || "Unknown Guru"}
          </div>
          <div className="text-sm text-gray-500">
            @{guru?.threads_handle || "unknown"}
          </div>
        </div>

        <div className="text-xs text-gray-400">
          {formatDistanceToNow(post.posted_at)}
        </div>
      </div>

      {/* Content */}
      <div className="text-gray-800 whitespace-pre-wrap leading-relaxed">
        {post.content}
      </div>

      {/* Footer */}
      {post.threads_url && (
        <div className="mt-4 pt-3 border-t border-gray-100">
          <a
            href={post.threads_url}
            target="_blank"
            rel="noopener noreferrer"
            className="text-sm text-primary-600 hover:text-primary-700 flex items-center gap-1"
          >
            <span>Threads에서 보기</span>
            <svg
              className="w-4 h-4"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"
              />
            </svg>
          </a>
        </div>
      )}
    </article>
  );
}
