from tavily import TavilyClient
from langchain_core.tools import tool
from src.config import Config
from src.tools.schemas import WebSearchInput

# Initialize Tavily client once at module level (not on every call)
_client = TavilyClient(api_key=Config.TAVILY_API_KEY)


@tool(args_schema=WebSearchInput)
def web_search(query: str) -> str:
    """
    Search the web for current information.
    Use this for recent events, facts, research papers, or anything
    that requires up-to-date information.

    Args:
        query: The search query string

    Returns:
        A formatted string with search results including titles, URLs, and content
    """
    try:
        response = _client.search(
            query=query,
            max_results=5,          # top 5 results
            search_depth="advanced", # deeper crawl vs "basic"
            include_answer=True,     # Tavily's own AI summary of results
        )

        # Format results into clean readable text for the LLM
        output = []

        # Tavily's own summary answer (quick overview)
        if response.get("answer"):
            output.append(f"Summary: {response['answer']}\n")

        # Individual search results
        for i, result in enumerate(response.get("results", []), 1):
            output.append(
                f"[{i}] {result['title']}\n"
                f"URL: {result['url']}\n"
                f"Content: {result['content'][:500]}...\n"  # first 500 chars
            )

        return "\n".join(output) if output else "No results found."

    except Exception as e:
        # Never let a tool crash the whole agent
        return f"Search failed: {str(e)}"