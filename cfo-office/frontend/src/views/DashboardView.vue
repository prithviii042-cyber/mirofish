<template>
  <div>
    <div class="page-header">
      <h1>📊 KPI Dashboard</h1>
      <p>Upload financial documents to extract and visualize key metrics.</p>
    </div>

    <div class="dashboard-layout">
      <!-- Left: Upload + Documents -->
      <div class="sidebar">
        <div class="card">
          <div class="section-title">📄 Upload Document</div>
          <FileUpload :loading="store.loading" @file="handleFile" />
          <div v-if="uploadResult" class="success-msg">
            ✓ Extracted {{ uploadResult.kpi_count }} KPIs from {{ uploadResult.filename }}
          </div>
          <div v-if="store.error" class="error-msg">{{ store.error }}</div>
        </div>

        <div v-if="store.documents.length" class="card">
          <div class="section-title">
            🗂 Loaded Documents
            <button class="btn btn-danger" style="margin-left:auto;padding:0.3rem 0.7rem;font-size:0.8rem" @click="clearAll">Clear all</button>
          </div>
          <div v-for="doc in store.documents" :key="doc.filename" class="doc-item">
            <span class="doc-icon">📄</span>
            <div class="doc-info">
              <span class="doc-name">{{ doc.filename }}</span>
              <span class="doc-meta">{{ doc.period || "—" }} · {{ doc.company || "—" }}</span>
            </div>
          </div>
        </div>

        <div v-if="summary" class="card">
          <div class="section-title">💬 AI Summary</div>
          <p class="summary-text">{{ summary }}</p>
        </div>
      </div>

      <!-- Right: KPIs + Charts -->
      <div class="main-panel">
        <div v-if="!store.kpis.length" class="empty-list">
          <div style="font-size:3rem;margin-bottom:1rem">📊</div>
          <p>Upload a financial document to populate the dashboard.</p>
        </div>

        <template v-else>
          <!-- KPI grid by category -->
          <div v-for="(group, cat) in groupedKpis" :key="cat" class="kpi-group">
            <div class="section-title">{{ cat }}</div>
            <div class="kpi-grid">
              <KPICard v-for="kpi in group" :key="kpi.name + kpi.period" :kpi="kpi" />
            </div>
          </div>

          <!-- Charts -->
          <div v-if="chartData.revenue.length || chartData.profitability.length" class="charts-row">
            <div class="card chart-card" v-if="chartData.revenue.length">
              <div class="section-title">Revenue & Expense KPIs</div>
              <Bar :data="revenueChartData" :options="chartOptions" />
            </div>
            <div class="card chart-card" v-if="categoryChartData.labels.length">
              <div class="section-title">KPIs by Category</div>
              <Doughnut :data="categoryChartData" :options="doughnutOptions" />
            </div>
          </div>
        </template>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { Bar, Doughnut } from "vue-chartjs";
import {
  Chart as ChartJS, CategoryScale, LinearScale, BarElement,
  ArcElement, Tooltip, Legend, Title,
} from "chart.js";
import { useCFOStore } from "../store/index.js";
import FileUpload from "../components/FileUpload.vue";
import KPICard from "../components/KPICard.vue";

ChartJS.register(CategoryScale, LinearScale, BarElement, ArcElement, Tooltip, Legend, Title);

const store = useCFOStore();
const uploadResult = ref(null);
const summary = ref("");

onMounted(() => store.fetchKPIs());

async function handleFile(file) {
  uploadResult.value = null;
  try {
    const result = await store.uploadDocument(file);
    uploadResult.value = result;
    summary.value = result.summary || "";
  } catch {}
}

async function clearAll() {
  await store.clearKPIs();
  uploadResult.value = null;
  summary.value = "";
}

const groupedKpis = computed(() => {
  const groups = {};
  for (const kpi of store.kpis) {
    const cat = kpi.category || "Other";
    if (!groups[cat]) groups[cat] = [];
    groups[cat].push(kpi);
  }
  return groups;
});

// Chart data — pick numeric KPIs from Revenue + Expenses categories
const chartData = computed(() => {
  const revenue = store.kpis.filter((k) => ["Revenue", "Profitability"].includes(k.category) && !isNaN(parseFloat(k.value)));
  const profitability = store.kpis.filter((k) => k.category === "Expenses" && !isNaN(parseFloat(k.value)));
  return { revenue, profitability };
});

const revenueChartData = computed(() => {
  const items = store.kpis.filter((k) =>
    ["Revenue", "Profitability", "Expenses"].includes(k.category) && !isNaN(parseFloat(k.value))
  ).slice(0, 8);
  return {
    labels: items.map((k) => k.name),
    datasets: [{
      label: "Value",
      data: items.map((k) => parseFloat(k.value)),
      backgroundColor: items.map((k) => {
        if (k.category === "Revenue") return "rgba(34,197,94,0.7)";
        if (k.category === "Expenses") return "rgba(239,68,68,0.7)";
        return "rgba(59,130,246,0.7)";
      }),
      borderRadius: 6,
    }],
  };
});

const categoryChartData = computed(() => {
  const counts = {};
  for (const kpi of store.kpis) {
    counts[kpi.category || "Other"] = (counts[kpi.category || "Other"] || 0) + 1;
  }
  const colors = ["#58a6ff","#22c55e","#ef4444","#f59e0b","#8b5cf6","#06b6d4","#ec4899"];
  const labels = Object.keys(counts);
  return {
    labels,
    datasets: [{
      data: Object.values(counts),
      backgroundColor: labels.map((_, i) => colors[i % colors.length]),
      borderWidth: 0,
    }],
  };
});

const chartOptions = {
  responsive: true,
  plugins: { legend: { display: false }, tooltip: { callbacks: { label: (ctx) => ` ${ctx.raw.toLocaleString()}` } } },
  scales: {
    x: { ticks: { color: "#8b949e", font: { size: 11 } }, grid: { color: "rgba(255,255,255,0.05)" } },
    y: { ticks: { color: "#8b949e" }, grid: { color: "rgba(255,255,255,0.05)" } },
  },
};

const doughnutOptions = {
  responsive: true,
  plugins: {
    legend: { position: "right", labels: { color: "#8b949e", font: { size: 12 }, padding: 16 } },
  },
};
</script>

<style scoped>
.dashboard-layout { display: grid; grid-template-columns: 300px 1fr; gap: 1.5rem; align-items: start; }
@media (max-width: 900px) { .dashboard-layout { grid-template-columns: 1fr; } }
.sidebar { display: flex; flex-direction: column; gap: 1rem; }
.main-panel { display: flex; flex-direction: column; gap: 1.5rem; }

.doc-item { display: flex; align-items: center; gap: 0.75rem; padding: 0.6rem 0; border-bottom: 1px solid var(--border); }
.doc-item:last-child { border-bottom: none; }
.doc-icon { font-size: 1.2rem; }
.doc-info { display: flex; flex-direction: column; }
.doc-name { font-size: 0.85rem; font-weight: 600; color: var(--text-primary); word-break: break-all; }
.doc-meta { font-size: 0.75rem; color: var(--text-muted); }

.summary-text { font-size: 0.88rem; color: var(--text-secondary); line-height: 1.65; }

.kpi-group { margin-bottom: 0.5rem; }
.kpi-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(170px, 1fr)); gap: 0.85rem; }

.charts-row { display: grid; grid-template-columns: 1fr 1fr; gap: 1.25rem; }
@media (max-width: 700px) { .charts-row { grid-template-columns: 1fr; } }
.chart-card { min-height: 280px; }
</style>
