<template>
  <div>
    <div class="page-header">
      <h1>📋 Report Generator</h1>
      <p>Generate board-ready CFO reports from your uploaded data and scenario analyses.</p>
    </div>

    <div class="report-layout">
      <!-- Config panel -->
      <div class="config-panel">
        <div class="card">
          <div class="section-title">⚙️ Configure Report</div>

          <div class="data-summary">
            <div class="ds-item">
              <span class="ds-count" :class="store.kpis.length ? 'has-data' : ''">{{ store.kpis.length }}</span>
              <span class="ds-label">KPIs loaded</span>
            </div>
            <div class="ds-item">
              <span class="ds-count" :class="store.documents.length ? 'has-data' : ''">{{ store.documents.length }}</span>
              <span class="ds-label">Documents</span>
            </div>
            <div class="ds-item">
              <span class="ds-count" :class="store.scenarios.length ? 'has-data' : ''">{{ store.scenarios.length }}</span>
              <span class="ds-label">Scenarios</span>
            </div>
          </div>

          <div v-if="!store.kpis.length && !store.scenarios.length" class="context-notice">
            💡 No data loaded yet. The report will be generated from Claude's general financial knowledge. <router-link to="/dashboard">Upload documents</router-link> for a data-driven report.
          </div>

          <div class="form-group">
            <label>Report Type</label>
            <select v-model="selectedType" :disabled="streaming">
              <option v-for="t in reportTypes" :key="t" :value="t">{{ t }}</option>
            </select>
          </div>

          <div class="form-group">
            <label>Additional Instructions <span class="optional">(optional)</span></label>
            <textarea
              v-model="instructions"
              placeholder="e.g. 'Focus on cash flow concerns and runway analysis. Highlight risks for the board.'"
              rows="4"
              :disabled="streaming"
            ></textarea>
          </div>

          <button class="btn btn-primary" style="width:100%" @click="generateReport" :disabled="streaming">
            {{ streaming ? "Generating…" : "📋 Generate Report" }}
          </button>
          <button v-if="streaming" class="btn btn-secondary" style="width:100%;margin-top:0.5rem" @click="stopStream">Stop</button>

          <div v-if="error" class="error-msg">{{ error }}</div>
        </div>

        <!-- Report history -->
        <div v-if="store.reports.length" class="card">
          <div class="section-title">📂 Previous Reports</div>
          <div v-for="r in store.reports" :key="r.id" class="history-item">
            <div class="history-text" @click="loadReport(r.id)">
              <span class="history-icon">📋</span>
              <div class="history-info">
                <span class="history-title">{{ r.type }}</span>
                <span class="history-preview">{{ r.preview }}…</span>
              </div>
            </div>
            <button class="btn btn-danger" style="padding:0.3rem 0.6rem;font-size:0.8rem" @click="store.deleteReport(r.id)">✕</button>
          </div>
        </div>
      </div>

      <!-- Report output -->
      <div class="report-output card">
        <div class="output-header">
          <div class="section-title">📄 Report Output</div>
          <div class="output-actions">
            <button v-if="output" class="btn btn-secondary" style="padding:0.35rem 0.8rem;font-size:0.8rem" @click="copyOutput">
              {{ copied ? "✓ Copied" : "📋 Copy" }}
            </button>
            <button v-if="output" class="btn btn-secondary" style="padding:0.35rem 0.8rem;font-size:0.8rem" @click="downloadMd">
              ⬇ Download .md
            </button>
          </div>
        </div>
        <StreamingOutput :content="output" :streaming="streaming">
          <template #empty>
            <div class="output-empty">
              <div style="font-size:3rem;margin-bottom:1rem">📋</div>
              <p>Configure the report settings and click <strong>Generate Report</strong>.</p>
              <p style="margin-top:0.5rem;font-size:0.82rem">Claude will use your loaded KPIs and scenario analyses as source material.</p>
            </div>
          </template>
        </StreamingOutput>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useCFOStore } from "../store/index.js";
import { getReportTypes, streamReport, getReport } from "../api/index.js";
import StreamingOutput from "../components/StreamingOutput.vue";

const store = useCFOStore();
const reportTypes = ref(["CFO Monthly Board Report"]);
const selectedType = ref("CFO Monthly Board Report");
const instructions = ref("");
const output = ref("");
const streaming = ref(false);
const error = ref("");
const copied = ref(false);
let stopFn = null;

