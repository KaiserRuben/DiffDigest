# OLLAMAService.py
import httpx
from typing import Dict

from LLMService.BaseLLMService import BaseLLMService


class OLLAMAService(BaseLLMService):
    def __init__(self, model_url: str, model_name: str):
        self.generate_url = model_url + "/api/generate"
        self.model_name = model_name

    def get_model_name(self) -> str:
        return self.model_name

    def get_url(self) -> str:
        return self.generate_url

    def generate(self, prompt: str) -> Dict[str, str]:
        payload = {"prompt": prompt, "model": self.model_name, "stream": False}

        try:
            response = httpx.post(self.generate_url, json=payload, timeout=300.0)
            response.raise_for_status()
            json_response = response.json()
            return json_response["response"]
        except httpx.HTTPError as e:
            raise Exception(f"Error: Failed to call OLLAMA API. {str(e)}")
