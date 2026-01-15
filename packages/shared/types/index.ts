// Guru 관련 타입
export interface Guru {
  id: string;
  name: string;
  threadsHandle: string;
  avatarUrl?: string;
  bio?: string;
  createdAt: string;
}

// Guru 포스트 타입
export interface GuruPost {
  id: string;
  guruId: string;
  guru?: Guru;
  content: string;
  threadsUrl?: string;
  postedAt: string;
  createdAt: string;
}

// 사용자 타입
export interface User {
  id: string;
  email: string;
  name?: string;
  avatarUrl?: string;
  googleId: string;
  createdAt: string;
}

// 챗봇 관련 타입
export interface ChatMessage {
  id: string;
  role: "user" | "assistant";
  content: string;
  sources?: ChatSource[];
  createdAt: string;
}

export interface ChatSource {
  title: string;
  url?: string;
  type: "arxiv" | "huggingface" | "cache";
  relevanceScore?: number;
}

export interface ChatRequest {
  query: string;
  userId?: string;
}

export interface ChatResponse {
  message: ChatMessage;
  cached: boolean;
}

// API 응답 래퍼
export interface ApiResponse<T> {
  data?: T;
  error?: string;
  message?: string;
}

// 피드 요청/응답
export interface FeedRequest {
  userId?: string;
  guruIds?: string[];
  limit?: number;
  offset?: number;
}

export interface FeedResponse {
  posts: GuruPost[];
  total: number;
  hasMore: boolean;
}
