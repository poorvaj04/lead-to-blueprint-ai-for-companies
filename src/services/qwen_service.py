import requests

OLLAMA_URL = "http://localhost:11434/api/generate"

def ask_qwen(prompt):

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": "qwen3:8b",
            "prompt": prompt,
            "stream": False
        }
    )

    data = response.json()

    return data["respon-se"]