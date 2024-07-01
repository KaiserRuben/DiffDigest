import requests

import config

from LLMService.LLMServiceStrategy import LLMServiceStrategy
from config import LLM_SERVICE


def call_api(prompt):
    llm_strategy = LLMServiceStrategy(LLM_SERVICE)
    try:
        response = llm_strategy.generate(prompt)
        return response.strip()
    except requests.RequestException as e:
        raise Exception(f"Error: Failed to call API. {str(e)}")
