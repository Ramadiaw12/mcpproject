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
def search(query : str):
    """
    Search the web for the given query.
    """
    results = web_search_client.invoke({"query":query})
    return results

if __name__ == "__main__":
    mcp.run(transport="streamable-http")

# if __name__ == "__main__":
#     mcp.run(transport="streamable-http")
