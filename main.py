import argparse
from config import Config
from loader.reader import DataReader
from loader.index import Index
from llm.llm import Llm


def load_index_and_run_engine(config):
    index = Index(
        storage_dir=config.storage_dir,
    ).load()

    chat_engine = index.as_chat_engine(similarity_top_k=3, chat_mode="context")
    while True:
        query_str = input("\nQ: ")
        if query_str == "exit":
            print("Cya!")
            break
        if query_str.strip() == "":
            continue

        streaming_response = chat_engine.stream_chat(query_str)
        for token in streaming_response.response_gen:
            print(token, end="")


def load_data_and_store_index(config):
    data_loader = DataReader(data_dir=config.data_dir)
    docs = data_loader.load()

    _ = Index(
        storage_dir=config.storage_dir,
        documents=docs,
    ).persist()


def get_arg_parser():
    parser = argparse.ArgumentParser(
        prog='llm',
        description='LLM prompt augmentation to chat with your documents',
        usage='%(prog)s [options]'
    )
    parser.add_argument(
        '-L', '--load-data',
        help='Ingest your documents and create index',
        action='store_true',
        required=False
    )
    parser.add_argument(
        '-Q', '--query-data',
        help='Chat with your documents. Type "exit" to quit',
        action='store_true',
        required=False
    )

    return parser


def main():
    parser = get_arg_parser()
    args = parser.parse_args()

    config = Config()

    Llm(model_type=config.model_type).set()

    if args.load_data:
        load_data_and_store_index(config)
    elif args.query_data:
        load_index_and_run_engine(config)
    else:
        print("Invalid arguments")
        parser.print_help()


if __name__ == "__main__":
    main()
