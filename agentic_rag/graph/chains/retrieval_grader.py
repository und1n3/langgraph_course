from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from pydantic import BaseModel, Field

llm = ChatOllama(model="qwen3", num_ctx=4096, temperature=0)
# llm = ChatOllama(model="llama3.2", num_ctx=4096)


class GradeDocuments(BaseModel):
    """
    Boolean score for relevance check on retrieved documents.
    """

    binary_score: bool = Field(
        description="Boolean answer . Grade it as True if the question is related to the documents, else grade it as False. "
    )


structured_llm_grader = llm.with_structured_output(GradeDocuments)

system = """ You are a grader assessing relevance of a retrieved document to a user questions.
If the document contains keyword(s) or semantic meaning related to the question you must grade it as a boolen answer True/False """

grade_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        ("human", "Retrieved document: \n\n {document} \n\n User question: {question}"),
    ]
)

retrieval_grader = grade_prompt | structured_llm_grader
