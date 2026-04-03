<template>
  <div class="kpi-card" :class="`cat-${categorySlug}`">
    <div class="kpi-category">{{ kpi.category }}</div>
    <div class="kpi-value">
      <span class="value">{{ kpi.value }}</span>
      <span v-if="kpi.unit" class="unit">{{ kpi.unit }}</span>
    </div>
    <div class="kpi-name">{{ kpi.name }}</div>
    <div v-if="kpi.period" class="kpi-period">{{ kpi.period }}</div>
  </div>
</template>

<script setup>
import { computed } from "vue";
const props = defineProps({ kpi: Object });
const categorySlug = computed(() =>
  (props.kpi.category || "other").toLowerCase().replace(/\s+/g, "-")
);
</script>

<style scoped>
.kpi-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 1.25rem;
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
  transition: transform 0.15s, box-shadow 0.15s;
  border-left: 4px solid var(--accent);
}
.kpi-card:hover { transform: translateY(-2px); box-shadow: 0 4px 20px rgba(0,0,0,0.15); }
.kpi-card.cat-revenue { border-left-color: #22c55e; }
.kpi-card.cat-expenses { border-left-color: #ef4444; }
.kpi-card.cat-profitability { border-left-color: #3b82f6; }
.kpi-card.cat-liquidity { border-left-color: #f59e0b; }
.kpi-card.cat-growth { border-left-color: #8b5cf6; }
.kpi-card.cat-headcount { border-left-color: #06b6d4; }
.kpi-category {
  font-size: 0.7rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--text-muted);
  font-weight: 600;
}
.kpi-value { display: flex; align-items: baseline; gap: 0.3rem; }
.value { font-size: 1.6rem; font-weight: 700; color: var(--text-primary); line-height: 1; }
.unit { font-size: 0.85rem; color: var(--text-secondary); font-weight: 500; }
.kpi-name { font-size: 0.85rem; color: var(--text-secondary); font-weight: 500; }
.kpi-period { font-size: 0.75rem; color: var(--text-muted); margin-top: 0.15rem; }
</style>
