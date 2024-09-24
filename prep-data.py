from huggingface_hub import list_repo_files, hf_hub_download

def list_wiki_datasets():
    all_files = list_repo_files("weaviate/wiki-sample", repo_type="dataset")
    
    # get items with 0001 parquet file, this way we avoid duplicates
    items = list(filter(lambda path: path.endswith("0001.parquet"), all_files))

    # remove the parquet from the name
    return [item.replace("/0001.parquet", "") for item in items]

def list_dataset_files(dataset):
    dataset_files = list_repo_files("weaviate/wiki-sample", repo_type="dataset")

    return list(filter(lambda path: path.startswith(dataset), dataset_files))

def download_file(file):
    hf_hub_download(
        repo_id="weaviate/wiki-sample",
        filename=file,
        repo_type="dataset",
        local_dir="wiki-data",
    )

def download_source_files(dataset="no-vectors", max_files=1000):
    files_to_download = list_dataset_files(dataset)
    # print(f"Files to download: {files_to_download}")

    for file in files_to_download:
        print(f"Downloading {file}")
        download_file(file)

        max_files -= 1
        if(max_files == 0): break

download_source_files("openai/text-embedding-3-small", 10)