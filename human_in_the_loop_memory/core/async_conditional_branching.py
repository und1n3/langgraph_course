from dotenv import load_dotenv

load_dotenv()

import operator
from typing import Annotated, Any, Sequence
from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START, END


class State(TypedDict):
    aggregate: Annotated[list, operator.add]
    which: str


class ReturnNodeValue:
    def __init__(self, node_secret: str):
        self._value = node_secret

    def __call__(self, state: State) -> Any:
        print(f"Adding {self._value} to {state['aggregate']}")
        return {"aggregate": [self._value]}


builder = StateGraph(State)
builder.add_node("a", ReturnNodeValue("I'm A"))
builder.add_edge(START, "a")
builder.add_node("b", ReturnNodeValue("I'm B"))
builder.add_node("c", ReturnNodeValue("I'm C"))
builder.add_node("d", ReturnNodeValue("I'm D"))
builder.add_node("e", ReturnNodeValue("I'm E"))


def route_bc_or_cd(state: State) -> Sequence[str]:
    # which nodes to run concurrently
    if state["which"] == "cd":
        return ["c", "d"]
    return ["b", "c"]


intermediates = ["b", "c", "d"]

builder.add_conditional_edges(
    "a",
    route_bc_or_cd,
    path_map=intermediates,  # helps with the visualization of the graph
)
for node in intermediates:
    builder.add_edge(node, "e")

builder.add_edge("e", END)

graph = builder.compile()
graph.get_graph().draw_mermaid_png(
    output_file_path="async_graph_conditional_branching.png"
)

if __name__ == "__main__":
    print("Running Async Graph")
    graph.invoke(
        {"aggregate": [], "which": "cd"}, {"configurable": {"thread_id": "foo"}}
    )
