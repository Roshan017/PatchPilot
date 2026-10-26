import json
from urllib.request import Request, urlopen


class OllamClient:
    def __init__(
        self,
        model: str = "qwen2.b:3b",
        base_url: str = "http://localhost:11434"
    ) -> None:

        self.model = model,
        self.base_url = base_url.rstrip("/")

    
    def generate(self, prompt: str) -> str:
        if not prompt.strip():
            raise ValueError("Prompt cannot be empty")

        url = f"{self.base_url}/api/generate"

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }

        request = Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        with urlopen(request, timeout=120) as response:
            result = json.loads(response.read().decode("utf-8"))

        return result["response"]


