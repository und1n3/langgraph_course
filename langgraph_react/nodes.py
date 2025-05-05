from dotenv import load_dotenv
from langgraph.prebuilt import ToolNode

from react import react_agent_runnable, tools
from state import AgentState

load_dotenv()
tool_executor = ToolNode(tools)


def run_agent_reasoning_engine(state: AgentState):
    agent_outcome = react_agent_runnable.invoke(state)
    return {
        "agent_outcome": agent_outcome
    }  # this will override the original agent outcome


def execute_tools(
    state: AgentState,
):  # hidden assumption, the agent always will have the "agent_outcome" field
    agent_action = state["agent_outcome"]

    ##ADDED CODE AS THE TAVILY SEARCH WAS NOT WORKING
    tool_name = agent_action.tool
    tool_input = agent_action.tool_input

    if tool_name == "tavily_search" and isinstance(tool_input, str):
        formatted_input = {"query": tool_input.strip()}
        print(f"Formated input: {formatted_input}")
        from react import tools

        for tool in tools:
            if tool.name == tool_name:
                output = tool.invoke(formatted_input)
                return {"intermediate_steps": [(agent_action, str(output))]}

    # ---
    output = tool_executor.invoke(agent_action)
    return {"intermediate_steps": [(agent_action, str(output))]}
