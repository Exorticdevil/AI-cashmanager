import os
from openai import OpenAI

def build_context(summary: dict) -> str:
    """Convert summary dict into a readable context string for the LLM."""
    by_cat   = summary.get("by_cat", {})
    by_merch = summary.get("by_merch", {})
    by_day   = summary.get("by_day", {})

    cat_lines   = "\n".join([f"  - {k}: ₹{v:,.0f}" for k, v in list(by_cat.items())[:6]])
    merch_lines = "\n".join([f"  - {k}: ₹{v:,.0f}" for k, v in list(by_merch.items())[:5]])
    day_lines   = "\n".join([f"  - {k}: ₹{v:,.0f}" for k, v in by_day.items()])

    return f"""
User's UPI spending summary:
- Total spent: ₹{summary.get('total', 0):,.0f}
- Total transactions: {summary.get('n_trans', 0)}
- Average spend per day: ₹{summary.get('avg_day', 0):,.0f}
- Top category: {summary.get('top_cat', 'N/A')} (₹{summary.get('top_cat_amt', 0):,.0f}, {summary.get('top_cat_pct', 0)}% of total)
- Busiest spending day: {summary.get('busiest_day', 'N/A')}
- Late night transactions (after 10pm): {summary.get('late_night_n', 0)} ({summary.get('late_night_pct', 0)}% of total)

Spending by category:
{cat_lines}

Top merchants:
{merch_lines}

Spending by day of week:
{day_lines}
"""

NARRATIVE_PROMPT = """
You are a friendly, witty personal finance narrator for Indian millennials.
Based on the UPI spending data provided, write a warm and conversational 3-paragraph money story.

Rules:
- Write like a smart friend, not a bank statement
- Be specific — mention actual amounts, merchants, patterns
- Be non-judgmental but honest
- Use Indian context (₹, Swiggy, Zomato, Uber etc.)
- Keep each paragraph 2-3 sentences
- Highlight one surprising pattern in paragraph 2
- End with one forward-looking observation in paragraph 3
- Do NOT use bullet points — flowing prose only
- Total length: 120-160 words
"""

INSIGHTS_PROMPT = """
You are a data analyst for Indian UPI spending patterns.
Based on the spending data, generate exactly 6 specific insights.

Return your response as a JSON array of 6 objects, each with:
- "tag": short label (e.g. "Late night spender", "Friday pattern", "Good habit spotted")
- "tag_type": one of "amber", "blue", "green", "purple"
- "text": 1-2 sentence specific insight mentioning actual rupee amounts or percentages

Rules:
- Be hyper-specific — use real numbers from the data
- Mix positive observations with areas to watch
- Keep insight text under 30 words each
- Indian context only (₹, not $)
- Return ONLY valid JSON, no other text
"""

def generate_narrative(summary: dict, api_key: str) -> str:
    """Generate the main money story narrative."""
    client  = OpenAI(api_key=api_key)
    context = build_context(summary)
    resp    = client.chat.completions.create(
        model    = "gpt-4o-mini",
        messages = [
            {"role": "system", "content": NARRATIVE_PROMPT},
            {"role": "user",   "content": context}
        ],
        temperature = 0.8,
        max_tokens  = 300,
    )
    return resp.choices[0].message.content.strip()

def generate_insights(summary: dict, api_key: str) -> list:
    """Generate 6 specific spending insights as structured data."""
    import json
    client  = OpenAI(api_key=api_key)
    context = build_context(summary)
    resp    = client.chat.completions.create(
        model    = "gpt-4o-mini",
        messages = [
            {"role": "system", "content": INSIGHTS_PROMPT},
            {"role": "user",   "content": context}
        ],
        temperature = 0.7,
        max_tokens  = 600,
    )
    raw = resp.choices[0].message.content.strip()
    raw = raw.replace("```json", "").replace("```", "").strip()
    try:
        return json.loads(raw)
    except Exception:
        return []

def generate_april_tip(summary: dict, api_key: str) -> str:
    """Generate a short forward-looking tip for next month."""
    client  = OpenAI(api_key=api_key)
    context = build_context(summary)
    resp    = client.chat.completions.create(
        model    = "gpt-4o-mini",
        messages = [
            {"role": "system", "content": "You are a concise personal finance advisor for Indian millennials. Based on the UPI data, give ONE specific actionable tip for next month. 2 sentences max. Mention a specific rupee saving. Warm, non-preachy tone."},
            {"role": "user",   "content": context}
        ],
        temperature = 0.7,
        max_tokens  = 100,
    )
    return resp.choices[0].message.content.strip()
