const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

interface FetchOptions extends RequestInit {
  timeout?: number;
}

async function fetchWithTimeout(
  url: string,
  options: FetchOptions = {}
): Promise<Response> {
  const { timeout = 30000, ...fetchOptions } = options;

  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), timeout);

  try {
    const response = await fetch(url, {
      ...fetchOptions,
      signal: controller.signal,
    });
    return response;
  } finally {
    clearTimeout(timeoutId);
  }
}

// Guru API
export async function getGurus() {
  const response = await fetchWithTimeout(`${API_URL}/api/feed/gurus`);
  if (!response.ok) throw new Error("Failed to fetch gurus");
  return response.json();
}

export async function getUserGurus(userId: string) {
  const response = await fetchWithTimeout(`${API_URL}/api/users/${userId}/gurus`);
  if (!response.ok) throw new Error("Failed to fetch user gurus");
  return response.json();
}

export async function updateUserGurus(userId: string, guruIds: string[]) {
  const response = await fetchWithTimeout(`${API_URL}/api/users/${userId}/gurus`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ guru_ids: guruIds }),
  });
  if (!response.ok) throw new Error("Failed to update user gurus");
  return response.json();
}

// Feed API
export async function getFeed(params: {
  userId?: string;
  guruIds?: string[];
  limit?: number;
  offset?: number;
}) {
  const searchParams = new URLSearchParams();

  if (params.userId) searchParams.set("user_id", params.userId);
  if (params.guruIds?.length) searchParams.set("guru_ids", params.guruIds.join(","));
  if (params.limit) searchParams.set("limit", params.limit.toString());
  if (params.offset) searchParams.set("offset", params.offset.toString());

  const url = `${API_URL}/api/feed?${searchParams.toString()}`;
  const response = await fetchWithTimeout(url);

  if (!response.ok) throw new Error("Failed to fetch feed");
  return response.json();
}

// Chat API
export interface ChatMessage {
  id: string;
  role: "user" | "assistant";
  content: string;
  sources?: {
    title: string;
    url?: string;
    type: string;
    relevance_score?: number;
  }[];
  created_at: string;
}

export interface ChatResponse {
  message: ChatMessage;
  cached: boolean;
}

export async function sendChatMessage(
  query: string,
  userId?: string
): Promise<ChatResponse> {
  const response = await fetchWithTimeout(`${API_URL}/api/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query, user_id: userId }),
    timeout: 60000, // 챗봇은 더 긴 타임아웃
  });

  if (!response.ok) throw new Error("Failed to send message");
  return response.json();
}

export async function getChatStats() {
  const response = await fetchWithTimeout(`${API_URL}/api/chat/stats`);
  if (!response.ok) throw new Error("Failed to fetch chat stats");
  return response.json();
}

// User API
export async function getUserByGoogleId(googleId: string) {
  const response = await fetchWithTimeout(`${API_URL}/api/users/by-google/${googleId}`);
  if (!response.ok) {
    if (response.status === 404) return null;
    throw new Error("Failed to fetch user");
  }
  return response.json();
}
