from mcp.server.fastmcp import FastMCP
import math


# ============================================================
# MCP SERVER
# ============================================================

mcp = FastMCP("Math")


# ============================================================
# MCP TOOLS
# ============================================================

@mcp.tool()
def add(a: float, b: float) -> float:
    """Add two numbers."""
    return a + b


@mcp.tool()
def multiply(a: float, b: float) -> float:
    """Multiply two numbers."""
    return a * b


@mcp.tool()
def divide(a: float, b: float) -> float:
    """Divide a by b."""

    if b == 0:
        raise ValueError("Cannot divide by zero")

    return a / b


@mcp.tool()
def square_root(a: float) -> float:
    """Calculate the square root of a number."""

    if a < 0:
        raise ValueError(
            "Cannot calculate square root of a negative number"
        )

    return math.sqrt(a)


# ============================================================
# START MCP SERVER
# ============================================================

if __name__ == "__main__":
    mcp.run(transport="stdio")