"use client";

import { useSession } from "next-auth/react";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import {
  getGurus,
  getUserGurus,
  updateUserGurus,
  getUserByGoogleId,
} from "@/lib/api-client";
import Image from "next/image";

interface Guru {
  id: string;
  name: string;
  threads_handle: string;
  avatar_url?: string;
  bio?: string;
}

export default function SettingsPage() {
  const { data: session, status } = useSession();
  const router = useRouter();
  const [allGurus, setAllGurus] = useState<Guru[]>([]);
  const [followedIds, setFollowedIds] = useState<Set<string>>(new Set());
  const [userId, setUserId] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState<string | null>(null);

  useEffect(() => {
    if (status === "unauthenticated") {
      router.push("/login?callbackUrl=/settings");
    }
  }, [status, router]);

  useEffect(() => {
    async function loadData() {
      if (!session?.user?.id) return;

      try {
        setLoading(true);

        // 모든 Guru 조회
        const gurus = await getGurus();
        setAllGurus(gurus);

        // 사용자 정보 조회
        const user = await getUserByGoogleId(session.user.id);
        if (user) {
          setUserId(user.id);

          // 사용자가 팔로우하는 Guru 조회
          const followed = await getUserGurus(user.id);
          setFollowedIds(new Set(followed.map((g: Guru) => g.id)));
        }
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    }

    if (status === "authenticated") {
      loadData();
    }
  }, [session, status]);

  const toggleGuru = (guruId: string) => {
    setFollowedIds((prev) => {
      const next = new Set(prev);
      if (next.has(guruId)) {
        next.delete(guruId);
      } else {
        next.add(guruId);
      }
      return next;
    });
  };

  const saveChanges = async () => {
    if (!userId) return;

    try {
      setSaving(true);
      await updateUserGurus(userId, Array.from(followedIds));
      setMessage("설정이 저장되었습니다!");
      setTimeout(() => setMessage(null), 3000);
    } catch (err) {
      setMessage("저장에 실패했습니다.");
      console.error(err);
    } finally {
      setSaving(false);
    }
  };

  if (status === "loading" || loading) {
    return (
      <div className="max-w-2xl mx-auto px-4 py-8">
        <div className="animate-pulse">
          <div className="h-8 bg-gray-200 rounded w-1/3 mb-6" />
          <div className="grid grid-cols-2 gap-4">
            {[1, 2, 3, 4].map((i) => (
              <div key={i} className="h-24 bg-gray-200 rounded-xl" />
            ))}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-2xl mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold text-gray-900 mb-2">Guru 설정</h1>
      <p className="text-gray-500 mb-6">
        팔로우할 AI Guru를 선택하세요. 선택한 Guru의 포스트가 피드에 표시됩니다.
      </p>

      {message && (
        <div
          className={`mb-4 p-3 rounded-lg text-sm ${
            message.includes("실패")
              ? "bg-red-50 text-red-600"
              : "bg-green-50 text-green-600"
          }`}
        >
          {message}
        </div>
      )}

      {allGurus.length === 0 ? (
        <div className="bg-gray-50 rounded-xl p-8 text-center">
          <p className="text-gray-500">등록된 Guru가 없습니다.</p>
        </div>
      ) : (
        <>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-6">
            {allGurus.map((guru) => {
              const isFollowed = followedIds.has(guru.id);
              return (
                <button
                  key={guru.id}
                  onClick={() => toggleGuru(guru.id)}
                  className={`p-4 rounded-xl border-2 transition-all text-left ${
                    isFollowed
                      ? "border-primary-500 bg-primary-50"
                      : "border-gray-200 bg-white hover:border-gray-300"
                  }`}
                >
                  <div className="flex items-center gap-3">
                    {guru.avatar_url ? (
                      <Image
                        src={guru.avatar_url}
                        alt={guru.name}
                        width={48}
                        height={48}
                        className="rounded-full"
                      />
                    ) : (
                      <div className="w-12 h-12 rounded-full bg-gradient-to-br from-primary-400 to-primary-600 flex items-center justify-center text-white font-semibold text-lg">
                        {guru.name.charAt(0)}
                      </div>
                    )}
                    <div className="flex-1 min-w-0">
                      <div className="font-semibold text-gray-900">
                        {guru.name}
                      </div>
                      <div className="text-sm text-gray-500 truncate">
                        @{guru.threads_handle}
                      </div>
                    </div>
                    <div
                      className={`w-6 h-6 rounded-full border-2 flex items-center justify-center ${
                        isFollowed
                          ? "border-primary-500 bg-primary-500"
                          : "border-gray-300"
                      }`}
                    >
                      {isFollowed && (
                        <svg
                          className="w-4 h-4 text-white"
                          fill="none"
                          stroke="currentColor"
                          viewBox="0 0 24 24"
                        >
                          <path
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            strokeWidth={2}
                            d="M5 13l4 4L19 7"
                          />
                        </svg>
                      )}
                    </div>
                  </div>
                  {guru.bio && (
                    <p className="mt-2 text-sm text-gray-600 line-clamp-2">
                      {guru.bio}
                    </p>
                  )}
                </button>
              );
            })}
          </div>

          <div className="flex justify-end">
            <button
              onClick={saveChanges}
              disabled={saving}
              className="px-6 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:bg-gray-300 transition-colors"
            >
              {saving ? "저장 중..." : "저장"}
            </button>
          </div>
        </>
      )}
    </div>
  );
}
