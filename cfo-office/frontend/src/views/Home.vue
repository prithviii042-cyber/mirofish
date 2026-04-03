<template>
  <div class="home">
    <div class="hero">
      <div class="hero-badge">Powered by Claude Opus 4.6</div>
      <h1>CFO Office <span class="accent">AI</span></h1>
      <p class="hero-sub">
        Upload your financial documents. Run what-if scenarios. Generate board-ready reports.<br />
        Swarm-intelligence simulation for the modern CFO.
      </p>
      <div class="hero-actions">
        <router-link to="/dashboard" class="btn btn-primary">→ Open Dashboard</router-link>
        <router-link to="/scenario" class="btn btn-secondary">Run a Scenario</router-link>
      </div>
    </div>

    <div class="features">
      <div class="feature-card" v-for="f in features" :key="f.title">
        <div class="feature-icon">{{ f.icon }}</div>
        <h3>{{ f.title }}</h3>
        <p>{{ f.desc }}</p>
        <router-link :to="f.link" class="feature-link">Open →</router-link>
      </div>
    </div>

    <div class="workflow card">
      <h2 class="section-title">⚙️ How it works</h2>
      <div class="steps">
        <div v-for="(step, i) in steps" :key="i" class="step">
          <div class="step-num">{{ i + 1 }}</div>
          <div class="step-content">
            <strong>{{ step.title }}</strong>
            <span>{{ step.desc }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
const features = [
  {
    icon: "📊",
    title: "KPI Dashboard",
    desc: "Upload financial reports (PDF, CSV, XLSX) and Claude extracts key metrics automatically — revenue, EBITDA, margins, cash position, headcount, and more.",
    link: "/dashboard",
  },
  {
    icon: "🔮",
    title: "Scenario Modeling",
    desc: "Describe a strategic decision in plain English. Claude simulates the financial impact and models how each stakeholder group — board, investors, employees — will react.",
    link: "/scenario",
  },
  {
    icon: "📋",
    title: "Report Generation",
    desc: "Generate board-ready CFO reports: monthly reviews, quarterly summaries, investor updates, scenario impact reports — all from your uploaded data.",
    link: "/report",
  },
];

const steps = [
  { title: "Upload documents", desc: "Drop in financial statements, board decks, or data exports (PDF, CSV, XLSX)." },
  { title: "Extract KPIs", desc: "Claude reads the documents and pulls out every financial metric it finds." },
  { title: "Run scenarios", desc: "Describe a what-if situation. Claude simulates impacts and stakeholder reactions." },
  { title: "Generate reports", desc: "Produce polished, board-ready reports from your data and scenario analyses." },
];
</script>

<style scoped>
.home { max-width: 900px; margin: 0 auto; }
.hero {
  text-align: center;
  padding: 4rem 2rem 3rem;
}
.hero-badge {
  display: inline-block;
  font-size: 0.75rem;
  padding: 0.3rem 0.8rem;
  background: var(--accent-dim);
  color: var(--accent);
  border-radius: 20px;
  font-weight: 600;
  margin-bottom: 1.25rem;
  letter-spacing: 0.05em;
}
.hero h1 {
  font-size: 3.5rem;
  font-weight: 800;
  line-height: 1.1;
  margin-bottom: 1rem;
}
.accent { color: var(--accent); }
.hero-sub {
  font-size: 1.1rem;
  color: var(--text-secondary);
  line-height: 1.7;
  margin-bottom: 2rem;
}
.hero-actions { display: flex; gap: 1rem; justify-content: center; flex-wrap: wrap; }

.features {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.25rem;
  margin-bottom: 2rem;
}
.feature-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 1.75rem;
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
  transition: border-color 0.2s;
}
.feature-card:hover { border-color: var(--accent); }
.feature-icon { font-size: 2rem; }
.feature-card h3 { font-size: 1.05rem; font-weight: 700; }
.feature-card p { color: var(--text-secondary); font-size: 0.88rem; line-height: 1.6; flex: 1; }
.feature-link { color: var(--accent); font-size: 0.88rem; font-weight: 600; text-decoration: none; }
.feature-link:hover { text-decoration: underline; }

.steps { display: flex; flex-direction: column; gap: 1rem; }
.step { display: flex; align-items: flex-start; gap: 1rem; }
.step-num {
  width: 28px; height: 28px;
  background: var(--accent-dim);
  color: var(--accent);
  border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-size: 0.8rem; font-weight: 700;
  flex-shrink: 0;
}
.step-content { display: flex; flex-direction: column; gap: 0.2rem; }
.step-content strong { font-size: 0.9rem; }
.step-content span { font-size: 0.85rem; color: var(--text-secondary); }
</style>
