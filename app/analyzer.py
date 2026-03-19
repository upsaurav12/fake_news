import json
import anthropic
from app.models import Article, CredibilityAnalysis, ExtractedKeywords
from app.news_fetcher import score_source_quality
from groq import Groq

SYSTEM_PROMPT = """You are a senior fact-checker at an investigative journalism outlet.

Your job: analyze a news claim against real evidence from news articles and produce a nuanced, honest credibility assessment.

CORE RULES:
1. Base verdict ONLY on the evidence provided — not your training knowledge
2. If evidence is absent or off-topic, say UNVERIFIABLE — never fabricate support
3. Distinguish between what sources confirm vs. what they merely imply
4. A claim can be technically true but MISLEADING if context is stripped
5. Multiple low-quality sources agreeing is NOT the same as one high-quality source confirming
6. Older articles (>30 days) should reduce confidence for time-sensitive claims

VERDICT DEFINITIONS:
- LIKELY TRUE: 2+ credible sources directly confirm the core claim
- NEEDS CONTEXT: Claim is partially true but missing critical context that changes its meaning
- MISLEADING: Facts are selectively presented to imply something false
- LIKELY FALSE: Credible sources directly contradict the core claim
- UNVERIFIABLE: Insufficient or irrelevant evidence to make a determination

Respond ONLY with a valid JSON object. No markdown, no explanation.

Format exactly:
{
  "verdict": "LIKELY TRUE | NEEDS CONTEXT | MISLEADING | LIKELY FALSE | UNVERIFIABLE",
  "credibility_score": <integer 0-100>,
  "confidence": <integer 0-100>,
  "reasoning": "2-3 sentences explaining your verdict with specific reference to the evidence",
  "red_flags": ["specific concern drawn from evidence or claim structure"],
  "supporting_points": ["specific point of support from evidence"],
  "source_quality": "HIGH | MEDIUM | LOW",
  "claim_type_analysis": "one sentence about what type of claim this is and what verification it requires",
  "recommendation": "one concrete action the reader should take"
}"""


def build_evidence_block(articles: list[Article]) -> str:
    """Format articles into a structured evidence block for the prompt."""
    if not articles:
        return "No relevant articles found."

    lines = []
    for i, a in enumerate(articles, 1):
        lines.append(
            f"[{i}] SOURCE: {a.source}\n"
            f"    HEADLINE: {a.title}\n"
            f"    SUMMARY: {a.description or 'No description available'}\n"
            f"    DATE: {a.published_at or 'Unknown'}"
        )
    return "\n\n".join(lines)


def analyze_credibility(
    client: Groq,
    original_text: str,
    extracted: ExtractedKeywords,
    articles: list[Article],
) -> CredibilityAnalysis:

    source_quality = score_source_quality(articles)
    evidence_block = build_evidence_block(articles)

    prompt = f"""
You are a professional fact-checker.

Analyze the claim using the provided evidence.

Return ONLY valid JSON. No explanation.

Format:
{{
  "verdict": "...",
  "credibility_score": 0-100,
  "confidence": 0-100,
  "reasoning": "...",
  "red_flags": ["..."],
  "supporting_points": ["..."],
  "claim_type_analysis": "...",
  "recommendation": "..."
}}

---

ORIGINAL CLAIM:
"{original_text}"

CORE CLAIM:
"{extracted.main_claim}"

CLAIM TYPE: {extracted.claim_type}
ENTITIES: {", ".join(extracted.entities) if extracted.entities else "None"}
TIME: {extracted.time_context or "Not specified"}
SOURCE QUALITY: {source_quality}

EVIDENCE ({len(articles)} articles):
{evidence_block}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are a strict fact-checking system."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
        max_tokens=1000
    )

    raw = response.choices[0].message.content.strip()

    # ✅ Safe JSON parsing
    try:
        data = json.loads(raw)

    except Exception:
        match = re.search(r"\{.*\}", raw, re.DOTALL)
        if match:
            data = json.loads(match.group())
        else:
            # fallback
            return CredibilityAnalysis(
                verdict="UNVERIFIABLE",
                credibility_score=50,
                confidence=30,
                reasoning="LLM output parsing failed.",
                red_flags=[],
                supporting_points=[],
                source_quality=source_quality,
                claim_type_analysis="Parsing failure",
                recommendation="Check manually."
            )

    # enforce source quality
    data["source_quality"] = source_quality

    return CredibilityAnalysis(**data)