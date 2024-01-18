import logging
from pathlib import Path
from llama_index import (
    SimpleDirectoryReader,
    download_loader
)


class DataLoader:
    __LOGGER_NAME = "data_loader"

    __JSON_READER_LOADER = "JSONReader"
    __WIKIPEDIA_READER_LOADER = "WikipediaReader"

    def __init__(self, simple_data_dir, json_data_dir, wiki_pages_file_path):
        # Set logger
        self.logger = logging.getLogger(self.__LOGGER_NAME)

        # Data directories and files to load
        self.simple_data_dir = simple_data_dir
        self.json_data_dir = json_data_dir
        self.wiki_pages_file_path = wiki_pages_file_path

    def load(self):
        """
        Loads the documents from all the given directories.
        :return: List of llama-index documents
        """

        documents = self.__load_simple()
        documents.extend(self.__load_json())
        documents.extend(self.__load_wiki())

        return documents

    def __load_simple(self):
        """
        Loads the documents from the given simple data directory.
        The best file reader will be automatically selected from the given file extensions.
        :return: List of llama-index documents
        """

        self.logger.info(f"Loading files from {self.simple_data_dir} directory ...")
        documents = SimpleDirectoryReader(self.simple_data_dir).load_data()
        self.logger.info(f"Loaded {len(documents)} documents")

        return documents

    def __load_json(self):
        """
        Loads the documents from the given JSON file path.
        :return: List of llama-index documents
        """

        self.logger.debug("Downloading JSON reader ...")
        JSONReader = download_loader(self.__JSON_READER_LOADER)
        loader = JSONReader()

        self.logger.info(f"Loading JSON docs from {self.json_data_dir} directory ...")
        documents = loader.load_data(Path(self.json_data_dir), is_jsonl=False)
        self.logger.info(f"Loaded {len(documents)} documents")

        return documents

    def __load_wiki(self):
        """
        Loads the wikipedia pages from the given wikipedia file path.
        :return: List of llama-index documents
        """

        self.logger.debug("Downloading Wikipedia reader ...")
        WikipediaReader = download_loader(self.__WIKIPEDIA_READER_LOADER)
        loader = WikipediaReader()

        wiki_pages = self.__get_pages(self.wiki_pages_file_path)

        self.logger.info(f"Loading Wikipedia pages ...")
        documents = loader.load_data(pages=wiki_pages)
        self.logger.info(f"Loaded {len(documents)} documents")

        return documents

    @staticmethod
    def __get_pages(file_path):
        """
        Reads the pages/links/documents from the given file path.
        :param file_path: The path to the file containing the pages
        :return: List of pages
        """

        with open(file_path, "r") as f:
            links = f.readlines()
        return links
