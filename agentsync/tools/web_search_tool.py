import requests
import re
from typing import Optional
from duckduckgo_search import DDGS
from markdownify import markdownify
from requests.exceptions import RequestException
import agentsync.config as settings

class GoogleSearchTool:
    name = "web_search"
    description = """Performs a Google web search for your query and returns the top search results."""
    inputs = {
        "query": {"type": "string", "description": "The search query to perform."},
        "num_results": {"type": "integer", "description": "Number of results to return", "nullable": True},
    }
    output_type = "string"

    def __init__(self, max_results: int = 5):
        self.api_key = settings.SERPAPI_KEY
        self.max_results = max_results
        if not self.api_key:
            raise ValueError("❌ Error: SERPAPI API key is required.")

    def search(self, query: str, num_results: Optional[int] = None) -> str:
        """
        Perform a web search using SerpApi.

        Args:
            query (str): The search query.
            num_results (int, optional): Number of results to fetch.

        Returns:
            str: Formatted search results.
        """
        if not query:
            raise ValueError("❌ Error: Search query is required.")

        search_results = self._search_serpapi(query, num_results or self.max_results)

        if not search_results:
            return f"No results found for '{query}'. Try a more general query."

        formatted_results = [f"**{i+1}. [{res['title']}]({res['link']})**\n{res['snippet']}" for i, res in enumerate(search_results)]
        return "## Search Results\n\n" + "\n\n".join(formatted_results)

    def _search_serpapi(self, query: str, num_results: int):
        """Helper function to fetch search results from SerpApi."""
        params = {
            "q": query,
            "api_key": self.api_key,
            "engine": "google",
            "google_domain": "google.com",
        }
        response = requests.get("https://serpapi.com/search.json", params=params)

        if response.status_code != 200:
            raise Exception(f"Error fetching search results: {response.text}")

        results = response.json().get("organic_results", [])
        return [{"title": res.get("title"), "link": res.get("link"), "snippet": res.get("snippet", "")} for res in results[:num_results]]

class DuckDuckGoSearchTool:
    name = "web_search"
    description = """Performs a DuckDuckGo web search based on your query and returns the top search results."""
    inputs = {"query": {"type": "string", "description": "The search query to perform."}}
    output_type = "string"

    def __init__(self, max_results=10):
        self.max_results = max_results
        self.ddgs = DDGS()

    def search(self, query: str) -> str:
        results = self.ddgs.text(query, max_results=self.max_results)
        if not results:
            return "No results found! Try a less restrictive/shorter query."
        formatted_results = [f"**{i+1}. [{res['title']}]({res['href']})**\n{res['body']}" for i, res in enumerate(results)]
        return "## Search Results\n\n" + "\n\n".join(formatted_results)


class VisitWebpageTool:
    name = "visit_webpage"
    description = """Visits a webpage and reads its content as a markdown string."""
    inputs = {"url": {"type": "string", "description": "The URL of the webpage to visit."}}
    output_type = "string"

    def search(self, url: str) -> str:
        try:
            response = requests.get(url, timeout=20)
            response.raise_for_status()
            markdown_content = markdownify(response.text).strip()
            markdown_content = re.sub(r"\n{3,}", "\n\n", markdown_content)
            return markdown_content[:10000]  # Truncate long content
        except requests.exceptions.Timeout:
            return "The request timed out. Please try again later or check the URL."
        except RequestException as e:
            return f"Error fetching the webpage: {str(e)}"
        except Exception as e:
            return f"An unexpected error occurred: {str(e)}"
