from dataclasses import dataclass
from typing import Any, Callable


@dataclass(frozen=True)

class Tool:
    name:str
    desc:str
    function: Callable[..., Any]

class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, Tool] = {}

    
    def register(self, tool:Tool) -> None:
        if tool.name in self._tools:
           raise ValueError(f"Tool already registered: {tool.name}")
        
        self._tools[tool.name] = tool

    
    def get(self, name:str) -> Tool:
        if name not in self._tools:
            raise ValueError(f"Unknown tool: {name}")
        
        return self._tools[name]
    
    def list_tools(self) -> list[Tool]:
        return list(self._tools.values())