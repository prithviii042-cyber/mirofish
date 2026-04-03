from app.services import claude_client

SYSTEM = """You are an expert CFO advisor and financial scenario analyst.
You help CFOs model the impact of strategic decisions before they are made.
You think rigorously about financial mechanics, stakeholder dynamics, and second-order effects.
Write in a clear, structured, executive-ready style."""

SCENARIO_PROMPT = """## Financial Context
{context}

## Scenario to Simulate
{scenario}

## Analysis Instructions
Provide a comprehensive CFO-level scenario analysis with the following sections:

### 1. Financial Impact Summary
- Quantify projected changes to: Revenue, Gross Margin, EBITDA, Cash Flow, Headcount Cost
- Show best case / base case / worst case ranges where applicable
- Timeline: immediate (0-3 months), near-term (3-12 months), long-term (1-3 years)

### 2. Stakeholder Impact Simulation
For each stakeholder group, simulate their likely reaction and concerns:
- **Board of Directors**: governance, fiduciary concerns
- **Investors / Analysts**: valuation, narrative, comparables
- **Executive Team**: operational feasibility, morale
- **Employees**: impact on headcount, culture, retention risk
- **Customers / Partners**: continuity risk, relationship impact
- **Lenders / Credit Agencies** (if applicable): covenant, credit impact

### 3. Key Risks & Mitigations
List top 5 risks with likelihood (H/M/L), financial impact estimate, and mitigation strategy.

### 4. Decision Framework
- Go / No-Go recommendation with rationale
- 3 critical prerequisites before executing
- Key metrics to monitor during execution
- Abort / pivot triggers

### 5. CFO Action Checklist
Concrete next steps the CFO should take in the next 30 days."""


def stream_scenario(context: str, scenario: str):
    """Stream a scenario simulation. Yields text chunks."""
    prompt = SCENARIO_PROMPT.format(
        context=context[:30000] if context else "No financial context provided.",
        scenario=scenario,
    )
    yield from claude_client.stream_response(
        messages=[{"role": "user", "content": prompt}],
        system=SYSTEM,
        max_tokens=8000,
    )
