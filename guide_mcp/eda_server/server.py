"""MCP stdio entrypoint for the two implemented Phase 1 tools."""

import argparse

from mcp.server.fastmcp import FastMCP

from .tools import EdaTools


def create_server(tools=None):
    backend = tools or EdaTools()
    server = FastMCP("guide-eda-mcp")
    server.tool(structured_output=True)(backend.compile_rtl)
    server.tool(structured_output=True)(backend.simulate)
    return server


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    try:
        create_server().run(transport="stdio")
    except (ValueError, FileNotFoundError) as exc:
        parser.exit(2, f"guide-eda-mcp: {exc}\n")


if __name__ == "__main__":
    main()
