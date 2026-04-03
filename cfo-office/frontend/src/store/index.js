import { defineStore } from "pinia";
import * as api from "../api/index.js";

export const useCFOStore = defineStore("cfo", {
  state: () => ({
    kpis: [],
    documents: [],
    scenarios: [],
    reports: [],
    loading: false,
    error: null,
  }),

  actions: {
    async fetchKPIs() {
      const { data } = await api.getKPIs();
      this.kpis = data.kpis;
      this.documents = data.documents;
    },

    async uploadDocument(file) {
      this.loading = true;
      this.error = null;
      try {
        const fd = new FormData();
        fd.append("file", file);
        const { data } = await api.uploadDocument(fd);
        await this.fetchKPIs();
        return data;
      } catch (e) {
        this.error = e.response?.data?.error || e.message;
        throw e;
      } finally {
        this.loading = false;
      }
    },

    async clearKPIs() {
      await api.clearKPIs();
      this.kpis = [];
      this.documents = [];
    },

    async fetchScenarioHistory() {
      const { data } = await api.getScenarioHistory();
      this.scenarios = data;
    },

    async deleteScenario(id) {
      await api.deleteScenario(id);
      this.scenarios = this.scenarios.filter((s) => s.id !== id);
    },

    async fetchReportHistory() {
      const { data } = await api.getReportHistory();
      this.reports = data;
    },

    async deleteReport(id) {
      await api.deleteReport(id);
      this.reports = this.reports.filter((r) => r.id !== id);
    },
  },
});
