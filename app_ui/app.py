import streamlit as st
import weaviate
from weaviate.classes.query import MetadataQuery
import os
import cohere, os


co = cohere.Client(os.getenv("COHERE_API_KEY"))


def generate_query_from_prompt(prompt):
    response = co.chat(message=prompt, search_queries_only=True)
    return response.search_queries[0]["text"]


cluster_url = os.getenv("WORKSHOP_DEMO_URL")
cluster_key = os.getenv("WORKSHOP_DEMO_KEY_ADMIN")
COLLECTION_NAME = "Wikipedia"
MAIN_COLUMN = "title"
NAMED_VECTOR = "text_vector"
INIT_QUERY = "Albert Einstein"


GROUPED_TASK_INIT_PROMPT = "Describe how planes can fly, as you would to an 8-year old"
GROUPED_TASK_INIT_QUERY = "aerodynamics flight"
GROUPED_TASK_PROMPT_PREFIX = """
    Generate a response using the included information.
    If the provided text is insufficient, respond with
    'Sorry, the information provided is not enough.'
"""

SINGLE_PROMPT_INIT_PROMPT = "Turn this into a fun haiku: {title}"
SINGLE_PROMPT_INIT_QUERY = "aerodynamics flight"


if "grouped_task_output" not in st.session_state:
    st.session_state.grouped_task_output = (
        "Please click the button to generate a response."
    )

if "single_prompt_output" not in st.session_state:
    st.session_state.single_prompt_output = [
        {"data": "Please click the button to generate a response.", "generated": ""}
    ]

if "gen_search_results" not in st.session_state:
    st.session_state.gen_search_results = []

if "rag_search_type" not in st.session_state:
    st.session_state.rag_search_type = "hybrid"


def generate_grouped_task():
    search_type = st.session_state.rag_search_type
    if search_type == "neartext":
        grouped_response = collection.generate.near_text(
            query=gt_rag_query_str,
            limit=rag_limit,
            target_vector=NAMED_VECTOR,
            return_metadata=MetadataQuery(distance=True),
            grouped_task=grouped_task,
        )
    elif search_type == "keyword":
        grouped_response = collection.generate.bm25(
            query=gt_rag_query_str,
            limit=rag_limit,
            return_metadata=MetadataQuery(score=True),
            grouped_task=grouped_task,
        )
    else:
        grouped_response = collection.generate.hybrid(
            query=gt_rag_query_str,
            limit=rag_limit,
            alpha=alpha,
            target_vector=NAMED_VECTOR,
            return_metadata=MetadataQuery(score=True),
            grouped_task=grouped_task,
        )

    st.session_state.grouped_task_output = grouped_response.generated
    st.session_state.gen_search_results = [
        grouped_response.objects
    ]
    return True


def generate_single_prompt():
    if search_type == "neartext":
        single_response = collection.generate.near_text(
            query=sp_rag_query_str,
            limit=rag_limit,
            target_vector=NAMED_VECTOR,
            return_metadata=MetadataQuery(distance=True),
            single_prompt=single_prompt,
        )
    elif search_type == "keyword":
        single_response = collection.generate.bm25(
            query=sp_rag_query_str,
            limit=rag_limit,
            return_metadata=MetadataQuery(score=True),
            single_prompt=single_prompt,
        )
    else:
        single_response = collection.generate.hybrid(
            query=sp_rag_query_str,
            limit=rag_limit,
            alpha=alpha,
            target_vector=NAMED_VECTOR,
            return_metadata=MetadataQuery(score=True),
            single_prompt=single_prompt,
        )
    single_prompt_responses = [
        {"data": o.properties[MAIN_COLUMN], "generated": o.generated}
        for o in single_response.objects
    ]
    st.session_state.single_prompt_output = single_prompt_responses
    st.session_state.gen_search_results = [
        single_response.objects
    ]
    return True


headers = {
    "X-OpenAI-Api-Key": os.getenv(
        "OPENAI_API_KEY"
    ),  # Replace with your inference API key
    "X-Cohere-Api-Key": os.getenv(
        "COHERE_API_KEY"
    ),  # Replace with your inference API key
}


if cluster_url is None or cluster_key is None:
    client = None
else:
    client = weaviate.connect_to_wcs(
        cluster_url=cluster_url,
        auth_credentials=weaviate.auth.AuthApiKey(cluster_key),
        headers=headers,
    )


# Main app
if client is None:
    st.write("No Weaviate client found. Check connection details.")
