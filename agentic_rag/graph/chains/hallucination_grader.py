from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from langchain_core.runnables import RunnableSequence
from langchain_ollama import ChatOllama

llm = ChatOllama(model="qwen3", num_ctx=4096, temperature=0)


class GradeHallucinations(BaseModel):
    """Binary score for hallucination prsent in generation answer."""

    binary_score: bool = Field(
        description="Answwer is grounded in the facts 'yes' or 'no'"
    )


structured_llm_grader = llm.with_structured_output(GradeHallucinations)

system = """You are a grader assewssing whether an LLM generatiion is grounded in / supported by a set of retrieved facts.
Give a binary score 'yes' or 'no'. 'Yes' means that the answer is gfrounded in / supoorted by the set of facts"""

hallucination_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        ("human", "Set of facts \n\n {documents} \n\n LLm generation: {generation}"),
    ]
)


hallucination_grader: RunnableSequence = hallucination_prompt | structured_llm_grader
