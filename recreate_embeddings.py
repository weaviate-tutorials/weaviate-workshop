#!/usr/bin/env python3
"""
Script to recreate parquet files with new embeddings using mxbai-embed-large model
"""

import os
import pandas as pd
import requests
import numpy as np
from datasets import load_dataset
from tqdm import tqdm
from dotenv import load_dotenv
import json
import time
from urllib.parse import urlparse

# Load environment variables
load_dotenv()

OPENAI_URL = os.getenv("OPENAI_URL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")

def get_embedding(text, model=EMBEDDING_MODEL, max_retries=3):
    """Get embedding from Ollama using OpenAI API format with rate limiting"""
    # Use localhost for script running on host machine
    url = f"http://localhost:11434/v1/embeddings"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }
    data = {
        "input": text[:8192],  # Truncate very long texts
        "model": model
    }

    for attempt in range(max_retries):
        try:
            # Add delay to avoid rate limiting
            time.sleep(0.1)  # 100ms delay between requests

            response = requests.post(url, headers=headers, json=data, timeout=30)
            if response.status_code == 200:
                return response.json()["data"][0]["embedding"]
            elif response.status_code == 429:  # Rate limited
                wait_time = 2 ** attempt  # Exponential backoff
                print(f"Rate limited, waiting {wait_time}s...")
                time.sleep(wait_time)
                continue
            else:
                print(f"Error {response.status_code}: {response.text}")

        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)

    # Return zero vector as fallback
    return [0.0] * 1024

def process_parquet_file(input_path, output_path):
    """Process a single parquet file to replace embeddings"""
    print(f"Processing {input_path}")

    # Load the parquet file
    df = pd.read_parquet(input_path)

    # Get text column (adjust column name as needed)
    text_column = 'text'  # or 'content', 'wiki_text', etc. - check your data
    if text_column not in df.columns:
        print(f"Available columns: {df.columns.tolist()}")
        # Try common text column names
        for col in ['content', 'wiki_text', 'article', 'body']:
            if col in df.columns:
                text_column = col
                break

    print(f"Using text column: {text_column}")
    print(f"Processing {len(df)} rows...")

    # Generate new embeddings
    new_embeddings = []
    for idx, row in tqdm(df.iterrows(), total=len(df), desc="Generating embeddings"):
        try:
            text = str(row[text_column])
            embedding = get_embedding(text)
            new_embeddings.append(embedding)
        except Exception as e:
            print(f"Error processing row {idx}: {e}")
            # Use zero vector as fallback
            new_embeddings.append([0.0] * 1024)

    # Replace the vector column
    df['vector'] = new_embeddings

    # Save to new location
    df.to_parquet(output_path, index=False)
    print(f"Saved to {output_path}")

def main():
    # Create output directory
    input_dir = "wiki-data/weaviate/snowflake-arctic-v2"
    output_dir = "wiki-data/weaviate/mxbai-embed-large"
    os.makedirs(output_dir, exist_ok=True)

    # Process each parquet file
    parquet_files = [f for f in os.listdir(input_dir) if f.endswith('.parquet')]

    for filename in sorted(parquet_files):
        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, filename)

        # Skip if already processed
        if os.path.exists(output_path):
            print(f"Skipping {filename} - already exists")
            continue

        process_parquet_file(input_path, output_path)

if __name__ == "__main__":
    main()