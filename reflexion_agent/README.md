# Udemy course: LangGraph Develop LLM powered AI Agents

- [Github repo](https://github.com/emarco177/reflexion)

## Reflection Agent with tools
- [PAPER: Reflexion. Language Agents with Verbal Reinforcement Learning](https://arxiv.org/pdf/2303.11366)
- [LangChain Blog: Reflexion Agents](https://blog.langchain.dev/reflection-agents/)
- [Tavily: Search engine optimized for LLMs](https://tavily.com/)


The goal of the reflection agent is to give us a very detailed article about the topic we give. We want it to search the web and give citatiosn with a high quality answer.

### Project setup
If environment not created:

```
sudo apt install python3-poetry # or pip install poetry
poetry init
poetry add python-dotenv black isort langchain langchain-ollama langchain-openai langgraph
```

Expected .env file format:

```
OPENAI_API_KEY=...
TAVILY_API_KEY=...
LANGCHAIN_API_KEY=...
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=reflexion-agent
```