
import pytest

from patchpilot.tools.executor import ToolExecutor
from patchpilot.tools.setup import create_tool_registry


def test_executor_runs_registered_tool(tmp_path):
    repo = tmp_path / "sample-repo"
    repo.mkdir()

    (repo / "auth.py").write_text(
        "def login(): pass\n",
        encoding="utf-8",
    )

    executor = ToolExecutor(create_tool_registry())

    result = executor.execute(
        "list_files",
        {"repository_path": str(repo)},
    )

    assert result == ["auth.py"]


def test_executor_rejects_unknown_tool():
    executor = ToolExecutor(create_tool_registry())

    with pytest.raises(ValueError, match="Unknown tool"):
        executor.execute("missing_tool", {})


def test_executor_rejects_missing_arguments():
    executor = ToolExecutor(create_tool_registry())

    with pytest.raises(ValueError, match="Invalid arguments"):
        executor.execute("list_files", {})


def test_executor_returns_tool_result(tmp_path):
    repo = tmp_path / "sample-repo"
    repo.mkdir()

    (repo / "auth.py").write_text(
        "def login(): pass\n",
        encoding="utf-8",
    )

    executor = ToolExecutor(create_tool_registry())

    result = executor.execute(
        "search_code",
        {"repository_path": str(repo), "keyword": "login"},
    )

    assert result == ["auth.py:1: def login(): pass"]

