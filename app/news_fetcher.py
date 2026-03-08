import requests
from app.models import Article, NewsResponse

NEWS_API_BASE = "https://newsapi.org/v2/everything"

# Known high-credibility sources for source quality scoring
HIGH_CREDIBILITY_SOURCES = {
    "reuters", "associated press", "ap news", "bbc news", "bbc",
    "the guardian", "the new york times", "washington post",
    "al jazeera", "npr", "abc news", "cbs news", "nbc news",
    "the economist", "financial times", "bloomberg", "time",
    "the atlantic", "politifact", "snopes", "factcheck.org",
}

MEDIUM_CREDIBILITY_SOURCES = {
    "cnn", "fox news", "msnbc", "huffpost", "buzzfeed news",
    "the hill", "axios", "vox", "slate", "salon",
    "daily mail", "the independent", "usa today",
}


def fetch_news(api_key: str, query: str, keywords: list[str]) -> NewsResponse:
    """
    Step 2: Fetch articles from NewsAPI using two parallel queries:
    - Primary: the optimized search query from Claude
    - Secondary: top 2 raw keywords for broader coverage
    """

    seen_urls = set()
    all_articles = []

    queries_to_run = [query]
    if keywords:
        keyword_query = " ".join(keywords[:2])
        if keyword_query.lower() != query.lower():
            queries_to_run.append(keyword_query)

    for q in queries_to_run:
        try:
            response = requests.get(
                NEWS_API_BASE,
                params={
                    "q": q,
                    "pageSize": 6,
                    "sortBy": "relevancy",
                    "language": "en",
                    "apiKey": api_key,
                },
                timeout=10,
            )
            data = response.json()

            if data.get("status") != "ok":
                raise ValueError(data.get("message", "NewsAPI error"))

            for a in data.get("articles", []):
                url = a.get("url", "")
                title = a.get("title", "") or ""

                # Skip duplicates and removed articles
                if url in seen_urls or title == "[Removed]" or not title:
                    continue

                seen_urls.add(url)
                all_articles.append(
                    Article(
                        title=title,
                        source=a.get("source", {}).get("name", "Unknown"),
                        description=a.get("description"),
                        url=url,
                        published_at=a.get("publishedAt", "")[:10] if a.get("publishedAt") else None,
                    )
                )
        except requests.RequestException as e:
            raise ConnectionError(f"Failed to reach NewsAPI: {e}")

    return NewsResponse(articles=all_articles[:8], total_found=len(all_articles))


def score_source_quality(articles: list[Article]) -> str:
    """
    Assess overall source quality based on how many high-credibility
    outlets are represented in the fetched articles.
    """
    if not articles:
        return "LOW"

    high_count = sum(
        1 for a in articles
        if a.source.lower() in HIGH_CREDIBILITY_SOURCES
    )
    medium_count = sum(
        1 for a in articles
        if a.source.lower() in MEDIUM_CREDIBILITY_SOURCES
    )

    ratio = high_count / len(articles)

    if ratio >= 0.5 or high_count >= 3:
        return "HIGH"
    elif ratio >= 0.25 or medium_count >= 2:
        return "MEDIUM"
    else:
        return "LOW"