else:
    st.header("Weaviate Search and RAG Demo")
    st.subheader("Inputs")

    collection = client.collections.get(COLLECTION_NAME)

    search_tab, rag_tab = st.tabs(["Search", "RAG"])

    with search_tab:
        with st.container(height=200):
            query_str = st.text_input(
                label="Query string", value=INIT_QUERY, key="query_str"
            )
            limit = st.number_input(label="Limit", value=5, key="limit")

        def show_response(response):
            with st.container(height=300):
                for i, obj in enumerate(response.objects):
                    with st.expander(f"{obj.properties[MAIN_COLUMN]}"):
                        st.subheader(f"Object:")
                        st.write(obj.properties)
                        st.subheader(f"Distance:")
                        st.write(obj.metadata.distance)

        st.subheader("Search results")
        neartext, keyword, hybrid = st.tabs(["NearText", "Keyword", "Hybrid"])
        with neartext:
            neartext_response = collection.query.near_text(
                query=query_str,
                limit=limit,
                target_vector=NAMED_VECTOR,
                return_metadata=MetadataQuery(distance=True),
            )
            show_response(neartext_response)
        with keyword:
            keyword_response = collection.query.bm25(
                query=query_str,
                limit=limit,
                return_metadata=MetadataQuery(score=True),
            )
            show_response(keyword_response)
        with hybrid:
            alpha = st.slider("Alpha", 0.0, 1.0, 0.5, 0.1, key="hybrid_alpha")
            hybrid_response = collection.query.hybrid(
                query=query_str,
                limit=limit,
                alpha=alpha,
                target_vector=NAMED_VECTOR,
                return_metadata=MetadataQuery(score=True),
            )
            show_response(hybrid_response)

    with rag_tab:
        st.subheader("Retrieval augmented generation (RAG)")
        st.write("**Inputs**")

        grouped_task_tab, single_prompt_tab = st.tabs(["Grouped task", "Single prompt"])

        with grouped_task_tab:
            with st.container(border=True):
                search_type = st.radio(
                    "Search type",
                    options=["neartext", "keyword", "hybrid"],
                    horizontal=True,
                    key="rag_search_type_grouped",
                )
                if search_type == "hybrid":
                    alpha = st.slider("Alpha", 0.0, 1.0, 0.5, 0.1, key="rag_hybrid_alpha_gt")
                st.session_state.rag_search_type = search_type

                grouped_task_input = st.text_area(
                    label="Grouped task",
                    value=GROUPED_TASK_INIT_PROMPT,
                    key="grouped_task",
                    height=60,
                )
                grouped_task = GROUPED_TASK_PROMPT_PREFIX + " " + grouped_task_input

                query_method_col, query_str_col = st.columns([1, 2])
                with query_method_col:
                    query_method = st.selectbox(
                        options=["Manual", "From prompt"],
                        index=1,
                        label="Query method",
                        key="query_method",
                    )
                with query_str_col:
                    if query_method == "From prompt":
                        gt_rag_query_str = generate_query_from_prompt(grouped_task)
                        st.write(f"Generated query")
                        with st.container():
                            st.text(gt_rag_query_str)
                    else:
                        gt_rag_query_str = st.text_input(
                            label="Query string", value=GROUPED_TASK_INIT_QUERY, key="rag_query_str"
                        )
                rag_limit = st.number_input(label="Limit", value=5, key="rag_limit")

            st.button(
                "Generate response",
                key="generate_grouped_task",
                on_click=generate_grouped_task,
            )
            st.write("**Outputs**")
            with st.container(height=200):
                st.write(st.session_state.grouped_task_output)
            with st.expander("Search results"):
                for j, search_result in enumerate(st.session_state.gen_search_results):
                    st.write(search_result)


        with single_prompt_tab:
            with st.container(border=True):
                search_type = st.radio(
                    "Search type",
                    options=["neartext", "keyword", "hybrid"],
                    horizontal=True,
                    key="rag_search_type_single",
                )
                if search_type == "hybrid":
                    alpha = st.slider("Alpha", 0.0, 1.0, 0.5, 0.1, key="rag_hybrid_alpha_sp")
                st.session_state.rag_search_type = search_type

                single_prompt = st.text_area(
                    label="Single prompt",
                    value=SINGLE_PROMPT_INIT_PROMPT,
                    key="single_prompt",
                    height=60,
                )
                sp_rag_query_str = st.text_input(
                    label="Query string", value=SINGLE_PROMPT_INIT_QUERY, key="sp_rag_query_str"
                )

            st.button(
                "Generate response",
                key="generate_single_prompt",
                on_click=generate_single_prompt,
            )
            st.write("**Outputs**")
            with st.container(height=200):
                for i, rag_obj in enumerate(st.session_state.single_prompt_output):
                    st.caption(rag_obj["data"])
                    st.write(rag_obj["generated"])
            with st.expander("Search results"):
                for j, search_result in enumerate(st.session_state.gen_search_results):
                    st.write(search_result)
