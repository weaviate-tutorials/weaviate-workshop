from datasets import load_dataset
from tqdm import tqdm
from weaviate.util import generate_uuid5

def prepare_dataset():
    dt = load_dataset('parquet', data_files={'train': ['../wiki-data/openai/text-embedding-3-small/*.parquet']}, split="train", streaming=True)
    # dt = load_dataset("weaviate/wiki-sample", "openai-text-embedding-3-small", split="train", streaming=True)

    print(f"Loaded Dataset: '{dt.info.dataset_name}' - Config: '{dt.info.config_name}'")

    return dt

def test_dataset():
    dt = prepare_dataset()

    counter = 10
    for item in dt:
        print(item)

        counter -= 1
        if(counter == 0): break

def import_wiki_data(client, collection_name, max_rows=20_000):
    if(client.collections.exists(collection_name) == False):
        print(f"Error: Collection {collection_name} doesn't exist")
        return

    print(f"Importing {max_rows} data items")

    dataset = prepare_dataset()
    wiki = client.collections.get(collection_name)

    counter = 0

    with wiki.batch.fixed_size(batch_size=2000, concurrent_requests=2) as batch:
        for item in tqdm(dataset, total=max_rows):

            data_to_insert = {   
                "wiki_id": item["wiki_id"],
                "text": item["text"],
                "title": item["title"],
                "url": item["url"],
            }

            item_id = generate_uuid5(item["wiki_id"])

            # vector = item["vector"]
            item_vector = {
                "main_vector": item["vector"]
            }

            batch.add_object(
                properties=data_to_insert,
                
                uuid=item_id,
                vector=item_vector
            )

            # Check number of errors while running
            if(batch.number_errors > 10):
                print(f"Reached {batch.number_errors} Errors during batch import")
                break
            
            # stop after the request number reaches = max_rows
            counter += 1
            if(counter >= max_rows):
                break
    
    # check for errors at the end
    if (len(wiki.batch.failed_objects)>0):
        print("Final error check")
        print(f"Some errors {len(wiki.batch.failed_objects)}")
        print(wiki.batch.failed_objects[-1])
    
    print(f"Imported {counter} items")
    print("-----------------------------------")