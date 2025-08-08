from serpapi import GoogleSearch
from src.config.serp_config import params
from agents import function_tool

@function_tool
def web_search(query: str):
    try:
        # Add the query to params dynamically
        params['q'] = query
        
        search = GoogleSearch(params)
        results = search.get_dict()
        
        # Format the results
        if "organic_results" in results:
            organic_results = results["organic_results"]
            formatted_results = []
            for idx, result in enumerate(organic_results[:3], 1):  # Get top 3 results
                title = result.get("title", "No title")
                link = result.get("link", "No link")
                snippet = result.get("snippet", "No description")
                formatted_results.append(f"{idx}. {title}\n   {link}\n   {snippet}")
            
            return f"Search results for '{query}':\n" + "\n\n".join(formatted_results)
        else:
            return f"No organic results found for '{query}'"
            
    except Exception as e:
        return f"Error performing search: {str(e)}"
