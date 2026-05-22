import axios from 'axios';

function getApiBaseUrl() {
  const configured = process.env.NEXT_PUBLIC_API_URL;
  if (configured !== undefined) {
    return configured;
  }

  if (typeof window !== "undefined") {
    const { hostname, origin } = window.location;
    if (hostname === "localhost" || hostname === "127.0.0.1") {
      return "http://localhost:8000";
    }
    return origin;
  }

  return "http://localhost:8000";
}

export async function analyzeText(text: string, language: string) {
  try {
    const response = await axios.post(`${getApiBaseUrl()}/analyze`, { text, language });
    return response.data;
  } catch (error: unknown) {
    if (axios.isAxiosError(error)) {
      throw new Error(error.response?.data?.error || error.message || "Failed to analyze text");
    }
    throw new Error("An unexpected error occurred");
  }
}

export async function rewriteText(text: string, language: string, benchmarkText: string, benchmarkId: string) {
  try {
    const response = await axios.post(`${getApiBaseUrl()}/rewrite`, { 
      text, 
      language, 
      benchmark_text: benchmarkText, 
      benchmark_id: benchmarkId
    });
    return response.data;
  } catch (error: unknown) {
    if (axios.isAxiosError(error)) {
      throw new Error(error.response?.data?.error || error.message || "Failed to rewrite text");
    }
    throw new Error("An unexpected error occurred");
  }
}
