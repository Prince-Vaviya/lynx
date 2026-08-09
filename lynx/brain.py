import requests
import json

OMNIROUTE_URL = "http://localhost:20128/v1/chat/completions"

SYSTEM_PROMPT = (
    "You are Lynx, a personal voice assistant. "
    "Keep answers short and conversational, because they're read aloud. "
    "No markdown, no bullet points, no emojis."
)

def brain(text: str) -> str:
    payload = {
        "model": "auto",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": text}
        ],
        "stream": True
    }

    reply_chunks = []
    with requests.post(OMNIROUTE_URL, json=payload, stream=True) as r:
        for line in r.iter_lines():
            if not line:
                continue
            if line.startswith(b"data: "):
                chunk = line[len(b"data: "):].decode("utf-8")
                if chunk.strip() == "[DONE]":
                    break
                try:
                    j = json.loads(chunk)
                    delta = j["choices"][0]["delta"]
                    content_piece = delta.get("content")
                    if content_piece:  # only append if it's a real string
                        reply_chunks.append(content_piece)
                except Exception:
                    pass

    return "".join(reply_chunks).strip()
