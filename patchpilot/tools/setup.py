from patchpilot.tools.reading import read_file
from patchpilot.tools.searching import list_files, search_code
from patchpilot.tools.registry import Tool, ToolRegistry


def create_tool_registry() -> ToolRegistry:
    registry = ToolRegistry()

    registry.register(
        Tool(
            name = "read_file",
            desc = "Read a source file inside the repository.",
            function=read_file
        )
    )
    registry.register(
        Tool(
            name = "list_files",
            desc = "List all source files in the repository.",
            function=list_files
        )
    )
    registry.register(
        Tool(
            name = "search_code",
            desc = "Search source files for a keyword.",
            function=search_code
        )
    )


    return registry