from typing import List
from .models import PromptSession, Example, LLMConfig
from .llm_providers import create_provider, BaseLLMProvider


class PromptBusterWorkflow:
    def __init__(self, llm_config: LLMConfig):
        self.llm_provider = create_provider(llm_config)
        self.session = PromptSession()
    
    async def generate_initial_prompt_guide(self, role: str) -> str:
        prompt = f"Generate a detailed prompt engineering guide. The audience is {role}."
        return await self.llm_provider.generate(prompt)
    
    async def generate_prompt_from_examples(self, role: str, examples: List[Example]) -> str:
        examples_text = "\n\n".join([
            f"Input: {ex.input_text}\nOutput: {ex.expected_output}"
            for ex in examples
        ])
        
        prompt = f"""I have these 5 examples of how I want my prompt to work for {role}:

{examples_text}

Generate a prompt that could have generated the examples' outputs, and include a better set of examples."""
        
        return await self.llm_provider.generate(prompt)
    
    async def generate_evaluation_guide(self, role: str) -> str:
        prompt = f"Generate a detailed prompt evaluation guide. The audience is {role}."
        return await self.llm_provider.generate(prompt)
    
    async def evaluate_prompt(self, prompt_to_evaluate: str, evaluation_guide: str) -> str:
        evaluation_prompt = f"""Using this evaluation guide:

{evaluation_guide}

Evaluate the following prompt:

{prompt_to_evaluate}"""
        
        return await self.llm_provider.generate(evaluation_prompt)
    
    async def generate_improved_alternatives(self, original_prompt: str, evaluation_result: str) -> List[str]:
        improvement_prompt = f"""Based on this evaluation:

{evaluation_result}

Generate 3 improved alternative prompts for the original prompt:

{original_prompt}

Format your response as:
1. [First alternative]
2. [Second alternative]  
3. [Third alternative]"""
        
        response = await self.llm_provider.generate(improvement_prompt)
        
        alternatives = []
        lines = response.split('\n')
        current_alternative = ""
        
        for line in lines:
            line = line.strip()
            if line.startswith(('1.', '2.', '3.')):
                if current_alternative:
                    alternatives.append(current_alternative.strip())
                current_alternative = line[2:].strip()
            elif current_alternative:
                current_alternative += " " + line
        
        if current_alternative:
            alternatives.append(current_alternative.strip())
        
        return alternatives[:3]
    
    def set_role(self, role: str):
        self.session.role = role
    
    def add_example(self, input_text: str, expected_output: str):
        self.session.examples.append(Example(input_text=input_text, expected_output=expected_output))
    
    def set_generated_prompt(self, prompt: str):
        self.session.generated_prompt = prompt
    
    def set_evaluation_guide(self, guide: str):
        self.session.evaluation_guide = guide
    
    def set_evaluation_result(self, result: str):
        self.session.evaluation_result = result
    
    def set_alternative_prompts(self, alternatives: List[str]):
        self.session.alternative_prompts = alternatives
    
    def set_final_prompt(self, prompt: str):
        self.session.final_prompt = prompt