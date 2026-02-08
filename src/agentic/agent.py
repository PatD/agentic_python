from .ollama_client import OllamaClient
import os
from typing import Optional


def _extract_text_from_response(resp: object) -> Optional[str]:
    if not isinstance(resp, dict):
        return None
    # Common Ollama/v1 response shapes: {'choices': [{'text': ...}]}
    choices = resp.get('choices')
    if isinstance(choices, list) and choices:
        first = choices[0]
        if isinstance(first, dict):
            if 'text' in first and isinstance(first['text'], str):
                return first['text'].strip()
            # Some providers use nested message.content
            msg = first.get('message')
            if isinstance(msg, dict) and isinstance(msg.get('content'), str):
                return msg['content'].strip()

    # Fallbacks
    if isinstance(resp.get('text'), str):
        return resp['text'].strip()
    return None


def _build_episode_prompt(base_prompt: str, episode_number: int) -> str:
    guidance = (
        "Write a complete, original TV episode script in Markdown using a TV-script format. "
        "Tone: hard sci-fi with political intrigue and character-driven drama as part of the TV and book series The Expanse. "
        "Focus on the missing part of the TV show, books 7-9, which have not yet been adapted. "
        "It is ok to create entirely new characters, factions, and locations, or use existing. "
        "Include: a Title line, Episode number, Scene headings (INT/EXT), character names, and stage directions. "
        "Target length: approximately 1200-2500 words."
    )
    return f"{base_prompt}\n\nEpisode: {episode_number}\n\n{guidance}"


def run_demo(model: str = 'gemma3:1b', prompt: str = 'Generate an original TV episode script inspired by The Expanse', episodes: int = 1, save_dir: Optional[str] = None) -> None:
    client = OllamaClient()

    if save_dir:
        os.makedirs(save_dir, exist_ok=True)

    for i in range(1, max(1, episodes) + 1):
        episode_prompt = _build_episode_prompt(prompt, i)
        try:
            resp = client.generate(model=model, prompt=episode_prompt, max_tokens=2000)
        except Exception as e:
            print(f'Failed to call Ollama for episode {i}:', e)
            continue

        text = _extract_text_from_response(resp)
        if text is None:
            print(f'--- Episode {i} Response (raw) ---')
            print(resp)
            continue

        if save_dir:
            fname = os.path.join(save_dir, f'episode_{i:02d}.md')
            try:
                with open(fname, 'w', encoding='utf-8') as f:
                    f.write(text)
                print(f'Wrote episode {i} to', fname)
            except Exception as e:
                print(f'Failed to write episode {i} to file:', e)
        else:
            print(f'--- Episode {i} (markdown) ---')
            print(text)
