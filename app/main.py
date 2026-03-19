import os
import anthropic
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from groq import Groq
import os
from fastapi import HTTPException

from app.models import (
    ExtractRequest, NewsRequest, AnalyzeRequest,
    ExtractedKeywords, NewsResponse, CredibilityAnalysis, FullAnalysisResponse,
)
from app.extractor import extract_keywords
from app.news_fetcher import fetch_news
from app.analyzer import analyze_credibility

load_dotenv()

# ── App setup ─────────────────────────────────────────────────────────────────
app = FastAPI(
    title="TruthCheck API",
    description="AI-powered fake news detection backend",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:8080" ],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Clients ───────────────────────────────────────────────────────────────────
def get_groq_client() -> Groq:
    key = os.getenv("GROQ_API_KEY")
    if not key:
        raise HTTPException(
            status_code=500,
            detail="GROQ_API_KEY not set in .env"
        )
    return Groq(api_key=key)

def get_news_api_key() -> str:
    key = os.getenv("NEWS_API_KEY")
    if not key:
        raise HTTPException(status_code=500, detail="NEWS_API_KEY not set in .env")
    return key


# ── Routes ────────────────────────────────────────────────────────────────────

@app.get("/health")
def health_check():
    """Check if the server is running and keys are configured."""
    return {
        "status": "ok",
        "anthropic_key": "set" if os.getenv("ANTHROPIC_API_KEY") else "missing",
        "news_api_key": "set" if os.getenv("NEWS_API_KEY") else "missing",
    }


@app.post("/api/extract", response_model=ExtractedKeywords)
def extract(req: ExtractRequest):
    """
    Step 1: Extract keywords, entities, and core claim from raw news text.
    Uses Claude to produce a structured, searchable representation of the claim.
    """
    if not req.text or len(req.text.strip()) < 10:
        raise HTTPException(status_code=400, detail="Text is too short (minimum 10 characters)")

    client = get_anthropic_client()

    try:
        return extract_keywords(client, req.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Keyword extraction failed: {str(e)}")
    
    
@app.post("/api/verify", response_model=FullAnalysisResponse)
def verify_full(req: ExtractRequest):

    if not req.text or len(req.text.strip()) < 10:
        raise HTTPException(status_code=400, detail="Text is too short")

    client = get_groq_client()   # ✅ FIXED
    news_api_key = get_news_api_key()

    # Step 1: Extract
    try:
        extracted = extract_keywords(client, req.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Extraction failed: {str(e)}")

    # Step 2: Fetch news
    try:
        news_result = fetch_news(
            news_api_key,
            extracted.search_query,
            extracted.keywords
        )
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"News fetch failed: {str(e)}")

    # Step 3: Analyze credibility
    try:
        analysis = analyze_credibility(
            client,
            req.text,
            extracted,
            news_result.articles
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

    return FullAnalysisResponse(
        extracted=extracted,
        articles=news_result.articles,
        analysis=analysis,
    )
    
    
    

@app.post("/api/news", response_model=NewsResponse)
def news(req: NewsRequest):
    """
    Step 2: Search NewsAPI using extracted keywords.
    Runs two queries in parallel for broader article coverage.
    """
    if not req.query:
        raise HTTPException(status_code=400, detail="Query is required")

    news_api_key = get_news_api_key()

    try:
        return fetch_news(news_api_key, req.query, req.keywords)
    except ValueError as e:
        raise HTTPException(status_code=502, detail=str(e))
    except ConnectionError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"News fetch failed: {str(e)}")


@app.post("/api/analyze", response_model=CredibilityAnalysis)
def analyze(req: AnalyzeRequest):
    """
    Step 3: Analyze credibility of the claim against the fetched evidence.
    Claude reasons over the articles like a fact-checker and produces a verdict.
    """
    if not req.original_text or not req.articles:
        raise HTTPException(status_code=400, detail="original_text and articles are required")

    client = get_groq_client()

    # Re-hydrate models from dict
    from app.models import ExtractedKeywords, Article
    extracted = ExtractedKeywords(**req.extracted)
    articles = [Article(**a) for a in req.articles]

    try:
        return analyze_credibility(client, req.original_text, extracted, articles)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")




@app.post("/api/verify", response_model=FullAnalysisResponse)
def verify_full(req: ExtractRequest):

    print("\n========== NEW REQUEST ==========")
    print("INPUT TEXT:", req.text)

    if not req.text or len(req.text.strip()) < 10:
        raise HTTPException(status_code=400, detail="Text is too short")

    client = get_groq_client()
    news_api_key = get_news_api_key()

    # Step 1: Extraction
    try:
        print("\n[STEP 1] Extracting keywords...")
        extracted = extract_keywords(client, req.text)
        print("EXTRACTED:", extracted)

    except Exception as e:
        print("[ERROR - EXTRACTION]", str(e))
        raise HTTPException(status_code=500, detail=f"Extraction failed: {str(e)}")

    # Step 2: News Fetch
    try:
        print("\n[STEP 2] Fetching news...")
        news_result = fetch_news(news_api_key, extracted.search_query, extracted.keywords)
        print("QUERY:", extracted.search_query)
        print("ARTICLES FOUND:", len(news_result.articles))

    except Exception as e:
        print("[ERROR - NEWS FETCH]", str(e))
        raise HTTPException(status_code=502, detail=f"News fetch failed: {str(e)}")

    # Step 3: Analysis
    try:
        print("\n[STEP 3] Analyzing credibility...")
        analysis = analyze_credibility(client, req.text, extracted, news_result.articles)
        print("VERDICT:", analysis.verdict)

    except Exception as e:
        print("[ERROR - ANALYSIS]", str(e))
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

    print("========== DONE ==========\n")

    return FullAnalysisResponse(
        extracted=extracted,
        articles=news_result.articles,
        analysis=analysis,
    )