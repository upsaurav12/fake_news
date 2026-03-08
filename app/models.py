from pydantic import BaseModel
from typing import Optional


# ── Request Models ────────────────────────────────────────────────────────────

class ExtractRequest(BaseModel):
    text: str


class NewsRequest(BaseModel):
    query: str
    keywords: list[str] = []


class AnalyzeRequest(BaseModel):
    original_text: str
    extracted: dict
    articles: list[dict]


# ── Response Models ───────────────────────────────────────────────────────────

class ExtractedKeywords(BaseModel):
    main_claim: str
    keywords: list[str]
    entities: list[str]
    claim_type: str          # event | statistic | quote | scientific | political
    search_query: str
    time_context: Optional[str] = None


class Article(BaseModel):
    title: str
    source: str
    description: Optional[str] = None
    url: str
    published_at: Optional[str] = None


class NewsResponse(BaseModel):
    articles: list[Article]
    total_found: int


class CredibilityAnalysis(BaseModel):
    verdict: str             # LIKELY TRUE | NEEDS CONTEXT | MISLEADING | LIKELY FALSE | UNVERIFIABLE
    credibility_score: int   # 0-100
    confidence: int          # 0-100
    reasoning: str
    red_flags: list[str]
    supporting_points: list[str]
    source_quality: str      # HIGH | MEDIUM | LOW
    claim_type_analysis: str
    recommendation: str


class FullAnalysisResponse(BaseModel):
    extracted: ExtractedKeywords
    articles: list[Article]
    analysis: CredibilityAnalysis
