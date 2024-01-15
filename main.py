from config import Config
from loader import DataLoader


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
    print("Loading config ...")
    config = Config()

    print("Loading data ...")
    data_loader = DataLoader(
        storage_dir=config.storage_dir,
        simple_data_dir=config.simple_data_dir,
        json_data_dir=config.json_data_dir,
        wiki_pages_file_path=config.wiki_pages_file_path
    )
    index = data_loader.load()

    if config.is_engine_chat():
        run_chat_engine(index)
    elif config.is_engine_query():
        run_query_engine(index)
    else:
        print(f"Invalid query engine specified in {config.CONFIG_FILE_PATH} config file: {config.engine}")
        exit(-1)


if __name__ == "__main__":
    main()
