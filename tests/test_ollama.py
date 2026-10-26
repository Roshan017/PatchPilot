from ast import JoinedStr
import json
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError


url = "http://localhost:11434/api/generate"


payload = {
    "model": "qwen2.5:3b",
    "prompt": "Explain about AI and its uses",
    "stream": False
}


request = Request(
    url,
    data=json.dumps(payload).encode("utf-8"),
    headers={"Content-Type": "application/json"},
    method="POST"
)

try: 
    with urlopen(request, timeout=120) as response:
        res = json.loads(response.read().decode("utf-8"))

    print("MODEL:", res["model"])
    print("RESPONSE:", res["response"])

except (URLError, HTTPError, TimeoutError ) as e:
    print("Could not connect to OLLAMA: ", e)