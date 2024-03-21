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




if "grouped_task_output" not in st.session_state:
    st.session_state.grouped_task_output = (
        "Please click the button to generate a response."
    )

if "single_prompt_output" not in st.session_state:
    st.session_state.single_prompt_output = [
        {"data": "Please click the button to generate a response.", "generated": ""}
    ]


def generate_grouped_task():
    grouped_response = collection.generate.near_text(
        query=gt_rag_query_str,
        limit=rag_limit,
        grouped_task=grouped_task,
        return_metadata=MetadataQuery(score=True),
    )

    st.session_state.grouped_task_output = grouped_response.generated
    return True


def generate_single_prompt():
    single_response = collection.generate.near_text(
        query=sp_rag_query_str,
        limit=rag_limit,
        single_prompt=single_prompt,
        return_metadata=MetadataQuery(score=True),
    )
    single_prompt_responses = [
        {"data": o.properties[MAIN_COLUMN], "generated": o.generated}
        for o in single_response.objects
    ]
    st.session_state.single_prompt_output = single_prompt_responses
    return True


headers = {
    "X-OpenAI-Api-Key": os.getenv(
        "OPENAI_API_KEY"
    ),  # Replace with your inference API key
    "X-Cohere-Api-Key": os.getenv(
        "COHERE_API_KEY"
    ),  # Replace with your inference API key
}

conn_type = st.selectbox("Weaviate connection type", options=["WCS", "Local"], index=0)
if conn_type == "WCS":
    if cluster_url is None or cluster_key is None:
        client = None
    else:
        client = weaviate.connect_to_wcs(
            cluster_url=cluster_url,
            auth_credentials=weaviate.auth.AuthApiKey(cluster_key),
            headers=headers,
        )
else:
    client = weaviate.connect_to_local(headers=headers)

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
            alpha = st.slider("Alpha", 0.0, 1.0, 0.5, 0.1)
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
            with st.container():
                grouped_task = st.text_area(
                    label="Grouped task",
                    value="Describe how airplanes fly, like you would to an 8 year old.",
                    key="grouped_task",
                    height=60,
                )
                query_method_col, query_str_col = st.columns([1, 2])
                with query_method_col:
                    query_method = st.selectbox(
                        options=["Manual", "From prompt"],
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
                            label="Query string", value=INIT_QUERY, key="rag_query_str"
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

        with single_prompt_tab:
            single_prompt = st.text_area(
                label="Single prompt",
                value="Turn this into a fun haiku: {" + MAIN_COLUMN + "}",
                key="single_prompt",
                height=60,
            )
            sp_rag_query_str = st.text_input(
                label="Query string", value=INIT_QUERY, key="sp_rag_query_str"
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
