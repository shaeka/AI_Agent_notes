from mcp.server.fastmcp import FastMCP

mcp = FastMCP('Math')

@mcp.tool()
def add(a:int, b:int) -> int:
    """
    Add two numbers
    """
    return a+b

@mcp.tool()
def multiply(a:int, b:int) -> int:
    """
    Multiply two numbers
    """
    return a*b

if __name__ == '__main__':
    """
    The `transport='stdio'` argument tells the server to use `Standard Input/Output`(stdin and stdout) to receive and 
    respond to tool function calls.
    """
    mcp.run(transport='stdio')