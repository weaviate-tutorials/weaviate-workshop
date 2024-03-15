import streamlit as st
import weaviate
from weaviate.classes.query import MetadataQuery
import os


headers = {
    "X-OpenAI-Api-Key": os.getenv(
        "OPENAI_API_KEY"
    ),  # Replace with your inference API key
    "X-Cohere-Api-Key": os.getenv(
        "COHERE_API_KEY"
    ),  # Replace with your inference API key
}

conn_type = st.selectbox(
    "Weaviate connection type", options=["WCS", "Local"], index=0
)
if conn_type == "WCS":
    client_url = os.getenv("WORKSHOP_DEMO_URL")
    client_key = os.getenv("WORKSHOP_DEMO_KEY_ADMIN")
    if client_url is None or client_key is None:
        client = None
    else:
        client = weaviate.connect_to_wcs(
            cluster_url=os.getenv("WORKSHOP_DEMO_URL"),
            auth_credentials=weaviate.auth.AuthApiKey(os.getenv("WORKSHOP_DEMO_KEY_ADMIN")),
            headers=headers,
        )
else:
    client = weaviate.connect_to_local(
        headers=headers
    )

# Main app
if client is None:
    st.write("No Weaviate client found. Check connection details.")
else:
    st.header("Weaviate Search and RAG Demo")
    st.subheader("Inputs")

    collection = client.collections.get("Wikipedia")
    main_column = "title"

    with st.container(height=200):
        query_str = st.text_input(
            label="Query string", value="how do planes fly", key="query_str"
        )
        limit = st.number_input(label="Limit", value=7, key="limit")

    return_metadata = MetadataQuery(distance=True)

    neartext_response = collection.query.near_text(
        query=query_str, limit=limit, return_metadata=return_metadata
    )

    keyword_response = collection.query.bm25(
        query=query_str, limit=limit, return_metadata=return_metadata
    )

    hybrid_response = collection.query.near_text(
        query=query_str, limit=limit, return_metadata=return_metadata
    )

    def show_response(response):
        with st.container(height=200):
            for i, obj in enumerate(response.objects):
                with st.expander(f"{obj.properties[main_column]}"):
                    st.subheader(f"Object:")
                    st.write(obj.properties)
                    st.subheader(f"Distance:")
                    st.write(obj.metadata.distance)

    st.subheader("Search results")
    neartext, keyword, hybrid = st.tabs(["NearText", "Keyword", "Hybrid"])
    with neartext:
        show_response(neartext_response)
    with keyword:
        show_response(keyword_response)
    with hybrid:
        show_response(hybrid_response)

    st.subheader("Retrieval augmented generation (RAG)")
    st.write("**Inputs**")

    with st.container(height=200):
        single_prompt = st.text_input(
            label="Single prompt",
            value="Turn this into a fun haiku: {" + main_column + "}",
            key="single_prompt",
        )
        grouped_task = st.text_input(
            label="Grouped task", value="Summarize these results.", key="grouped_task"
        )

    # Perform RAG
    rag_response = collection.generate.near_text(
        query=query_str,
        limit=limit,
        single_prompt=single_prompt,
        grouped_task=grouped_task,
        return_metadata=return_metadata,
    )

    # Object details tab
    st.write("**Outputs**")
    single_prompt_output, grouped_task_output = st.tabs(
        ["Single prompt", "Grouped task"]
    )
    with single_prompt_output:
        with st.container(height=200):
            for i, rag_obj in enumerate(rag_response.objects):
                st.caption(f"{rag_obj.properties[main_column]}:")
                st.write(rag_obj.generated)
    with grouped_task_output:
        with st.container(height=200):
            st.write(rag_response.generated)
