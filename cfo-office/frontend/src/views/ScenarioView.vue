<template>
  <div>
    <div class="page-header">
      <h1>🔮 Scenario Modeling</h1>
      <p>Describe a strategic decision and Claude will simulate financial impact and stakeholder reactions.</p>
    </div>

    <div class="scenario-layout">
      <!-- Input panel -->
      <div class="input-panel">
        <div class="card">
          <div class="section-title">📝 Define Scenario</div>

          <div v-if="!store.documents.length" class="context-notice">
            <span>💡</span>
            <span>No documents loaded. <router-link to="/dashboard">Upload financial data</router-link> to give Claude context — or run the scenario with general financial knowledge.</span>
          </div>
          <div v-else class="context-notice success">
            <span>✓</span>
            <span>{{ store.documents.length }} document(s) loaded as context.</span>
          </div>

          <div class="form-group">
            <label>Scenario Description</label>
            <textarea
              v-model="scenarioText"
              placeholder="e.g. 'We are considering reducing headcount by 15% across engineering and G&A to extend runway by 6 months. What are the financial and organizational impacts?'"
              rows="6"
              :disabled="streaming"
            ></textarea>
          </div>

          <div class="quick-scenarios">
            <span class="qs-label">Quick templates:</span>
            <button v-for="qs in quickScenarios" :key="qs" class="qs-btn" @click="scenarioText = qs" :disabled="streaming">
              {{ qs.slice(0, 50) }}…
            </button>
          </div>

          <div class="form-actions">
            <button class="btn btn-primary" @click="runScenario" :disabled="!scenarioText.trim() || streaming">
              {{ streaming ? "Simulating…" : "▶ Run Simulation" }}
            </button>
            <button v-if="streaming" class="btn btn-secondary" @click="stopStream">Stop</button>
          </div>

          <div v-if="error" class="error-msg">{{ error }}</div>
        </div>

        <!-- Scenario history -->
        <div v-if="store.scenarios.length" class="card">
          <div class="section-title">📂 Previous Scenarios</div>
          <div v-for="s in store.scenarios" :key="s.id" class="history-item">
            <div class="history-text" @click="loadScenario(s.id)">
              <span class="history-icon">🔮</span>
              <div class="history-info">
                <span class="history-title">{{ s.scenario.slice(0, 80) }}{{ s.scenario.length > 80 ? '…' : '' }}</span>
                <span class="history-preview">{{ s.preview }}…</span>
              </div>
            </div>
            <button class="btn btn-danger" style="padding:0.3rem 0.6rem;font-size:0.8rem" @click="store.deleteScenario(s.id)">✕</button>
          </div>
        </div>
      </div>

      <!-- Output panel -->
      <div class="output-panel card">
        <div class="output-header">
          <div class="section-title">📈 Simulation Results</div>
          <button v-if="output" class="btn btn-secondary" style="padding:0.35rem 0.8rem;font-size:0.8rem" @click="copyOutput">
            {{ copied ? "✓ Copied" : "Copy" }}
          </button>
        </div>
        <StreamingOutput :content="output" :streaming="streaming">
          <template #empty>
            <div class="output-empty">
              <div style="font-size:3rem;margin-bottom:1rem">🔮</div>
              <p>Define a scenario and click <strong>Run Simulation</strong> to see the analysis here.</p>
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
import { streamScenario, getScenario } from "../api/index.js";
import StreamingOutput from "../components/StreamingOutput.vue";

const store = useCFOStore();
const scenarioText = ref("");
const output = ref("");
const streaming = ref(false);
const error = ref("");
const copied = ref(false);
let stopFn = null;

onMounted(() => {
  store.fetchKPIs();
  store.fetchScenarioHistory();
});

const quickScenarios = [
  "We are considering reducing headcount by 15% across G&A and engineering to extend runway. What are the financial, operational, and cultural impacts?",
  "We plan to raise a $30M Series B at a $150M pre-money valuation. How will this affect our cap table, dilution, and investor narrative?",
  "What happens if we increase pricing by 20% for existing customers? Model churn risk vs. revenue upside.",
  "We are evaluating acquiring a competitor for $50M cash. What are the integration costs, synergies, and financial impact on our balance sheet?",
];

function runScenario() {
  if (!scenarioText.value.trim()) return;
  output.value = "";
  error.value = "";
  streaming.value = true;

  stopFn = streamScenario(
    scenarioText.value,
    (chunk) => { output.value += chunk; },
    (_id) => {
      streaming.value = false;
      store.fetchScenarioHistory();
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

async function loadScenario(id) {
  const { data } = await getScenario(id);
  scenarioText.value = data.scenario;
  output.value = data.result;
}

function copyOutput() {
  navigator.clipboard.writeText(output.value);
  copied.value = true;
  setTimeout(() => (copied.value = false), 2000);
}
</script>

<style scoped>
.scenario-layout { display: grid; grid-template-columns: 380px 1fr; gap: 1.5rem; align-items: start; }
@media (max-width: 960px) { .scenario-layout { grid-template-columns: 1fr; } }

.input-panel { display: flex; flex-direction: column; gap: 1rem; }
.output-panel { min-height: 500px; }
.output-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 1rem; }
.output-header .section-title { margin-bottom: 0; }

.context-notice {
  display: flex; gap: 0.6rem; align-items: flex-start;
  background: var(--accent-dim);
  border: 1px solid rgba(88,166,255,0.3);
  border-radius: 8px;
  padding: 0.75rem;
  font-size: 0.85rem;
  color: var(--text-secondary);
  margin-bottom: 1rem;
}
.context-notice a { color: var(--accent); }
.context-notice.success { background: rgba(63,185,80,0.08); border-color: rgba(63,185,80,0.3); color: var(--accent-green); }

.form-group { display: flex; flex-direction: column; gap: 0.5rem; margin-bottom: 1rem; }
.form-group label { font-size: 0.85rem; font-weight: 600; color: var(--text-secondary); }
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

.quick-scenarios { display: flex; flex-direction: column; gap: 0.4rem; margin-bottom: 1rem; }
.qs-label { font-size: 0.78rem; color: var(--text-muted); font-weight: 600; text-transform: uppercase; letter-spacing: 0.06em; }
.qs-btn {
  text-align: left; padding: 0.5rem 0.75rem;
  background: var(--surface-hover); border: 1px solid var(--border);
  border-radius: 6px; color: var(--text-secondary);
  cursor: pointer; font-size: 0.8rem; font-family: inherit;
  transition: all 0.15s; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}
.qs-btn:hover { border-color: var(--accent); color: var(--text-primary); }
.qs-btn:disabled { opacity: 0.5; cursor: not-allowed; }

.form-actions { display: flex; gap: 0.75rem; flex-wrap: wrap; }

.history-item {
  display: flex; align-items: center; gap: 0.75rem;
  padding: 0.6rem 0; border-bottom: 1px solid var(--border);
}
.history-item:last-child { border-bottom: none; }
.history-text { display: flex; align-items: flex-start; gap: 0.6rem; cursor: pointer; flex: 1; min-width: 0; }
.history-text:hover .history-title { color: var(--accent); }
.history-icon { font-size: 1.1rem; flex-shrink: 0; margin-top: 0.1rem; }
.history-info { display: flex; flex-direction: column; min-width: 0; }
.history-title { font-size: 0.85rem; font-weight: 600; color: var(--text-primary); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; transition: color 0.15s; }
.history-preview { font-size: 0.78rem; color: var(--text-muted); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }

.output-empty { text-align: center; padding: 3rem 1rem; color: var(--text-muted); }
.output-empty p { font-size: 0.9rem; line-height: 1.6; }
</style>
