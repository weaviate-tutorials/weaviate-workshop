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

with st.expander("Weaviate connection details"):
    conn_type = st.selectbox(
        "Weaviate connection type", options=["WCS", "Local"], index=0
    )
    if conn_type == "WCS":
        use_env_vars = st.checkbox("Use environment variable keys", value=True)
        if use_env_vars:
            url_envvar = st.text_input(
                label="Environment key for the URL",
                key="url_env_var",
                value="WORKSHOP_DEMO_URL",
            )
            key_envvar = st.text_input(
                label="Environment key for the API key",
                key="key_env_var",
                value="WORKSHOP_DEMO_KEY_ADMIN",
            )
            cluster_url = os.getenv(url_envvar)
            cluster_key = os.getenv(key_envvar)
        else:
            cluster_url = st.text_input(
                label="URL", key="cluster_url", value="YOUR_CLUSTER_URL"
            )
            cluster_key = st.text_input(
                label="API key", key="cluster_key", value="YOUR_CLUSTER_API_KEY"
            )

        # Connect to Weaviate
        try:
            client = weaviate.connect_to_wcs(
                cluster_url=cluster_url,
                auth_credentials=weaviate.auth.AuthApiKey(cluster_key),
                headers=headers,
            )
        except Exception as e:
            client = None
            st.error(f"Error connecting to Weaviate: {e}")
    else:
        try:
            client = weaviate.connect_to_local(headers=headers)
        except Exception as e:
            client = None
            st.error(f"Error connecting to Weaviate: {e}")


# Main app
if client is not None:
    st.header("Weaviate Search and RAG Demo")
    st.subheader("Inputs")

    input_l, input_r = st.columns(2, gap="small")

    with input_l:
        with st.container(height=200):
            collections = client.collections.list_all(simple=True)
            collection_name = st.selectbox(
                label="Collection name",
                options=[c for c in sorted(collections.keys())],
                key="collection_name",
                index=0,
            )
            collection = client.collections.get(collection_name)
            random_object = collection.query.fetch_objects(limit=1)
            property_names = sorted(random_object.objects[0].properties.keys())
            main_column = st.selectbox(
                label="Summary column",
                options=[p for p in property_names],
                key="summary_column",
                index=0,
            )
    with input_r:
        with st.container(height=200):
            query_str = st.text_input(
                label="Query string", value="fashion sneakers", key="query_str"
            )
            limit = st.number_input(label="Limit", value=10, key="limit")

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
