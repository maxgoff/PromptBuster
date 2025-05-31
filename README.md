# PromptBuster

A Python GUI tool for systematically improving prompts using LLM feedback. PromptBuster implements a 7-step workflow that leverages the LLM's own weights to generate better prompts than you could write manually.

## Features

- **7-Step Workflow**: Guided process for prompt improvement
- **Multiple LLM Providers**: Support for OpenAI, Anthropic, and local models
- **Modern GUI**: Clean Tkinter interface with CustomTkinter
- **Configuration Management**: Save/load settings and sessions
- **Async Processing**: Non-blocking LLM requests

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd PromptBuster
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys
```

## Usage

1. Run the application:
```bash
python main.py
```

2. Configure your LLM provider in the left panel
3. Follow the 7-step workflow:
   - **Step 1**: Define your target role and generate initial prompt guide
   - **Step 2**: Input 5 examples of desired input/output behavior
   - **Step 3**: Generate a prompt from your examples
   - **Step 4**: Generate an evaluation guide for your role
   - **Step 5**: Evaluate the generated prompt
   - **Step 6**: Generate 3 improved alternatives
   - **Step 7**: Select and edit your final prompt

## The 7-Step Workflow

1. **Initial Prompt Guide**: Generate a detailed prompt engineering guide for your target audience
2. **Examples Input**: Provide 5 examples of how you want your prompt to work
3. **Prompt Generation**: Generate a prompt that could produce your examples' outputs
4. **Evaluation Guide**: Generate a detailed prompt evaluation guide
5. **Prompt Evaluation**: Evaluate the generated prompt using the evaluation guide
6. **Improved Alternatives**: Generate 3 improved alternative prompts
7. **Final Selection**: Select and edit your final prompt

## Supported LLM Providers

- **OpenAI**: GPT-4, GPT-3.5-turbo, etc.
- **Anthropic**: Claude-3 models
- **Local**: Any OpenAI-compatible API endpoint

## Configuration

Set your API keys in environment variables:
- `OPENAI_API_KEY`: For OpenAI models
- `ANTHROPIC_API_KEY`: For Anthropic models

Or configure them directly in the GUI.

## Benefits

- **Better than manual**: LLM's own weights influence prompt generation
- **Systematic**: Follows a proven 7-step methodology
- **Family-optimized**: Best results when using the same model family for generation and final use
- **Iterative**: Each step builds on the previous to improve quality

## Requirements

- Python 3.8+
- See `requirements.txt` for full dependency list

## License

See LICENSE file for details.
