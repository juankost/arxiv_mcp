#!/usr/bin/env python3
"""
Main entry point for the arxiv-mcp server.
"""
import os
from dotenv import load_dotenv
from arxiv_mcp.server import mcp

load_dotenv()


def main():
    """Run the MCP server."""
    transport = os.environ.get("TRANSPORT", "stdio")
    if transport in ["sse", "http", "streamable-http"]:
        host = os.environ.get("HOST", "0.0.0.0")
        port = int(os.environ.get("PORT", 8001))
        mcp.run(transport=transport, host=host, port=port)
    else:  # stdio
        mcp.run(transport=transport)


if __name__ == "__main__":
    main()
