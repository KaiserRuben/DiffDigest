# config.py
import os

from LLMService.OLLAMAService import OLLAMAService
from LLMService.OpenAIService import OpenAIService
from LLMService.AnthropicService import AnthropicService

OLLAMA_URL = "http://localhost:11434"
OLLAMA_MODEL = "llama3:instruct"

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = "gpt-4o"

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
ANTHROPIC_MODEL = "claude-3-5-sonnet-20240620"

# Choose the desired LLM service
# LLM_SERVICE = OLLAMAService(OLLAMA_URL, OLLAMA_MODEL)
# LLM_SERVICE = OpenAIService(OPENAI_API_KEY, OPENAI_MODEL)
LLM_SERVICE = AnthropicService(ANTHROPIC_API_KEY, ANTHROPIC_MODEL)


# The maximum number of old commits taken into account for the analysis (default: 10)
MAX_COMMITS = 50
