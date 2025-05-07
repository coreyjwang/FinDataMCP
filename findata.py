from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP

# https://modelcontextprotocol.io/quickstart/server

##### Initialize FastMCP server #############################################
mcp = FastMCP("findata")

# BASE_URL = "https://query1.finance.yahoo.com"
# HEADERS = {
#     "User-Agent": "finance-mcp/1.0"
# }


##### Helper functions to query & format ####################################
async def fetch_json(url: str) -> dict[str, Any] | None:
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=HEADERS)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None


##### Tool execution handler ################################################
@mcp.tool()
async def get_stock_price(symbol: str) -> str:
    """Get the current stock price for a ticker symbol.

    Args:
        symbol: Stock ticker (e.g. AAPL, TSLA, MSFT)
    """
    url = f"http://query1.finance.yahoo.com/v10/finance/quoteSummary/{symbol}?modules=financialData"
    data = await fetch_json(url)

    try:
        fin_data = data["quoteSummary"]["result"][0]["financialData"]
        price = fin_data["currentPrice"]["raw"]
        currency = fin_data.get("financialCurrency", "USD")
        return f"{symbol.upper()} is trading at {price} {currency}."
    except Exception:
        return f"Could not retrieve stock price for {symbol}."


##### Run server ############################################################
if __name__ == "__main__":
    mcp.run(transport="stdio")
