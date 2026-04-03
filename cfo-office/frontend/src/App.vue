<template>
  <NavBar />
  <main class="main-content">
    <router-view />
  </main>
</template>

<script setup>
import NavBar from "./components/NavBar.vue";
</script>

<style>
:root {
  --bg: #0d1117;
  --surface: #161b22;
  --surface-hover: #21262d;
  --border: #30363d;
  --text-primary: #e6edf3;
  --text-secondary: #8b949e;
  --text-muted: #6e7681;
  --accent: #58a6ff;
  --accent-dim: rgba(88, 166, 255, 0.1);
  --accent-green: #3fb950;
  --accent-red: #f85149;
  --accent-yellow: #d29922;
  --radius: 10px;
  --shadow: 0 2px 12px rgba(0, 0, 0, 0.3);
}

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", system-ui, sans-serif;
  background: var(--bg);
  color: var(--text-primary);
  min-height: 100vh;
}

.main-content {
  max-width: 1280px;
  margin: 0 auto;
  padding: 2rem 1.5rem;
}

/* Shared utilities */
.btn {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.55rem 1.2rem;
  border-radius: 6px;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  border: none;
  transition: all 0.15s;
  text-decoration: none;
}
.btn-primary { background: var(--accent); color: #0d1117; }
.btn-primary:hover { filter: brightness(1.1); }
.btn-primary:disabled { opacity: 0.5; cursor: not-allowed; }
.btn-secondary { background: var(--surface-hover); color: var(--text-secondary); border: 1px solid var(--border); }
.btn-secondary:hover { border-color: var(--accent); color: var(--text-primary); }
.btn-danger { background: rgba(248, 81, 73, 0.15); color: var(--accent-red); border: 1px solid transparent; }
.btn-danger:hover { border-color: var(--accent-red); }

.card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 1.5rem;
}

.page-header {
  margin-bottom: 2rem;
}
.page-header h1 {
  font-size: 1.6rem;
  font-weight: 700;
  color: var(--text-primary);
}
.page-header p {
  color: var(--text-secondary);
  margin-top: 0.35rem;
  font-size: 0.95rem;
}

.error-msg {
  background: rgba(248, 81, 73, 0.1);
  border: 1px solid var(--accent-red);
  color: var(--accent-red);
  padding: 0.75rem 1rem;
  border-radius: 8px;
  font-size: 0.9rem;
  margin-top: 0.75rem;
}

.success-msg {
  background: rgba(63, 185, 80, 0.1);
  border: 1px solid var(--accent-green);
  color: var(--accent-green);
  padding: 0.75rem 1rem;
  border-radius: 8px;
  font-size: 0.9rem;
  margin-top: 0.75rem;
}

.section-title {
  font-size: 1rem;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 1rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.empty-list {
  text-align: center;
  padding: 3rem;
  color: var(--text-muted);
  font-size: 0.9rem;
}
</style>
