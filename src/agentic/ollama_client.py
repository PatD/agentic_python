import os
import requests
from typing import Any


class OllamaClient:
    """Minimal Ollama HTTP client.

    Configurable via the `OLLAMA_URL` environment variable. Default: http://127.0.0.1:11434
    """

    def __init__(self, base_url: str | None = None):
        self.base_url = base_url or os.getenv('OLLAMA_URL', 'http://127.0.0.1:11434')

    def generate(self, model: str, prompt: str, max_tokens: int = 512, timeout: int = 120) -> Any:
        """Send a generation request to Ollama and return the response.

        This uses a JSON POST to `/v1/completions` (Ollama's HTTP-compatible API).
        If your Ollama setup uses a different endpoint or streaming, adapt this method.
        """
        url = f"{self.base_url}/v1/completions"
        payload = {
            'model': model,
            'prompt': prompt,
            'max_tokens': max_tokens,
        }
        resp = requests.post(url, json=payload, timeout=timeout)
        resp.raise_for_status()
        try:
            return resp.json()
        except ValueError:
            return resp.text
