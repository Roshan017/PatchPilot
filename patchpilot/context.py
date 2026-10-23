from dataclasses import dataclass, field
from typing import Any

@dataclass
class AgentContext:
    bug_report: str
    repository_path: str

    investigation: str | None = None
    patch: str | None = None
    test_results: dict[str, Any] = field(default_factory= dict)
    error: str | None = None