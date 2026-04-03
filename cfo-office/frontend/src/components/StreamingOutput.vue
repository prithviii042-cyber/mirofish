<template>
  <div class="streaming-output">
    <div v-if="streaming" class="streaming-indicator">
      <span class="dot"></span>
      <span class="dot"></span>
      <span class="dot"></span>
      <span class="label">Claude is analyzing…</span>
    </div>
    <div v-if="content" class="markdown-body" v-html="renderedContent"></div>
    <div v-if="!content && !streaming" class="empty-state">
      <slot name="empty">No output yet.</slot>
    </div>
  </div>
</template>

<script setup>
import { computed } from "vue";
import { marked } from "marked";

const props = defineProps({
  content: { type: String, default: "" },
  streaming: { type: Boolean, default: false },
});

const renderedContent = computed(() => {
  if (!props.content) return "";
  return marked.parse(props.content, { gfm: true, breaks: true });
});
</script>

<style scoped>
.streaming-output { width: 100%; }
.streaming-indicator {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  margin-bottom: 1rem;
  color: var(--accent);
  font-size: 0.85rem;
  font-weight: 500;
}
.dot {
  width: 7px; height: 7px;
  border-radius: 50%;
  background: var(--accent);
  animation: bounce 1.2s infinite ease-in-out;
}
.dot:nth-child(2) { animation-delay: 0.2s; }
.dot:nth-child(3) { animation-delay: 0.4s; }
@keyframes bounce {
  0%, 80%, 100% { transform: scale(0.6); opacity: 0.4; }
  40% { transform: scale(1); opacity: 1; }
}
.markdown-body {
  line-height: 1.7;
  color: var(--text-primary);
  font-size: 0.95rem;
}
.markdown-body :deep(h1),
.markdown-body :deep(h2),
.markdown-body :deep(h3),
.markdown-body :deep(h4) {
  color: var(--text-primary);
  margin: 1.5rem 0 0.5rem;
  font-weight: 700;
}
.markdown-body :deep(h1) { font-size: 1.5rem; border-bottom: 1px solid var(--border); padding-bottom: 0.5rem; }
.markdown-body :deep(h2) { font-size: 1.2rem; }
.markdown-body :deep(h3) { font-size: 1rem; color: var(--accent); }
.markdown-body :deep(table) {
  width: 100%;
  border-collapse: collapse;
  margin: 1rem 0;
  font-size: 0.88rem;
}
.markdown-body :deep(th) {
  background: var(--surface-hover);
  padding: 0.6rem 1rem;
  text-align: left;
  font-weight: 600;
  color: var(--text-secondary);
  border-bottom: 2px solid var(--border);
}
.markdown-body :deep(td) {
  padding: 0.55rem 1rem;
  border-bottom: 1px solid var(--border);
}
.markdown-body :deep(tr:hover td) { background: var(--surface-hover); }
.markdown-body :deep(strong) { color: var(--text-primary); font-weight: 700; }
.markdown-body :deep(ul), .markdown-body :deep(ol) { padding-left: 1.5rem; margin: 0.5rem 0; }
.markdown-body :deep(li) { margin: 0.25rem 0; }
.markdown-body :deep(blockquote) {
  border-left: 3px solid var(--accent);
  padding-left: 1rem;
  margin: 1rem 0;
  color: var(--text-secondary);
}
.markdown-body :deep(code) {
  background: var(--surface-hover);
  padding: 0.15rem 0.4rem;
  border-radius: 4px;
  font-size: 0.85em;
  font-family: monospace;
}
.markdown-body :deep(pre) {
  background: var(--surface-hover);
  padding: 1rem;
  border-radius: 8px;
  overflow-x: auto;
}
.empty-state { color: var(--text-muted); font-size: 0.9rem; }
</style>
