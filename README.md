# Agentic Python (local Ollama)

This repository demonstrates a minimal pip-based Python project that talks to a locally running Ollama instance.

Quick start

1. Create a virtual environment and activate it:

```bash
python3 -m venv venv
source venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. By default the client uses `http://127.0.0.1:11434`. If your Ollama HTTP server is running on a different address/port, set `OLLAMA_URL` in the environment or a `.env` file.

4. Run the demo:

```bash
python run.py --model <model-name> --prompt "Hello"
```

Notes
- If you're not sure which port your Ollama HTTP server listens on, confirm the address (common default is `127.0.0.1:11434`).
- This scaffold uses a simple HTTP client and prints the response; adjust `src/agentic/ollama_client.py` for streaming or other advanced patterns.
