from typing import List, Optional

from pydantic import BaseModel, Field


class Reflection(BaseModel):
    missing: str = Field(
        description="Describe what is missing in the initial answer . Be thorough, surely something could be improved."
    )
    superfluous: str = Field(
        description="Detail of what is **superfluous** in the initial answer . Be thorough, surely something could be improved"
    )


class AnswerQuestion(BaseModel):
    """Answer the question."""

    answer: str = Field(description="~250 word detailed answer to the question.")
    reflection: Reflection = Field(
        description="Your reflection on the initial answer, providing whats 'missing' and whats 'superfluous' info."
    )
    search_queries: List[str] = Field(
        description="1-3 search queries for researching improvements to address the critique of your current answer."
    )


class ReviseAnswer(AnswerQuestion):
    """Revise your original answer to your question."""

    references: List[str] = Field(
        description="Citations motivating your updated answer. Write the correct url, with existing data you obtained from the search"
    )
