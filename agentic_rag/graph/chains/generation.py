from langchain import hub
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import ChatOllama

llm = ChatOllama(model="qwen3", num_ctx=4096, temperature=0)
# llm = ChatOllama(model="llama3.2", num_ctx=4096)

prompt = hub.pull("rlm/rag-prompt")

generation_chain = prompt | llm | StrOutputParser()
