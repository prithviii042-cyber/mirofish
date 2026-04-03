import json
import re
from app.services import claude_client

SYSTEM = """You are a senior financial analyst assistant for a CFO office.
Extract key financial KPIs from the provided document text.
Always respond with valid JSON only — no markdown fences, no preamble."""

EXTRACTION_PROMPT = """Extract all financial KPIs from this document and return a JSON object.

Document:
{text}

Return a JSON object with this exact structure:
{{
  "kpis": [
    {{
      "name": "KPI name",
      "value": "numeric value or string",
      "unit": "USD / % / headcount / etc.",
      "period": "period it covers e.g. Q3 2024 or FY2024",
      "category": "one of: Revenue | Expenses | Profitability | Liquidity | Growth | Headcount | Other"
    }}
  ],
  "summary": "2-3 sentence executive summary of the financial picture",
  "period": "overall reporting period covered by the document",
  "company": "company name if identifiable, else null"
}}

Include every numeric KPI you can find: revenue, EBITDA, net income, gross margin, operating margin,
cash position, burn rate, runway, headcount, ARR, MRR, CAC, LTV, churn, debt, capex, etc."""


def extract_kpis(document_text: str) -> dict:
    """Use Claude to extract structured KPIs from document text."""
    prompt = EXTRACTION_PROMPT.format(text=document_text[:40000])  # cap at ~40K chars
    raw = claude_client.complete(
        messages=[{"role": "user", "content": prompt}],
        system=SYSTEM,
        max_tokens=4000,
    )
    # Strip any accidental markdown fences
    raw = re.sub(r"^```(?:json)?\s*", "", raw.strip())
    raw = re.sub(r"\s*```$", "", raw.strip())
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {"kpis": [], "summary": raw, "period": None, "company": None}
