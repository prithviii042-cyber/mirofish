<template>
  <div
    class="dropzone"
    :class="{ dragging, loading }"
    @dragover.prevent="dragging = true"
    @dragleave="dragging = false"
    @drop.prevent="onDrop"
    @click="fileInput.click()"
  >
    <input ref="fileInput" type="file" :accept="accept" style="display:none" @change="onFileChange" />
    <div v-if="loading" class="dz-content">
      <span class="spinner"></span>
      <span>Processing document…</span>
    </div>
    <div v-else class="dz-content">
      <span class="dz-icon">📄</span>
      <span class="dz-label">Drop a file or <u>click to browse</u></span>
      <span class="dz-hint">PDF, CSV, XLSX, TXT — max 20 MB</span>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
const props = defineProps({ loading: Boolean, accept: { default: ".pdf,.csv,.xlsx,.xls,.txt,.md" } });
const emit = defineEmits(["file"]);
const dragging = ref(false);
const fileInput = ref(null);

function onDrop(e) {
  dragging.value = false;
  const file = e.dataTransfer.files[0];
  if (file) emit("file", file);
}
function onFileChange(e) {
  const file = e.target.files[0];
  if (file) emit("file", file);
  e.target.value = "";
}
</script>

<style scoped>
.dropzone {
  border: 2px dashed var(--border);
  border-radius: 10px;
  padding: 2.5rem;
  text-align: center;
  cursor: pointer;
  transition: all 0.2s;
  background: var(--surface);
}
.dropzone:hover, .dropzone.dragging {
  border-color: var(--accent);
  background: var(--accent-dim);
}
.dropzone.loading { pointer-events: none; opacity: 0.7; }
.dz-content { display: flex; flex-direction: column; align-items: center; gap: 0.5rem; }
.dz-icon { font-size: 2.5rem; }
.dz-label { font-size: 0.95rem; color: var(--text-secondary); }
.dz-label u { color: var(--accent); }
.dz-hint { font-size: 0.78rem; color: var(--text-muted); }
.spinner {
  width: 28px; height: 28px;
  border: 3px solid var(--border);
  border-top-color: var(--accent);
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }
</style>
