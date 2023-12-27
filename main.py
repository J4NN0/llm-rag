import os
import os.path
from config import Config
from loader import load_wiki
from llama_index import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    load_index_from_storage,
    ServiceContext
)


def main():
    config = Config()

    # Check if storage already exists
    if not os.path.exists(config.storage_dir):
        print(f"Loading documents from {config.simple_data_dir} directory ...")
        documents = SimpleDirectoryReader(config.simple_data_dir).load_data()

        print(f"Loading documents from Wikipedia ...")
        wiki_documents = load_wiki(config.wiki_pages_file_path)
        documents.extend(wiki_documents)

        print("Building index over the documents ...")
        service_context = ServiceContext.from_defaults(chunk_size=512)
        index = VectorStoreIndex.from_documents(documents, service_context=service_context, show_progress=True)

        print(f"Persisting index to {config.storage_dir} storage ...")
        index.storage_context.persist(persist_dir=config.storage_dir)
    else:
        print(f"Loading existing index from {config.storage_dir} storage ...")
        storage_context = StorageContext.from_defaults(persist_dir=config.storage_dir)

        print("Loading index from storage ...")
        index = load_index_from_storage(storage_context)

    if config.is_engine_chat():
        # Create chat engine that can be used to query the index
        chat_engine = index.as_chat_engine(streaming=True, similarity_top_k=5)
        while True:
            query_str = input("Q: ")
            response = chat_engine.chat(query_str)
            response.print_response_stream()
    elif config.is_engine_query():
        # Create query engine that can be used to query the index
        query_engine = index.as_query_engine(streaming=True, similarity_top_k=5)
        response = query_engine.query("How long Federico lived in Sicily?")
        response.print_response_stream()
    else:
        print(f"Invalid query engine specified in config file")
        exit(-1)


if __name__ == "__main__":
    main()
