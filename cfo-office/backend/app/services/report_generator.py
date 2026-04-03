from app.services import claude_client

SYSTEM = """You are a senior financial advisor generating executive-quality CFO reports.
Write in a professional, authoritative style appropriate for board-level distribution.
Use precise financial language, include concrete numbers, and structure output clearly."""

REPORT_PROMPT = """## Available Financial Data
{kpi_data}

## Scenario Analysis Results (if any)
{scenario_data}

## Report Type Requested
{report_type}

## Additional Instructions
{instructions}

---

Generate a comprehensive CFO-quality report. Structure it as follows:

# {report_type}
*Prepared by CFO Office AI Assistant*

## Executive Summary
[3-5 sentences capturing the most important financial story]

## Key Performance Indicators
[Present the most critical KPIs in a clear table format with period-over-period comparison where data is available]

## Financial Performance Analysis
[Deep-dive into revenue, margins, costs, and cash position]

## Strategic Highlights & Risks
[Top opportunities and risks facing the business]

## Forward-Looking Indicators
[Trends, projections, and leading indicators]

## Recommendations
[3-5 specific, actionable recommendations for leadership]

## Appendix: Full KPI Table
[Complete table of all extracted metrics]"""


def stream_report(kpis: list, scenarios: list, report_type: str, instructions: str = ""):
    """Stream a report generation. Yields text chunks."""
    kpi_text = _format_kpis(kpis)
    scenario_text = _format_scenarios(scenarios)

    prompt = REPORT_PROMPT.format(
        kpi_data=kpi_text or "No KPI data loaded yet.",
        scenario_data=scenario_text or "No scenario analyses run yet.",
        report_type=report_type,
        instructions=instructions or "Generate a comprehensive report from the available data.",
    )
    yield from claude_client.stream_response(
        messages=[{"role": "user", "content": prompt}],
        system=SYSTEM,
        max_tokens=10000,
    )


def _format_kpis(kpis: list) -> str:
    if not kpis:
        return ""
    lines = ["| KPI | Value | Unit | Period | Category |", "|-----|-------|------|--------|----------|"]
    for k in kpis:
        lines.append(
            f"| {k.get('name','')} | {k.get('value','')} | {k.get('unit','')} | {k.get('period','')} | {k.get('category','')} |"
        )
    return "\n".join(lines)


def _format_scenarios(scenarios: list) -> str:
    if not scenarios:
        return ""
    parts = []
    for i, s in enumerate(scenarios, 1):
        parts.append(f"### Scenario {i}: {s.get('scenario','')}\n{s.get('result','')[:3000]}")
    return "\n\n".join(parts)
