import operator
from typing import Annotated, TypedDict, Union

from langchain_core.agents import AgentAction, AgentFinish


class AgentState(TypedDict):
    input: str
    agent_outcome: Union[
        AgentAction,
        AgentFinish,
        None,  # None also because when we run the first node we dont have anything in the state yet.
    ]
    intermediate_steps: Annotated[
        list[
            tuple[AgentAction, str]
        ],  # first element is element action and the output of that action (str)
        operator.add,  # keep adding to this list of intermediate states the new state
    ]
