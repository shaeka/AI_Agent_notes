from mcp.server.fastmcp import FastMCP

mcp = FastMCP('Weather')

@mcp.tool()
async def get_weather(location:str) -> str:
    """
    Get the weather of the location.
    """
    ### Usually we should set up an API call to retrieve weather information here 
    ### but for the purpose of this tutorial, we will just return a fixed result to show it works.
    return 'It is always raining in California.'

if __name__ == '__main__':
    """
    The `transport='streamable-http'` argument will make a localhost link for user to make API call (simulating MCP server).
    We can also setup our own url/ports etc for this server to be accessible by others.
    """
    mcp.run(transport='streamable-http') 
    ### Run python weather.py