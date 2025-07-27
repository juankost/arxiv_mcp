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
    mcp.run(transport=os.environ.get("TRANSPORT", "stdio"))


if __name__ == "__main__":
    main()
