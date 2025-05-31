from pydantic import BaseModel
from typing import List, Optional
from enum import Enum


class WorkflowStep(Enum):
    INITIAL_PROMPT = "initial_prompt"
    EXAMPLES_INPUT = "examples_input"
    PROMPT_GENERATION = "prompt_generation"
    EVALUATION_GUIDE = "evaluation_guide"
    PROMPT_EVALUATION = "prompt_evaluation"
    IMPROVED_ALTERNATIVES = "improved_alternatives"
    FINAL_SELECTION = "final_selection"


class Example(BaseModel):
    input_text: str
    expected_output: str


class PromptSession(BaseModel):
    role: str = ""
    examples: List[Example] = []
    generated_prompt: str = ""
    evaluation_guide: str = ""
    evaluation_result: str = ""
    alternative_prompts: List[str] = []
    final_prompt: str = ""
    current_step: WorkflowStep = WorkflowStep.INITIAL_PROMPT


class LLMProvider(Enum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    LOCAL = "local"


class LLMConfig(BaseModel):
    provider: LLMProvider
    model: str
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    temperature: float = 0.7
    max_tokens: int = 4000