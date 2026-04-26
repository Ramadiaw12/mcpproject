from mcp.server.fastmcp import FastMCP
from langchain_tavily import TavilySearch
from dotenv import load_dotenv

load_dotenv(override=True)

web_search_client = TavilySearch()
mcp = FastMCP(name="mcp-server", host="0.0.0.0", port=24000)

@mcp.tool()
def get_employee_infos(name : str):
    """
    Get information about an employee.
    """
    return {
        "name": name,
        "age" : 23,
        "salary": 10000
    }

@mcp.tool()
def search(query):
    """
    Search the web for the given query.
    Accepts string, dict with 'query', or dict with 'input'.
    """
    # Extraire la requête réelle, quel que soit le format d'entrée
    if isinstance(query, dict):
        # Format 1: {"query": "..."} (ce que vous recevez actuellement)
        if "query" in query:
            search_query = query["query"]
        # Format 2: {"input": {"query": "..."}}
        elif "input" in query and isinstance(query["input"], dict):
            search_query = query["input"].get("query", "")
        else:
            search_query = str(query)
    else:
        search_query = str(query)

    # Maintenant, appelez Tavily avec le format QU'IL ATTEND
    # D'après l'erreur, TavilyResearchInput veut {"input": {"query": ...}}
    results = web_search_client.invoke({"input": {"query": search_query}})
    return results

if __name__ == "__main__":
    mcp.run(transport="streamable-http")

if __name__ == "__main__":
    mcp.run(transport="streamable-http")