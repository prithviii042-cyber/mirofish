<template>
  <nav class="navbar">
    <div class="navbar-brand">
      <span class="brand-icon">💼</span>
      <span class="brand-name">CFO Office <span class="brand-ai">AI</span></span>
    </div>
    <div class="navbar-links">
      <router-link to="/" exact-active-class="active">Home</router-link>
      <router-link to="/dashboard" active-class="active">Dashboard</router-link>
      <router-link to="/scenario" active-class="active">Scenarios</router-link>
      <router-link to="/report" active-class="active">Reports</router-link>
    </div>
    <div class="navbar-model">
      <span class="model-badge">claude-opus-4-6</span>
    </div>
  </nav>
</template>

<style scoped>
.navbar {
  display: flex;
  align-items: center;
  padding: 0 2rem;
  height: 60px;
  background: var(--surface);
  border-bottom: 1px solid var(--border);
  position: sticky;
  top: 0;
  z-index: 100;
}
.navbar-brand {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-right: 2rem;
  text-decoration: none;
}
.brand-icon { font-size: 1.4rem; }
.brand-name {
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--text-primary);
  white-space: nowrap;
}
.brand-ai {
  color: var(--accent);
  font-weight: 800;
}
.navbar-links {
  display: flex;
  gap: 0.25rem;
  flex: 1;
}
.navbar-links a {
  padding: 0.4rem 1rem;
  border-radius: 6px;
  color: var(--text-secondary);
  text-decoration: none;
  font-size: 0.9rem;
  font-weight: 500;
  transition: all 0.15s;
}
.navbar-links a:hover { background: var(--surface-hover); color: var(--text-primary); }
.navbar-links a.active { background: var(--accent-dim); color: var(--accent); }
.navbar-model { margin-left: auto; }
.model-badge {
  font-size: 0.75rem;
  padding: 0.25rem 0.6rem;
  background: var(--accent-dim);
  color: var(--accent);
  border-radius: 20px;
  font-family: monospace;
  font-weight: 600;
}
</style>
