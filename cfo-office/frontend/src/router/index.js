import { createRouter, createWebHistory } from "vue-router";
import Home from "../views/Home.vue";
import DashboardView from "../views/DashboardView.vue";
import ScenarioView from "../views/ScenarioView.vue";
import ReportView from "../views/ReportView.vue";

const routes = [
  { path: "/", component: Home },
  { path: "/dashboard", component: DashboardView },
  { path: "/scenario", component: ScenarioView },
  { path: "/report", component: ReportView },
];

export default createRouter({
  history: createWebHistory(),
  routes,
});
