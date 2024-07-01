from LLMService.LLMServiceStrategy import LLMServiceStrategy
from config import LLM_SERVICE


def call_api(prompt):
    llm_strategy = LLMServiceStrategy(LLM_SERVICE)
    response = llm_strategy.generate(prompt)
    return response.strip()

