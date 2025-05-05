from typing import Literal

from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from langchain_ollama import ChatOllama


class RouteQuery(BaseModel):
    """Route a user query to the most relevant datasource."""

    datasource: Literal["vectorstore", "websearch"] = Field(
        ...,  # elipsis: this field will be required once we instantiate an object of this class
        description="Given a user question choose to route it to web search or a vectorstore.",
    )


llm = ChatOllama(model="qwen3", num_ctx=4096, temperature=0)
structured_llm_router = llm.with_structured_output(RouteQuery)

system = """You are an expert at routing a user question to a vectorstore or web search.,
The vectorstore contains documents related to agents, prompt engineering, and adversarial attacks.
Use the vectorstore for questionson these topics. For all else, use web-search."""

route_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        ("human", "{question}"),
    ]
)

question_router = route_prompt | structured_llm_router
