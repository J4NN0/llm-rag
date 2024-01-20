from config import Config
from loader.reader import DataReader
from loader.index import Index


def run_chat_engine(index):
    # Create chat engine that can be used to query the index
    chat_engine = index.as_chat_engine(streaming=True, similarity_top_k=5)
    while True:
        query_str = input("Q: ")
        response = chat_engine.chat(query_str)
        response.print_response_stream()


def run_query_engine(index):
    # Create query engine that can be used to query the index
    query_engine = index.as_query_engine(streaming=True, similarity_top_k=5)
    while True:
        query_str = input("Q&A: ")
        response = query_engine.query(query_str)
        response.print_response_stream()


def main():
    config = Config()

    data_loader = DataReader(data_dir=config.data_dir)
    docs = data_loader.load()

    index = Index(
        documents=docs,
        storage_dir=config.storage_dir,
        model_type=config.model_type,
        model_path=config.model_path
    ).persist()

    if config.is_engine_chat():
        run_chat_engine(index)
    elif config.is_engine_query():
        run_query_engine(index)
    else:
        print(f"Invalid query engine specified in {config.CONFIG_FILE_PATH} config file: {config.engine}")
        exit(-1)


if __name__ == "__main__":
    main()
