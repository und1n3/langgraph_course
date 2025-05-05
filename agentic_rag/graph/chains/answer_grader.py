from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from langchain_core.runnables import RunnableSequence
from langchain_ollama import ChatOllama

llm = ChatOllama(model="qwen3", num_ctx=4096, temperature=0)


class GradeAnswer(BaseModel):
    binary_score: bool = Field(
        description="answer addresses the question 'yes' or 'no' "
    )


structured_llm_grader = llm.with_structured_output(GradeAnswer)


system = """ You are a grader assessing whether an answer addresses / resolves a question \n 
Give a binary score 'yes' or 'no'. 'Yes' means that the answer resolves the question."""

answer_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        ("human", "User question: \n\n {question} \n\n LLM generation: {generation}"),
    ]
)

answer_grader: RunnableSequence = answer_prompt | structured_llm_grader
