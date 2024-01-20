import argparse
from config import Config
from loader.reader import DataReader
from loader.index import Index
from engine import run_chat_engine, run_query_engine


def load_index_and_run_engine(config):
    index = Index(
        storage_dir=config.storage_dir,
        model_type=config.model_type
    ).load()

    if config.is_engine_chat():
        run_chat_engine(index)
    elif config.is_engine_query():
        run_query_engine(index)
    else:
        print(f"Invalid query engine: {config.engine}")
        exit(-1)


def load_data_and_store_index(config):
    data_loader = DataReader(data_dir=config.data_dir)
    docs = data_loader.load()

    _ = Index(
        storage_dir=config.storage_dir,
        documents=docs,
        model_type=config.model_type
    ).persist()


def get_arg_parser():
    parser = argparse.ArgumentParser(
        prog='llm',
        description='Fine tune a language model for question answering',
        usage='%(prog)s [options]'
    )
    parser.add_argument(
        '-L', '--load-data',
        help='Ingest your custom documents and create index',
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

    if args.load_data:
        load_data_and_store_index(config)
    elif args.query_data:
        load_index_and_run_engine(config)
    else:
        print("Invalid arguments")
        parser.print_help()


if __name__ == "__main__":
    main()
