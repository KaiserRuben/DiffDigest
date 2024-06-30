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

    def generate(self, prompt: str) -> Dict[str, str]:
        try:
            response = self.client.completions.create(
                prompt=prompt,
                model=self.model,
                max_tokens_to_sample=100,
            )
            return {"response": response.completion.strip()}
        except Exception as e:
            raise Exception(f"Error: Failed to call Anthropic API. {str(e)}")
