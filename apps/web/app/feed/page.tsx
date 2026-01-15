"use client";

import { useSession } from "next-auth/react";
import { useEffect, useState } from "react";
import { getFeed, getGurus, getUserByGoogleId } from "@/lib/api-client";
import { FeedCard } from "@/components/feed/FeedCard";
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

export default function FeedPage() {
  const { data: session, status } = useSession();
  const [posts, setPosts] = useState<Post[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [hasMore, setHasMore] = useState(false);
  const [offset, setOffset] = useState(0);

  useEffect(() => {
    async function loadFeed() {
      try {
        setLoading(true);

        let userId: string | undefined;

        // 로그인한 경우 사용자의 팔로우 Guru 기반 피드
        if (session?.user?.id) {
          const user = await getUserByGoogleId(session.user.id);
          if (user) {
            userId = user.id;
          }
        }

        const response = await getFeed({ userId, limit: 20, offset: 0 });
        setPosts(response.posts);
        setHasMore(response.has_more);
        setOffset(response.posts.length);
      } catch (err) {
        setError("피드를 불러오는데 실패했습니다.");
        console.error(err);
      } finally {
        setLoading(false);
      }
    }

    if (status !== "loading") {
      loadFeed();
    }
  }, [session, status]);

  const loadMore = async () => {
    try {
      let userId: string | undefined;
      if (session?.user?.id) {
        const user = await getUserByGoogleId(session.user.id);
        if (user) userId = user.id;
      }

      const response = await getFeed({ userId, limit: 20, offset });
      setPosts((prev) => [...prev, ...response.posts]);
      setHasMore(response.has_more);
      setOffset((prev) => prev + response.posts.length);
    } catch (err) {
      console.error(err);
    }
  };

  if (status === "loading" || loading) {
    return (
      <div className="max-w-2xl mx-auto px-4 py-8">
        <div className="animate-pulse space-y-4">
          {[1, 2, 3].map((i) => (
            <div key={i} className="bg-gray-200 h-40 rounded-xl" />
          ))}
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="max-w-2xl mx-auto px-4 py-8">
        <div className="bg-red-50 text-red-600 p-4 rounded-xl">{error}</div>
      </div>
    );
  }

  return (
    <div className="max-w-2xl mx-auto px-4 py-8">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold text-gray-900">Guru 피드</h1>
        {session && (
          <Link
            href="/settings"
            className="text-sm text-primary-600 hover:text-primary-700"
          >
            Guru 설정
          </Link>
        )}
      </div>

      {posts.length === 0 ? (
        <div className="bg-gray-50 rounded-xl p-8 text-center">
          <p className="text-gray-500 mb-4">
            {session
              ? "팔로우하는 Guru가 없거나 포스트가 없습니다."
              : "표시할 포스트가 없습니다."}
          </p>
          {session && (
            <Link
              href="/settings"
              className="inline-block px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700"
            >
              Guru 팔로우하기
            </Link>
          )}
        </div>
      ) : (
        <>
          <div className="space-y-4">
            {posts.map((post) => (
              <FeedCard key={post.id} post={post} />
            ))}
          </div>

          {hasMore && (
            <div className="mt-6 text-center">
              <button
                onClick={loadMore}
                className="px-6 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200"
              >
                더 보기
              </button>
            </div>
          )}
        </>
      )}
    </div>
  );
}