onMounted(async () => {
  store.fetchKPIs();
  store.fetchReportHistory();
  try {
    const { data } = await getReportTypes();
    reportTypes.value = data;
  } catch {}
});

function generateReport() {
  output.value = "";
  error.value = "";
  streaming.value = true;

  stopFn = streamReport(
    selectedType.value,
    instructions.value,
    (chunk) => { output.value += chunk; },
    (_id) => {
      streaming.value = false;
      store.fetchReportHistory();
    },
    (err) => {
      error.value = err;
      streaming.value = false;
    },
  );
}

function stopStream() {
  stopFn?.();
  streaming.value = false;
}

async function loadReport(id) {
  const { data } = await getReport(id);
  selectedType.value = data.type;
  output.value = data.content;
}

function copyOutput() {
  navigator.clipboard.writeText(output.value);
  copied.value = true;
  setTimeout(() => (copied.value = false), 2000);
}

function downloadMd() {
  const blob = new Blob([output.value], { type: "text/markdown" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `${selectedType.value.replace(/\s+/g, "_")}.md`;
  a.click();
  URL.revokeObjectURL(url);
}
</script>

<style scoped>
.report-layout { display: grid; grid-template-columns: 340px 1fr; gap: 1.5rem; align-items: start; }
@media (max-width: 960px) { .report-layout { grid-template-columns: 1fr; } }

.config-panel { display: flex; flex-direction: column; gap: 1rem; }
.report-output { min-height: 600px; }
.output-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 1rem; }
.output-header .section-title { margin-bottom: 0; }
.output-actions { display: flex; gap: 0.5rem; }

.data-summary {
  display: grid; grid-template-columns: repeat(3, 1fr);
  gap: 0.75rem; margin-bottom: 1.25rem;
}
.ds-item { text-align: center; background: var(--bg); border-radius: 8px; padding: 0.75rem 0.5rem; }
.ds-count { display: block; font-size: 1.6rem; font-weight: 700; color: var(--text-muted); }
.ds-count.has-data { color: var(--accent); }
.ds-label { font-size: 0.72rem; color: var(--text-muted); font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; }

.context-notice {
  background: var(--accent-dim);
  border: 1px solid rgba(88,166,255,0.3);
  border-radius: 8px;
  padding: 0.75rem;
  font-size: 0.83rem;
  color: var(--text-secondary);
  margin-bottom: 1rem;
  line-height: 1.5;
}
.context-notice a { color: var(--accent); }

.form-group { display: flex; flex-direction: column; gap: 0.5rem; margin-bottom: 1rem; }
.form-group label { font-size: 0.85rem; font-weight: 600; color: var(--text-secondary); }
.optional { font-weight: 400; color: var(--text-muted); }

select {
  background: var(--bg);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 0.65rem 0.75rem;
  color: var(--text-primary);
  font-size: 0.9rem;
  font-family: inherit;
  cursor: pointer;
  width: 100%;
}
select:focus { outline: none; border-color: var(--accent); }
select:disabled { opacity: 0.6; }

textarea {
  background: var(--bg);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 0.75rem;
  color: var(--text-primary);
  font-size: 0.9rem;
  font-family: inherit;
  resize: vertical;
  line-height: 1.6;
  transition: border-color 0.2s;
}
textarea:focus { outline: none; border-color: var(--accent); }
textarea:disabled { opacity: 0.6; }

.history-item { display: flex; align-items: center; gap: 0.75rem; padding: 0.6rem 0; border-bottom: 1px solid var(--border); }
.history-item:last-child { border-bottom: none; }
.history-text { display: flex; align-items: flex-start; gap: 0.6rem; cursor: pointer; flex: 1; min-width: 0; }
.history-text:hover .history-title { color: var(--accent); }
.history-icon { font-size: 1.1rem; flex-shrink: 0; margin-top: 0.1rem; }
.history-info { display: flex; flex-direction: column; min-width: 0; }
.history-title { font-size: 0.85rem; font-weight: 600; color: var(--text-primary); transition: color 0.15s; }
.history-preview { font-size: 0.78rem; color: var(--text-muted); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }

.output-empty { text-align: center; padding: 3rem 1rem; color: var(--text-muted); }
.output-empty p { font-size: 0.9rem; line-height: 1.6; }
</style>
