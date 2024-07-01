# AnthropicService.py
from typing import Dict
from anthropic import Anthropic

from LLMService.BaseLLMService import BaseLLMService


class AnthropicService(BaseLLMService):
    def __init__(self, api_key: str, model: str):
        self.client = Anthropic(api_key=api_key)
        self.model = model

    def get_model_name(self) -> str:
        return self.model

    def get_url(self) -> str:
        return "-"

    def generate(self, prompt: str) -> str:
        try:
            response = self.client.messages.create(
                messages=[{
                    "role": "user",
                    "content": [{"type": "text", "text": prompt}]
                }],
                model=self.model,
                max_tokens=1000,
            )
            return response.content[0].text.strip()
        except Exception as e:
            raise Exception(f"Error: Failed to call Anthropic API. {str(e)}")
