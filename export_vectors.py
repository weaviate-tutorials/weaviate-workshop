#!/usr/bin/env python3
"""
Export vectorized data from Weaviate back to parquet files
"""

import os
import pandas as pd
import weaviate
from weaviate.classes.init import Auth
from tqdm import tqdm
from dotenv import load_dotenv

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

def export_to_parquet():
    """Export vectorized data to new parquet files"""
    print("Connecting to Weaviate...")
    client = connect_to_weaviate()

    wiki = client.collections.get("Wiki")
    total_count = len(wiki)
    print(f"Found {total_count} items in Wiki collection")

    # Create output directory
    output_dir = "wiki-data/weaviate/nomic-embed-text"
    os.makedirs(output_dir, exist_ok=True)
    print(f"Exporting to: {output_dir}")

    # Export data in batches
    all_data = []
    batch_size = 1000

    print("Exporting data...")
    for i in tqdm(range(0, total_count, batch_size), desc="Fetching batches"):
        response = wiki.query.fetch_objects(
            limit=batch_size,
            offset=i,
            include_vector=True
        )

        for obj in response.objects:
            all_data.append({
                "title": obj.properties["title"],
                "text": obj.properties["text"],
                "wiki_id": obj.properties["wiki_id"],
                "url": obj.properties["url"],
                "vector": obj.vector["default"]  # Get the 768-dim vector
            })

    print(f"Collected {len(all_data)} items")

    # Convert to DataFrame
    df = pd.DataFrame(all_data)

    # Split into files of 25k each (like original)
    items_per_file = 25000
    total_files = (len(df) + items_per_file - 1) // items_per_file

    print(f"Splitting into {total_files} files...")
    for i in range(total_files):
        start_idx = i * items_per_file
        end_idx = min((i + 1) * items_per_file, len(df))

        file_df = df.iloc[start_idx:end_idx]
        filename = f"{output_dir}/{i+1:04d}.parquet"
        file_df.to_parquet(filename, index=False)
        print(f"✓ Saved {filename} with {len(file_df)} items")

    client.close()
    print(f"✅ Export completed! {total_files} files saved to {output_dir}/")
    print(f"Total items exported: {len(all_data)}")

if __name__ == "__main__":
    export_to_parquet()