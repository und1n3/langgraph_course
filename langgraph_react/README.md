# Udemy course: LangGraph Develop LLM powered AI Agents


## Agent Executor
It will be the typical hello world of agents but implemented on LangGraph

- [PAPER: ReAct - Sytnergizing Reasoning and Acting in Language Models](https://arxiv.org/pdf/2210.03629)

The goal is to add reflexion in the RAG workflow and see if the answer is indeed based on the documents.

---
- [Github repo](https://github.com/emarco177/langgraph-course/tree/project/ReAct-agent)

---- 
### Project setup
If environment not created:

```
sudo apt install python3-poetry # or pip install poetry
poetry init
poetry add langchain langgraph langchain-ollama langchain-tavily langchainhub black isort python-dotenv
```
If an error raises for LangGraph: 
write this in the `pyproject.toml` file in python version ">=3.12,<4.0"

### Set the Python interpreter in VS Code

1. Open your project folder in VS Code.
2. Press Cmd+Shift+P (Mac) or Ctrl+Shift+P (Windows/Linux) to open the Command Palette.
3. Type Python: Select Interpreter and hit Enter.
4. Choose the interpreter that matches the path from poetry env info --path.

To activate poetry in the shell:
````
source $(poetry env info --path)/bin/activate  # macOS/Linux
````

### Expected .env file format:

```
OPENAI_API_KEY=...
TAVILY_API_KEY=...
LANGCHAIN_API_KEY=...
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=langgraph-react
```

We will also practice writing tests with pytest for LLMs.