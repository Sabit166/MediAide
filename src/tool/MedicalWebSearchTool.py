from serpapi import GoogleSearch
from src.main import settings
from agents import function_tool

@function_tool
def web_search(query: str):
    try:
        # Add the query to params dynamically
        params = settings.params.copy()  # Copy existing params to avoid modifying the original
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


def main():
    """
    Test function for the medical web search tool.
    """
    print("Testing Medical Web Search Tool...")
    
    try:
        # Test with a sample medical query
        test_query = "diabetes symptoms and treatment"
        print(f"Testing search for: '{test_query}'")
        
        result = web_search(test_query)
        print("✅ Search completed successfully")
        print("Search Results:")
        print("-" * 50)
        print(result)
        print("-" * 50)
        
    except Exception as e:
        print(f"❌ Error testing medical web search tool: {e}")
        print("Make sure you have:")
        print("1. SERPAPI_API_KEY in your environment variables")
        print("2. Valid SerpAPI credentials")
        print("3. Internet connection")


if __name__ == "__main__":
    main()
