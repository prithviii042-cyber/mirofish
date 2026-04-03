import axios from "axios";

const api = axios.create({ baseURL: "/api" });

// Dashboard
export const uploadDocument = (formData) =>
  api.post("/dashboard/upload", formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
export const getKPIs = () => api.get("/dashboard/kpis");
export const clearKPIs = () => api.delete("/dashboard/kpis");

// Scenarios
export const getScenarioHistory = () => api.get("/scenario/history");
export const getScenario = (id) => api.get(`/scenario/${id}`);
export const deleteScenario = (id) => api.delete(`/scenario/${id}`);

// Reports
export const getReportTypes = () => api.get("/report/types");
export const getReportHistory = () => api.get("/report/history");
export const getReport = (id) => api.get(`/report/${id}`);
export const deleteReport = (id) => api.delete(`/report/${id}`);

// Streaming helpers (SSE)
export function streamScenario(scenario, onChunk, onDone, onError) {
  return _postSSE("/api/scenario/run", { scenario }, onChunk, onDone, onError);
}

export function streamReport(reportType, instructions, onChunk, onDone, onError) {
  return _postSSE(
    "/api/report/generate",
    { report_type: reportType, instructions },
    onChunk,
    onDone,
    onError,
  );
}

function _postSSE(url, body, onChunk, onDone, onError) {
  const ctrl = new AbortController();

  fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
    signal: ctrl.signal,
  })
    .then(async (res) => {
      if (!res.ok) {
        const text = await res.text();
        onError?.(text);
        return;
      }
      const reader = res.body.getReader();
      const decoder = new TextDecoder();
      let buffer = "";

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split("\n");
        buffer = lines.pop() ?? "";
        for (const line of lines) {
          if (!line.startsWith("data: ")) continue;
          const payload = line.slice(6).trim();
          if (!payload) continue;
          try {
            const parsed = JSON.parse(payload);
            if (parsed.error) {
              onError?.(parsed.error);
            } else if (parsed.done) {
              onDone?.(parsed.id);
            } else if (parsed.text) {
              onChunk?.(parsed.text);
            }
          } catch {
            // ignore malformed SSE line
          }
        }
      }
    })
    .catch((err) => {
      if (err.name !== "AbortError") onError?.(err.message);
    });

  return () => ctrl.abort();
}
