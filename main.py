import configparser
import os
import os.path
import openai
from llama_index import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    load_index_from_storage,
    ServiceContext,
    download_loader
)

OPENAI_API_KEY_ENV_VAR = "OPENAI_API_KEY"
CONFIG_FILE = "config.ini"


def main():
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)

    storage_dir = config['DIRECTORY']['STORAGE']
    data_dir = config['DIRECTORY']['DATA']

    os.environ[OPENAI_API_KEY_ENV_VAR] = config['OPENAI']['API_KEY']
    openai.api_key = os.environ["OPENAI_API_KEY"]

    # Check if storage already exists
    if not os.path.exists(storage_dir):
        print(f"Loading documents from {data_dir} directory ...")
        documents = SimpleDirectoryReader(data_dir).load_data()

        print(f"Loading documents from Wikipedia ...")
        WikipediaReader = download_loader("WikipediaReader")
        loader = WikipediaReader()
        documents.extend(loader.load_data(pages=["Berlin"]))

        print("Building index over the documents ...")
        service_context = ServiceContext.from_defaults(chunk_size=512)
        index = VectorStoreIndex.from_documents(documents, service_context=service_context, show_progress=True)

        print(f"Persisting index to {storage_dir} storage ...")
        index.storage_context.persist(persist_dir=storage_dir)
    else:
        print(f"Loading existing index from {data_dir} storage ...")
        storage_context = StorageContext.from_defaults(persist_dir=storage_dir)

        print("Loading index from storage ...")
        index = load_index_from_storage(storage_context)

    if config['QUERY']['ENGINE'].casefold() == "chat":
        # Create chat engine that can be used to query the index
        chat_engine = index.as_chat_engine(streaming=True, similarity_top_k=5)
        while True:
            query_str = input("Q: ")
            response = chat_engine.chat(query_str)
            response.print_response_stream()
    elif config['QUERY']['ENGINE'].casefold() == "query":
        # Create query engine that can be used to query the index
        query_engine = index.as_query_engine(streaming=True, similarity_top_k=5)
        response = query_engine.query("How long Federico lived in Sicily?")
        response.print_response_stream()
    else:
        print(f"Invalid query engine specified in {CONFIG_FILE} file")
        exit(-1)


if __name__ == "__main__":
    main()
