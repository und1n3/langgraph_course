# Udemy course: LangGraph Develop LLM powered AI Agents



## Agentic RAG
- Based on the Langchain/Mistral Cookbook but refactored.
- [PAPER: Self-RAG Learning to Retrieve Generate and Critique though self-reflection](https://arxiv.org/pdf/2310.11511)
- [PAPER: Corrective Retrieval Augmented Generation](https://arxiv.org/pdf/2401.15884)
- [PAPER: Adaptive-RAG Learning to Adapt Retrieval augmented LLLM through Question Complexity](https://arxiv.org/pdf/2403.14403)

The goal is to add reflexion in the RAG workflow and see if the answer is indeed based on the documents.

---
- [Github repo](https://github.com/emarco177/langgraph-course)

- [Mistral YT video](https://www.youtube.com/watch?v=sgnrL7yo1TE)
- [Cookbook](https://github.com/mistralai/cookbook/tree/main/third_party/langchain)
---- 
### Project setup
If environment not created:

```
sudo apt install python3-poetry # or pip install poetry
poetry init
poetry add python-dotenv black isort pytest langchain-openai langchain-ollama langgraph langchain chromadb langchainhub tiktoken langchain-community beautifulsoup4
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
LANGCHAIN_PROJECT=reflexion-agent
```

We will also practice writing tests with pytest for LLMs.