import requests

def search_gdelt(query, max_records=50):
    url = "https://api.gdeltproject.org/api/v2/doc/doc"
    
    params = {
        "query": query,
        "mode": "artlist",
        "maxrecords": max_records,
        "format": "json"
    }

    r = requests.get(url, params=params, timeout=10)

    if r.status_code != 200:
        return []

    data = r.json()
    articles = []

    for a in data.get("articles", []):
        articles.append({
            "title": a.get("title"),
            "source": a.get("sourceCountry"),
            "url": a.get("url"),
            "seendate": a.get("seendate")
        })

    return articles


# Example
print(search_gdelt("WHO confirms virus lab China"))
