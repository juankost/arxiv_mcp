#!/usr/bin/env python3
"""
Main entry point for the arxiv-mcp server.
"""

from src.server import mcp


def main():
    """Run the MCP server."""
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
