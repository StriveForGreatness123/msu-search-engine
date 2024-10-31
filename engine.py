import requests

def perform_duckduckgo_search(query):
    """Search DuckDuckGo using their API."""
    url = f"https://api.duckduckgo.com/?q={query}&format=json"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()

        results = [
            {'title': item.get('Text', 'No Title'), 'link': item.get('FirstURL', '#')}
            for item in data.get('RelatedTopics', [])
        ]
        return results

    except requests.exceptions.RequestException as e:
        print(f"Error fetching DuckDuckGo results: {e}")
        return []

def perform_github_search(query):
    """Search GitHub repositories using their API."""
    url = f"https://api.github.com/search/repositories?q={query}"
    headers = {'Accept': 'application/vnd.github.v3+json'}
    try:
        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status()
        data = response.json()

        results = [
            {'title': item['full_name'], 'link': item['html_url']}
            for item in data.get('items', [])
        ]
        return results

    except requests.exceptions.RequestException as e:
        print(f"Error fetching GitHub results: {e}")
        return []

def redirect_to_external_sources(query):
    """Provide formatted URLs to external sources for the query."""
    links = {
        "Google Scholar": f"https://scholar.google.com/scholar?q={query}",
        "ResearchGate": f"https://www.researchgate.net/search/publication?q={query}",
        "IEEE Xplore": f"https://ieeexplore.ieee.org/search/searchresult.jsp?queryText={query}",
        "ACM Digital Library": f"https://dl.acm.org/action/doSearch?AllField={query}",
        "Morgan Library": "https://www.morgan.edu/library",
    }
    return links  # Return the links dictionary instead of printing

# The main function is no longer needed since this is a web app
