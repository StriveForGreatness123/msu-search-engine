import requests
import os
import webbrowser

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
            {'title': item['name'], 'link': item['html_url']}
            for item in data.get('items', [])
        ]
        return results

    except requests.exceptions.RequestException as e:
        print(f"Error fetching GitHub results: {e}")
        return []

def display_results(source, results):
    """Display results from a given source."""
    if not results:
        print(f"No results found from {source}.")
        return

    print(f"\nResults from {source}:\n")
    for i, result in enumerate(results, 1):
        print(f"{i}. {result['title']}")
        print(f"   Link: {result['link']}\n")

def redirect_to_external_sources(query):
    """Provide formatted URLs to external sources for the query."""
    print("\nExternal Sources:")
    links = {
        "Google Scholar": f"https://scholar.google.com/scholar?q={query}",
        "ResearchGate": f"https://www.researchgate.net/search/publication?q={query}",
        "IEEE Xplore": f"https://ieeexplore.ieee.org/search/searchresult.jsp?queryText={query}",
        "ACM Digital Library": f"https://dl.acm.org/action/doSearch?AllField={query}",
        "Morgan Library": "https://www.morgan.edu/library",
    }

    for name, url in links.items():
        print(f"- {name}: {url}")

def main():
    """Main function to run the multi-source search engine."""
    print("\nWelcome to the Multi-Source Privacy Search Engine!")
    print("Type '/exit' to quit or '/help' for available sources.\n")

    while True:
        query = input("Enter your search query: ").strip()

        if query.lower() == "/exit":
            print("Goodbye!")
            break
        elif query.lower() == "/help":
            print("\nAvailable Sources:")
            print("- DuckDuckGo (direct API)")
            print("- GitHub (direct API)")
            print("- Google Scholar (redirect)")
            print("- ResearchGate (redirect)")
            print("- IEEE Xplore (redirect)")
            print("- ACM Digital Library (redirect)\n")
            continue

        # Perform searches
        print(f"\nSearching for '{query}'...\n")
        duckduckgo_results = perform_duckduckgo_search(query)
        github_results = perform_github_search(query)

        # Display results
        display_results("DuckDuckGo", duckduckgo_results)
        display_results("GitHub", github_results)

        # Provide external source links
        redirect_to_external_sources(query)

        # Option to open a link in the browser
        open_link = input("\nWould you like to open any external source? (y/n): ").strip().lower()
        if open_link == 'y':
            webbrowser.open(f"https://scholar.google.com/scholar?q={query}")

if __name__ == "__main__":
    main()
