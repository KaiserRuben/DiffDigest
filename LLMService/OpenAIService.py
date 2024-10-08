# OpenAIService.py
import openai
from typing import Dict

from LLMService.BaseLLMService import BaseLLMService


class OpenAIService(BaseLLMService):
    def __init__(self, api_key: str, model: str):
        openai.api_key = api_key
        self.model = model

    def get_model_name(self) -> str:
        return self.model

    def get_url(self) -> str:
        return "-"

    def generate(self, prompt: str) -> str:
        try:
            response = openai.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "user",
                     "content": prompt}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"Error: Failed to call OpenAI API. {str(e)}")
