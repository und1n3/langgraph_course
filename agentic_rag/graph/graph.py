from dotenv import load_dotenv

from langgraph.graph import END, StateGraph


from graph.chains.hallucination_grader import hallucination_grader
from graph.chains.answer_grader import answer_grader
from graph.chains.router import question_router, RouteQuery
from graph.consts import RETRIEVE, GENERATE, GRADE_DOCUMENTS, WEBSEARCH
from graph.nodes import generate, grade_documents, retrieve, web_search
from graph.state import GraphState

load_dotenv()


def decide_to_generate(state) -> str:
    print("--- ASSESS GRADED DOCUMENTS ---")
    if state["web_search"]:
        print("--- DECISION: NOT ALL DOCUMENTS ARE RELEVANT TO QUESTION")
        return WEBSEARCH
    else:
        print("--- DECISION: GENERATE ---")
        return GENERATE


def grade_generation_grounded_in_documents_and_question(state: GraphState) -> str:
    print("--- CHECK HALLUCINATIONS ---")
    question = state["question"]
    documents = state["documents"]
    generation = state["generation"]

    score = hallucination_grader.invoke(
        {"documents": documents, "generation": generation}
    )
    if hallucination_grade := score.binary_score:
        print("--- DECISION: GENERATION IS GROUNDED IN DOCUMENTS ---")
        print("--- GRADE GENERATION vs QUESTION ---")
        score = answer_grader.invoke({"question": question, "generation": generation})
        if answer_grade := score.binary_score:
            print("--- DECISION; GENERATION ADDRESSES QUESTION ---")
            return "useful"  # we'll map to end
        else:
            print("--- DECISION; GENERATION DOES NOT ADDRESS QUESTION ---")
            return "not useful"  # we'll need to search the web
    else:
        print("---DECISION: GENERATION IS NOT GROUNDED IN DOCUMENTS")
        return "not supported"  # we'll need to generate again from the documents


def route_question(state: GraphState) -> str:
    print("--- ROUTE QUESTION ---")
    question = state["question"]
    source: RouteQuery = question_router.invoke({"question": question})
    if source.datasource == WEBSEARCH:
        print("--- ROUTE QUESTION TO WEB SEARCH ---")
        return WEBSEARCH
    elif source.datasource == "vectorstore":
        print("--- ROUTE QUESTION TO RAG ---")
        return RETRIEVE


workflow = StateGraph(GraphState)
workflow.add_node(RETRIEVE, retrieve)
workflow.add_node(GRADE_DOCUMENTS, grade_documents)
workflow.add_node(GENERATE, generate)
workflow.add_node(WEBSEARCH, web_search)

# workflow.set_entry_point(RETRIEVE)
workflow.add_edge(RETRIEVE, GRADE_DOCUMENTS)

workflow.add_conditional_edges(
    GRADE_DOCUMENTS,  # origin
    decide_to_generate,  # function to decide
    {
        WEBSEARCH: WEBSEARCH,
        GENERATE: GENERATE,
    },  # path map. Useful when function not returning the node names
)

workflow.add_conditional_edges(
    GENERATE,
    grade_generation_grounded_in_documents_and_question,
    {"not supoorted": GENERATE, "useful": END, "not useful": WEBSEARCH},
)

workflow.set_conditional_entry_point(
    route_question, {WEBSEARCH: WEBSEARCH, RETRIEVE: RETRIEVE}
)


workflow.add_edge(WEBSEARCH, GENERATE)
workflow.add_edge(GENERATE, END)

app = workflow.compile()

app.get_graph().draw_mermaid_png(output_file_path="graph_self_rag.png")
