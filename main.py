import os
import os.path
import openai
from llama_index import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    load_index_from_storage,
    ServiceContext
)

OPENAI_API_KEY_ENV_VAR = "OPENAI_API_KEY"
FILE_DIRECTORY = "./data"
STORAGE_DIRECTORY = "./storage"


def main():
    os.environ[OPENAI_API_KEY_ENV_VAR] = "sk-<your-key-here>"
    openai.api_key = os.environ["OPENAI_API_KEY"]

    # Check if storage already exists
    if not os.path.exists(STORAGE_DIRECTORY):
        print(f"Loading documents from {FILE_DIRECTORY} directory ...")
        documents = SimpleDirectoryReader(FILE_DIRECTORY).load_data()

        print("Building index over the documents ...")
        service_context = ServiceContext.from_defaults(chunk_size=512)
        index = VectorStoreIndex.from_documents(documents, service_context=service_context, show_progress=True)

        print(f"Persisting index to {STORAGE_DIRECTORY} storage ...")
        index.storage_context.persist()
    else:
        print(f"Loading documents from {FILE_DIRECTORY} storage ...")
        storage_context = StorageContext.from_defaults(persist_dir=STORAGE_DIRECTORY)

        print("Loading index from storage ...")
        index = load_index_from_storage(storage_context)

    # Create query engine that can be used to query the index
    query_engine = index.as_query_engine()
    response = query_engine.query("How long Federico lived in Sicily?")
    print(response)


if __name__ == "__main__":
    main()
