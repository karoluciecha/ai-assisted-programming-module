import json
import sys
import asyncio
from datetime import datetime
import urllib.request
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# Terminal colors for logging
CYAN = '\033[96m'
YELLOW = '\033[93m'
GREEN = '\033[92m'
BLUE = '\033[94m'
RED = '\033[91m'
RESET = '\033[0m'
BOLD = '\033[1m'

def log_message(msg_type, data):
    """Pretty print messages to stderr - helps with debugging"""
    timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    print(f"\n{BOLD}{CYAN}[{timestamp}] {msg_type}{RESET}", file=sys.stderr)
    print(f"{YELLOW}{'─'*60}{RESET}", file=sys.stderr)
    print(json.dumps(data, indent=2), file=sys.stderr)
    print(f"{YELLOW}{'─'*60}{RESET}\n", file=sys.stderr)
    sys.stderr.flush()

# TODO: Implement these helper functions

API_BASE = "https://hacker-news.firebaseio.com/v0"


def fetch_top_stories(count: int = 5) -> list:
    """
    Fetch top story IDs from Hacker News API
    
    Args:
        count: Number of story IDs to return (default 5, max 10)
    
    Returns:
        List of story IDs
    
    API Endpoint: https://hacker-news.firebaseio.com/v0/topstories.json
    
    Hint: This returns a large list of IDs. You need to slice it to get the top N.
    """
    count = max(1, min(int(count), 10))
    with urllib.request.urlopen(f"{API_BASE}/topstories.json", timeout=10) as resp:
        ids = json.loads(resp.read().decode("utf-8"))
    return ids[:count]


def fetch_story_details(story_id: int) -> dict:
    """
    Fetch detailed information about a specific story
    
    Args:
        story_id: The Hacker News story ID
    
    Returns:
        Dictionary with story details (title, author, score, url, time)
    
    API Endpoint: https://hacker-news.firebaseio.com/v0/item/{story_id}.json
    
    The API returns a JSON object with fields like:
    - title: Story title
    - by: Author username
    - score: Number of upvotes
    - url: Link to the story (might be None for Ask HN posts)
    - time: Unix timestamp
    """
    with urllib.request.urlopen(f"{API_BASE}/item/{int(story_id)}.json", timeout=10) as resp:
        item = json.loads(resp.read().decode("utf-8"))
    if not item:  # the API answers null for an unknown id
        return None
    return {
        "title": item.get("title", "(no title)"),
        "author": item.get("by", "unknown"),
        "score": item.get("score", 0),
        "url": item.get("url") or "(no URL, e.g. an Ask HN post)",
        "time": datetime.fromtimestamp(item["time"]).strftime("%Y-%m-%d %H:%M")
        if "time" in item else "unknown",
    }


# Create the MCP server
app = Server("news-server")

@app.list_tools()
async def list_tools() -> list[Tool]:
    """
    Define the tools that this server provides.
    
    You need to define two tools:
    1. get_top_stories
    2. get_story_details
    
    Each tool needs:
    - name: The tool's name (string)
    - description: What the tool does (string)
    - inputSchema: JSON Schema defining the parameters
    
    Hint: Look at the examples in Part 1 and Part 2 for reference.
    """
    log_message("📋 LIST TOOLS REQUEST", {"method": "tools/list"})
    
    # TODO: Define your tools here
    tools = [
        Tool(
            name="get_top_stories",
            description=(
                "Get the current top stories from Hacker News as a numbered list "
                "of story IDs. Use this first to find what is trending; pass an "
                "ID to get_story_details for the title, author and link."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "count": {
                        "type": "integer",
                        "description": "How many stories to return (1-10, default 5)",
                        "default": 5,
                        "minimum": 1,
                        "maximum": 10,
                    }
                },
            },
        ),
        Tool(
            name="get_story_details",
            description=(
                "Get the title, author, score, URL and time of one Hacker News "
                "story, given its numeric story ID (e.g. from get_top_stories)."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "story_id": {
                        "type": "integer",
                        "description": "The Hacker News story ID",
                    }
                },
                "required": ["story_id"],
            },
        ),
    ]
    
    log_message("✅ LIST TOOLS RESPONSE", {
        "tools": [{"name": t.name, "description": t.description} for t in tools]
    })
    
    return tools

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """
    Handle tool execution.
    
    This function is called when a client wants to use one of your tools.
    
    Args:
        name: The name of the tool to execute
        arguments: Dictionary of arguments passed to the tool
    
    Returns:
        List containing a TextContent object with the result
    """
    log_message("🔧 TOOL CALL REQUEST", {
        "tool": name,
        "arguments": arguments
    })
    
    def is_int(v):
        return isinstance(v, int) and not isinstance(v, bool)

    arguments = arguments or {}

    if name == "get_top_stories":
        count = arguments.get("count")
        if count is None:
            count = 5
        if not is_int(count) or not 1 <= count <= 10:
            text = "Error: count must be an integer between 1 and 10."
        else:
            try:
                ids = await asyncio.to_thread(fetch_top_stories, count)
                lines = [f"{i}. story id {sid}" for i, sid in enumerate(ids, 1)]
                text = f"Top {len(ids)} Hacker News stories:\n" + "\n".join(lines)
            except Exception as e:
                text = f"Error: could not fetch top stories ({e})."

    elif name == "get_story_details":
        story_id = arguments.get("story_id")
        if not is_int(story_id) or story_id <= 0:
            text = "Error: story_id is required and must be a positive integer."
        else:
            try:
                story = await asyncio.to_thread(fetch_story_details, story_id)
                if story is None:
                    text = f"Error: no story found with id {story_id}."
                else:
                    text = (
                        f"Title: {story['title']}\n"
                        f"Author: {story['author']}\n"
                        f"Score: {story['score']}\n"
                        f"URL: {story['url']}\n"
                        f"Posted: {story['time']}"
                    )
            except Exception as e:
                text = f"Error: could not fetch story {story_id} ({e})."

    else:
        text = f"Error: unknown tool '{name}'."

    log_message("✅ TOOL CALL RESPONSE", {"text": text})
    return [TextContent(type="text", text=text)]


async def main():
    """Main entry point for the server"""
    print(f"\n{BOLD}{GREEN}🚀 News MCP Server Starting...{RESET}", file=sys.stderr)
    print(f"{CYAN}📰 Using Hacker News API{RESET}\n", file=sys.stderr)
    sys.stderr.flush()
    
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
