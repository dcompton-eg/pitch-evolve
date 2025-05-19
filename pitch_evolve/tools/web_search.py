import logging
import os
from typing import Dict, Any, List, Optional
from tavily import TavilyClient

log_formatter = logging.Formatter(
    '%(levelname)s::%(asctime)s::%(module)s::%(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
console_handler = logging.StreamHandler()
console_handler.setFormatter(log_formatter)
logger = logging.getLogger("web_discovery")
logger.setLevel(logging.INFO)
logger.addHandler(console_handler)


def web_search(query: str,
               recency: str,
               max_results: int = 5) -> Optional[List[Dict[str, Any]]]:
    """
    Retrieve information from the web using Tavily's search engine.

    Parameters:
        query: The information query to search for
        recency: Timeframe filter ('day'/'d', 'week'/'w', 'month'/'m', 'year'/'y')
        max_results: Number of results to return (default: 5)

    Returns:
        Collection of search results or None if search fails
    """
    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")  # Tavily API key for search
    search_engine = TavilyClient(api_key=TAVILY_API_KEY)

    try:
        logger.info(
            f"Initiating web search for: {query}, limit: {max_results}")

        search_response = search_engine.search(
            query,
            max_results=max_results,
            time_range=recency,
            include_raw_content=True
        )

        # Process the results
        results = search_response.get("results", [])
        processed_results = []
        seen_urls = set()  # Track URLs we've already seen

        for result in results:
            url = result.get("url", "")

            # Skip duplicate URLs
            if url in seen_urls:
                logger.info(f"Skipping duplicate search result URL: {url}")
                continue

            seen_urls.add(url)
            processed_results.append({
                "title": result.get("title", "Untitled"),
                "content": result.get("content"),
                "raw_content": result.get("raw_content"),
                "url": url
            })

        logger.info(
            f"Retrieved {len(processed_results)} unique web results")
        return processed_results

    except Exception as e:
        logger.error(f"Web search error: {e}")
        return None
