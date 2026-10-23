
import pytest

from patchpilot.tools.registry import Tool, ToolRegistry
from patchpilot.tools.setup import create_tool_registry


def test_register_and_get_tool():
    registry = ToolRegistry()

    tool = Tool(
        name="example",
        desc="An example tool",
        function=lambda: "hello",
    )

    registry.register(tool)

    assert registry.get("example") is tool


def test_duplicate_tool_registration_is_rejected():
    registry = ToolRegistry()
    tool = Tool("example", "Example", lambda: None)

    registry.register(tool)

    with pytest.raises(ValueError, match="Tool already registered"):
        registry.register(tool)


def test_unknown_tool_is_rejected():
    registry = ToolRegistry()

    with pytest.raises(ValueError, match="Unknown tool"):
        registry.get("missing")


def test_default_registry_contains_three_tools():
    registry = create_tool_registry()

    names = {tool.name for tool in registry.list_tools()}

    assert names == {"read_file", "list_files", "search_code"}
