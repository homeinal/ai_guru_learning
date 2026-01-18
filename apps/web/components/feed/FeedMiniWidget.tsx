"use client";

import { useState, useEffect } from "react";
import { useSession } from "next-auth/react";
import { getFeed, getUserByGoogleId } from "@/lib/api-client";
import { formatDistanceToNow } from "@/lib/utils";
import Link from "next/link";

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

export function FeedMiniWidget() {
  const { data: session, status } = useSession();
  const [posts, setPosts] = useState<Post[]>([]);
  const [loading, setLoading] = useState(true);
  const [isCollapsed, setIsCollapsed] = useState(false);

  useEffect(() => {
    async function loadFeed() {
      try {
        setLoading(true);

        let userId: string | undefined;
        if (session?.user?.id) {
          const user = await getUserByGoogleId(session.user.id);
          if (user) {
            userId = user.id;
          }
        }

        const response = await getFeed({ userId, limit: 3, offset: 0 });
        setPosts(response.posts);
      } catch (err) {
        console.error("Feed load error:", err);
      } finally {
        setLoading(false);
      }
    }

    if (status !== "loading") {
      loadFeed();
    }
  }, [session, status]);

  if (loading) {
    return (
      <div className="bg-gray-50 rounded-lg p-3 mb-4">
        <div className="animate-pulse flex gap-2">
          <div className="h-3 bg-gray-200 rounded w-20" />
          <div className="h-3 bg-gray-200 rounded flex-1" />
        </div>
      </div>
    );
  }

  if (posts.length === 0) {
    return null;
  }

  return (
    <div className="bg-gradient-to-r from-primary-50 to-blue-50 rounded-lg border border-primary-100 mb-4 overflow-hidden">
      {/* Header */}
      <button
        onClick={() => setIsCollapsed(!isCollapsed)}
        className="w-full px-4 py-2 flex items-center justify-between hover:bg-primary-100/50 transition-colors"
      >
        <div className="flex items-center gap-2">
          <span className="text-sm font-medium text-primary-700">Guru 피드</span>
          <span className="text-xs text-primary-500 bg-primary-100 px-1.5 py-0.5 rounded">
            {posts.length}개 새 포스트
          </span>
        </div>
        <svg
          className={`w-4 h-4 text-primary-500 transition-transform ${isCollapsed ? "" : "rotate-180"}`}
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
        </svg>
      </button>

      {/* Content */}
      {!isCollapsed && (
        <div className="px-4 pb-3">
          <div className="space-y-2">
            {posts.map((post) => (
              <div
                key={post.id}
                className="bg-white rounded-lg p-3 shadow-sm border border-gray-100"
              >
                <div className="flex items-start gap-2">
                  {/* Avatar */}
                  <div className="w-8 h-8 rounded-full bg-gradient-to-br from-primary-400 to-primary-600 flex items-center justify-center text-white text-xs font-semibold flex-shrink-0">
                    {post.guru?.name?.charAt(0) || "?"}
                  </div>

                  {/* Content */}
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2 mb-1">
                      <span className="text-sm font-medium text-gray-900 truncate">
                        {post.guru?.name || "Unknown"}
                      </span>
                      <span className="text-xs text-gray-400">
                        {formatDistanceToNow(post.posted_at)}
                      </span>
                    </div>
                    <p className="text-sm text-gray-600 line-clamp-2">
                      {post.content}
                    </p>
                  </div>
                </div>
              </div>
            ))}
          </div>

          {/* Footer */}
          <Link
            href="/feed"
            className="block mt-3 text-center text-sm text-primary-600 hover:text-primary-700 font-medium"
          >
            모든 피드 보기 &rarr;
          </Link>
        </div>
      )}
    </div>
  );
}
