import datetime

from dotenv import load_dotenv

load_dotenv()

from langchain_core.messages import HumanMessage
from langchain_core.output_parsers.openai_tools import (
    JsonOutputToolsParser,
    PydanticToolsParser,
)
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI

from schemas import AnswerQuestion, ReviseAnswer

# llm = ChatOpenAI(model="gpt-3.5-turbo-1106")
llm = ChatOllama(model="qwen3")
parser = JsonOutputToolsParser(return_id=True)
parser_pydantic = PydanticToolsParser(tools=[AnswerQuestion])


actor_prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are an expert researcher. Provide an answer in the expected format: 
                - answer 
                - reflection: 
                    - missing
                    - superfluous
                - search_queries
            Current time: {time}
            
            1. {first_instruction}
            2. Reflect and critique your anser. Be severe to maximize improvement.
            3. Recommend search queries to research information and improve your answer.""",
        ),
        MessagesPlaceholder(variable_name="messages"),
        ("system", "Answer the user's question above using the required format."),
    ]
).partial(
    # in order to populate the placeholders defined in the prompt that we already know
    time=lambda: datetime.datetime.now().isoformat(),
)


first_responder_prompt_template = actor_prompt_template.partial(
    first_instruction="Provide a detailed ~250 word answer."
)

first_responder = first_responder_prompt_template | llm.bind_tools(
    tools=[AnswerQuestion], tool_choice="AnswerQuestion"
)

revise_instructions = """Revise your previous answer using the new informations.
    - You should use the previous critique to add important information to your anser.
        - You MUST include numerical citations in your revised answer to ensure it can be verified.
        - Add a "References" section to the bottom of your answer (which does not count towards the word limit). DO NOT MAKE UP THE URLS USE EXACTLY THE PROVIDED DATA from the available tools.In the following form using the urls for the corresponding references where you extracted the data from:
            - [1] https://
            - [2] https://
            - [3] https://
        - You should use the previous critique to remove superfluous information from your answer and make SURE it is not more than 250 words
    """

revisor = actor_prompt_template.partial(
    first_instruction=revise_instructions
) | llm.bind_tools(tools=[ReviseAnswer], tool_choice="ReviseAnswer")

if __name__ == "__main__":
    human_message = HumanMessage(
        content="write about AI-Powered SOC / autonomous soc problem domain, list startups that do that and raised capital."
    )
    chain = (
        first_responder_prompt_template
        | llm.bind_tools(tools=[AnswerQuestion], tool_choice="AnswerQuestion")
        | parser_pydantic
    )
    # res_1 = first_responder.invoke(input={"messages": [human_message]})
    # print(res_1)

    res = chain.invoke(input={"messages": [human_message]})

    # print(res)
    print("--- Answer ---\n")
    print(res[0].answer)
    print("\n--- Reflection ---\n")
    print("Missing: ")
    print(res[0].reflection.missing)
    print("\nSuperfluous:")
    print(res[0].reflection.superfluous)
    print("\n--- Search queries ---\n")
    print(res[0].search_queries)
