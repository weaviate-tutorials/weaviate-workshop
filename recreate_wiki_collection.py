#!/usr/bin/env python3
"""
Script to recreate Wiki collection with nomic-embed-text and export to parquet
"""

import os
import pandas as pd
import weaviate
from weaviate.classes.init import Auth
from weaviate.classes.config import Configure
from datasets import load_dataset
from tqdm import tqdm
from dotenv import load_dotenv
from weaviate.util import generate_uuid5

# Load environment variables
load_dotenv()

WEAVIATE_KEY = os.getenv("WEAVIATE_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_URL = os.getenv("OPENAI_URL")

def connect_to_weaviate():
    """Connect to Weaviate"""
    client = weaviate.connect_to_local(
        host="localhost",
        port=8080,
        grpc_port=50051,
        auth_credentials=Auth.api_key(WEAVIATE_KEY),
        headers={
            "X-OpenAI-Api-Key": OPENAI_API_KEY,
            "X-OpenAI-BaseURL": OPENAI_URL
        }
    )
    return client

def recreate_collection(client):
    """Delete and recreate Wiki collection with nomic-embed-text"""
    print("Deleting existing Wiki collection...")
    try:
        client.collections.delete("Wiki")
        print("✓ Deleted existing collection")
    except Exception as e:
        print(f"Collection didn't exist or error deleting: {e}")

    print("Creating new Wiki collection with nomic-embed-text...")
    collection = client.collections.create(
        name="Wiki",
        vectorizer_config=Configure.Vectorizer.text2vec_openai(
            model="nomic-embed-text",
            dimensions=768,
        ),
        generative_config=Configure.Generative.openai(
            model="qwen2.5:0.5b"
        ),
    )
    print("✓ Created new collection")
    return collection

def load_and_import_data(collection):
    """Load data and import without vectors (let Weaviate vectorize)"""
    print("Loading original parquet data...")

    # Load data without vectors
    dataset = load_dataset('parquet',
                          data_files={'train': ['wiki-data/weaviate/snowflake-arctic-v2/*.parquet']},
                          split="train",
                          streaming=False)  # Load all into memory for faster processing

    print(f"Loaded {len(dataset)} items")

    print("Importing data and vectorizing...")
    with collection.batch.fixed_size(batch_size=200, concurrent_requests=2) as batch:
        for item in tqdm(dataset, desc="Importing"):
            # Only use text fields, skip the old vector
            data_obj = {
                "title": item["title"],
                "text": item["text"],
                "wiki_id": item["wiki_id"],
                "url": item["url"]
            }

            id = generate_uuid5(item["wiki_id"])
            batch.add_object(data_obj, uuid=id)

            # Check for errors
            if batch.number_errors > 10:
                print(f"Too many errors: {batch.number_errors}")
                break

    print(f"✓ Import completed. Final count: {len(collection)}")

def export_to_parquet(collection):
    """Export vectorized data to new parquet files"""
    print("Exporting vectorized data to parquet...")

    # Create output directory
    output_dir = "wiki-data/weaviate/nomic-embed-text"
    os.makedirs(output_dir, exist_ok=True)

    # Get all data with vectors
    all_data = []

    # Query in batches
    batch_size = 1000
    offset = 0

    while True:
        response = collection.query.fetch_objects(
            limit=batch_size,
            offset=offset,
            include_vector=True
        )

        if not response.objects:
            break

        for obj in response.objects:
            all_data.append({
                "title": obj.properties["title"],
                "text": obj.properties["text"],
                "wiki_id": obj.properties["wiki_id"],
                "url": obj.properties["url"],
                "vector": obj.vector["default"]  # Get the vector
            })

        offset += batch_size
        print(f"Exported {len(all_data)} items...")

    # Convert to DataFrame and save
    df = pd.DataFrame(all_data)

    # Split into files of 25k each (like original)
    items_per_file = 25000
    total_files = (len(df) + items_per_file - 1) // items_per_file

    for i in range(total_files):
        start_idx = i * items_per_file
        end_idx = min((i + 1) * items_per_file, len(df))

        file_df = df.iloc[start_idx:end_idx]
        filename = f"{output_dir}/{i+1:04d}.parquet"
        file_df.to_parquet(filename, index=False)
        print(f"✓ Saved {filename} with {len(file_df)} items")

    print(f"✓ Export completed! {total_files} files saved to {output_dir}/")

def main():
    print("Starting Wiki collection recreation...")

    client = connect_to_weaviate()
    print("✓ Connected to Weaviate")

    collection = recreate_collection(client)
    load_and_import_data(collection)
    export_to_parquet(collection)

    client.close()
    print("✓ All done!")

if __name__ == "__main__":
    main()