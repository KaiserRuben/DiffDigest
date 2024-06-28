import requests

import config


def call_api(url, headers, prompt):
    try:
        response = requests.post(url, headers=headers, json={
            "model": config.OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False
        })
        response.raise_for_status()
        return response.json()['response'].strip()
    except requests.RequestException as e:
        raise Exception(f"Error: Failed to call API. {str(e)}")
