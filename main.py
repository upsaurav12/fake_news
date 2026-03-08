from groq import Groq
import requests

client = Groq(api_key="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")

response = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[{"role": "user", "content": "Hello"}],
    temperature=0.2
)


def build_block(term, synonyms):
    all_terms = [term] + synonyms.get(term, [])
    quoted = [f'"{t}"' for t in all_terms]
    return "(" + " OR ".join(quoted) + ")"

def build_query(llm_output):
    entities = llm_output["entities"]
    concepts = llm_output["concepts"]
    synonyms = llm_output["synonyms"]

    blocks = []

    for e in entities:
        blocks.append(build_block(e, synonyms))

    for c in concepts:
        blocks.append(build_block(c, synonyms))

    return " AND ".join(blocks)


llm_output = {
  "entities": ["WHO", "China"],
  "concepts": ["lab created virus"],
  "synonyms": {
    "WHO": ["World Health Organization"],
    "lab created virus": [
        "lab-made virus",
        "virus created in lab",
        "laboratory origin virus"
    ],
    "China": ["Chinese"]
  }
}

def call_llama(prompt, temperature=0.2):
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are a precise fact-checking assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=temperature,
        max_tokens=800
    )

    return response.choices[0].message.content


prompt = """
You are an information retrieval system.

From the news text below, generate 5 to 10 concise search queries that can be used directly in:
- Reddit search
- news article search engines
- web search APIs

Rules:
- Each query must contain at least one named entity (person, organization, place, or event)
- Prefer concrete phrases over single words
- Avoid vague terms like "shocking", "breaking", "people say"
- Focus on factual components (who did what, where, when)
- Keep each query under 12 words

Return ONLY a JSON array of strings.

News text:
"WHO confirms virus created in lab in China"
"""



query = build_query(llm_output)

def search_news_smart():
    query = (
        '("WHO" OR "World Health Organization") '
        'AND ("lab-created" OR "lab made" OR "laboratory origin") '
        'AND (virus OR pathogen) '
        'AND China'
    )

    r = requests.get(
        "https://newsapi.org/v2/everything",
        params={
            "q": query,
            "sortBy": "publishedAt",
            "language": "en",
            "pageSize": 50,
            "apiKey": "f6ced00f00dc4875ac6e335c0b2a8161"
        }
    )
    
    # print(query)

    return r.json()["articles"]



result = search_news_smart()


def pretty_article(a):
    print("=" * 80)
    print(f"📰 {a['title']}")
    print(f"Source: {a['source']['name']}")
    print(f"Author: {a.get('author','N/A')}")
    print(f"Published: {a['publishedAt']}")
    print()
    print(a.get("description", ""))
    print()
    print(f"🔗 {a['url']}")
    print("=" * 80)


for r in  result : 
    pretty_article(r)
    
