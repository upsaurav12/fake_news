import requests

def search_factcheck(query):
    url = "https://toolbox.google.com/factcheck/api/v1/claimsearch"

    params = {
        "query": query,
        "languageCode": "en"
    }

    r = requests.get(url, params=params, timeout=10)

    if r.status_code != 200:
        return []

    data = r.json()
    results = []

    for claim in data.get("claims", []):
        review = claim.get("claimReview", [{}])[0]

        results.append({
            "text": claim.get("text"),
            "claimant": claim.get("claimant"),
            "publisher": review.get("publisher", {}).get("name"),
            "rating": review.get("textualRating"),
            "url": review.get("url")
        })

    return results


# Example
print(search_factcheck("WHO confirms virus created in lab China"))
