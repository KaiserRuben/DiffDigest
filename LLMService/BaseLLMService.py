# BaseLLMService.py
from abc import ABC, abstractmethod
from typing import Dict


class BaseLLMService(ABC):
    @abstractmethod
    def get_model_name(self) -> str:
        pass

    @abstractmethod
    def get_url(self) -> str:
        pass

    @abstractmethod
    def generate(self, prompt: str) -> str:
        pass
