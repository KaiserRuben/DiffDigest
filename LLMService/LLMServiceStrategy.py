# LLMServiceStrategy.py
from typing import Dict

from LLMService.BaseLLMService import BaseLLMService

class LLMServiceStrategy:
    def __init__(self, llm_service: BaseLLMService):
        self.llm_service = llm_service

    def generate(self, prompt: str) -> str:
        return self.llm_service.generate(prompt)

    def get_url(self) -> str:
        return self.llm_service.get_url()