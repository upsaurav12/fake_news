import json
import anthropic
from app.models import ExtractedKeywords
from groq import Groq


SYSTEM_PROMPT = """You extract structured information from news claims for fact-checking.
Respond ONLY with a valid JSON object. No markdown fences, no explanation, no preamble.

Format exactly:
{
  "main_claim": "one sentence core falsifiable claim stripped of opinion and emotion",
  "keywords": ["keyword1", "keyword2", "keyword3", "keyword4"],
  "entities": ["person/org/place1", "entity2"],
  "claim_type": "event | statistic | quote | scientific | political",
  "search_query": "optimized 4-6 word news search query",
  "time_context": "time reference extracted from claim or null"
}

Rules:
- main_claim must be the single most verifiable assertion in the text
- keywords should be specific and searchable, not generic words
- entities are named people, organizations, countries, or places only
- search_query should be what a journalist would search to verify this"""


import json
from groq import Groq
from app.models import ExtractedKeywords


def extract_keywords(client: Groq, text: str) -> ExtractedKeywords:
    """Step 1: Extract structured keywords using Groq"""

    prompt = f"""
Extract structured information from this news claim.

Return ONLY valid JSON. No explanation.

Format:
{{
  "main_claim": "...",
  "keywords": ["..."],
  "entities": ["..."],
  "claim_type": "...",
  "search_query": "...",
  "time_context": null
}}

Text:
{text}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are an information extraction system."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
        max_tokens=500
    )

    raw = response.choices[0].message.content.strip()

    # 🔥 Safe parsing
    try:
        data = json.loads(raw)
        return ExtractedKeywords(**data)

    except Exception:
        import re

        # try extracting JSON from messy output
        match = re.search(r"\{.*\}", raw, re.DOTALL)
        if match:
            try:
                data = json.loads(match.group())
                return ExtractedKeywords(**data)
            except:
                pass

        # fallback (last resort)
        words = [w for w in text.split() if len(w) > 4][:4]

        return ExtractedKeywords(
            main_claim=text[:150],
            keywords=words,
            entities=[],
            claim_type="event",
            search_query=" ".join(words[:4]),
            time_context=None,
        )