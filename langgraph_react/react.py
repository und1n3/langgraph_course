from dotenv import load_dotenv
from langchain import hub
from langchain.agents import create_react_agent
from langchain_tavily import TavilySearch
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import tool
from langchain_ollama import ChatOllama

load_dotenv()

react_prompt: PromptTemplate = hub.pull("hwchase17/react")


@tool
def triple(num: float) -> float:
    """
    :param num: a number to triple.
    :return: the number mutiplied by 3
    """
    return 3 * float(num)


tools = [TavilySearch(max_results=1), triple]

llm = ChatOllama(model="qwen3", num_ctx=4096)
react_agent_runnable = create_react_agent(llm, tools, react_prompt)
