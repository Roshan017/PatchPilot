from typing import Any

from patchpilot.tools.registry import ToolRegistry


class ToolExecutor:
    def __init__(self, registry: ToolRegistry) -> None:
        self.registry = registry

    
    def execute(self, tool_name:str, arguments:dict[str, Any]) -> Any: 
        
        tool = self.registry.get(tool_name)

        if not isinstance(arguments, dict):
            raise ValueError("Tool arguments must be a dictionary")
        

        try:
            return tool.function(**arguments)
        
        except TypeError as exc:
            raise ValueError(
                f"Invalid arguments for tool '{tool_name}': {exc} "
            ) from exc