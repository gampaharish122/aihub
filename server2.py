from mcp.server.fastmcp import FastMCP
from typing import Dict
import requests

# Constants
PORT = 1111
API_ENDPOINT_MAIN = "https://apidata.globaldata.com/GlobalDataAIHub/api/Content/GetAIHubAPI"
API_ENDPOINT_SOURCE_DATA = "https://apidata.globaldata.com/GlobalDataAIHub/api/Content/GetAIHubAPISourceData"

AUTH_HEADER = {
    "Authorization": "bearer 8eW2w2fE80Rd2a2Z499Sqs8zN8XmbJFJlNiaOBWoXFan9XrTajkQCYcy-5BzOAcquHHbYpiU-X34lcn3sf1T9VMqbx8hMj6QvLFni_-WhOYsSbQAtNyYiOjtdJtGmdtZPiI6Dgf_anJskc7uBh3vXKQSrfJzSdCmdWn6xLMSNc7qTLI_rLwp3UqjgiJYYYSZ_EyjABQqdW-pbPXPN04etgJOue2JP6EAzGFlK2noUVUL64uufY8me7sjnO3yxHoKZdkzBVZ_5pXUDIcbSBnuhAw9TH0n67solaowHZBxptMA9eEosk2S-7Z2q9RjybuIV9CPksX6aZCcxrJq_xoDSl39utzNMsnDCcb0ZRz9zVE",
    "Accept": "application/json"
}

# Initialize MCP server
mcp = FastMCP("GetAIHubApi", stateless_http=True, host="0.0.0.0", port=PORT)

# Tool 1: Original API
@mcp.tool()
def GetAIHubApi(question: str) -> Dict:
    """
    Calls the GlobalData AI Hub API with hardcoded source types and user-provided question.
    """
    url = f"{API_ENDPOINT_MAIN}?SourceType=News%2CDeals%2CFilings&Question={requests.utils.quote(question)}"
    
    try:
        response = requests.get(url, headers=AUTH_HEADER, timeout=1000)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {"error": str(e)}

# Tool 2: Source Data API with ChunkSize and Date range
@mcp.tool()
def GetAIHubAPISourceData(question: str, chunk_size: int, date_start: str, date_end: str) -> Dict:
    """
    Calls the GlobalData AI Hub SourceData API with SourceType, question, and user-defined chunk size and date range.
    Format for date_start and date_end should be DD-MM-YYYY.
    """
    params = {
        "SourceType": "News,Deals,Filings",
        "Question": question,
        "ChunkSize": chunk_size,
        "DateStart": date_start,
        "DateEnd": date_end
    }
    encoded_params = requests.compat.urlencode(params, quote_via=requests.utils.quote)
    url = f"{API_ENDPOINT_SOURCE_DATA}?{encoded_params}"
    
    try:
        response = requests.get(url, headers=AUTH_HEADER, timeout=1000)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {"error": str(e)}

# Start MCP server
if __name__ == "__main__":
    mcp.run(transport="streamable-http")
