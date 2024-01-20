import logging
import glob
from pathlib import Path
from llama_index import (
    SimpleDirectoryReader,
    download_loader
)


class DataLoader:
    __LOGGER_NAME = "data_loader"

    __SIMPLE_SUPPORTED_EXTENSIONS = [".csv", ".docx", ".epub", ".hwp", ".ipynb", ".jpeg", ".mbox", ".md", ".mp3", ".pdf", ".png", ".pptm", ".pptx"]
    __JSON_READER_LOADER = "JSONReader"
    __WIKIPEDIA_READER_LOADER = "WikipediaReader"

    def __init__(self, data_dir):
        # Set logger
        self.logger = logging.getLogger(self.__LOGGER_NAME)

        # Data directory and files to load
        self.data_dir = data_dir

    def load(self):
        """
        Loads the documents from all the given directories.

        :return: List of llama-index documents
        """

        documents = []
        if self.data_dir is not None:
            loaders = [
                self.__load_simple,
                self.__load_json,
                self.__load_wiki
            ]

            self.logger.info(f"Loading documents from {self.data_dir} directory ...")
            for load in loaders:
                documents.extend(load())
            self.logger.info(f"Loaded {len(documents)} documents")
        else:
            self.logger.info("No data directory specified, skipping loading documents")

        return documents

    def __load_simple(self):
        """
        Loads the documents from the given data directory only for supported file types.
        The best file reader will be automatically selected from the given file extensions.
        Docs: https://docs.llamaindex.ai/en/stable/module_guides/loading/simpledirectoryreader.html#supported-file-types

        :return: List of llama-index documents
        """

        self.logger.debug(f"Loading simple documents ...")
        documents = SimpleDirectoryReader(
            input_dir=self.data_dir,
            required_exts=self.__SIMPLE_SUPPORTED_EXTENSIONS
        ).load_data()
        self.logger.debug(f"Loaded {len(documents)} documents")

        return documents

    def __load_json(self):
        """
        Loads the JSON documents from the given data directory.

        :return: List of llama-index documents
        """

        json_files = self.__get_all_files_with_ext("json")

        JSONReader = download_loader(self.__JSON_READER_LOADER)
        loader = JSONReader()

        self.logger.debug(f"Loading JSON documents ...")
        documents = []
        for json_file in json_files:
            documents.extend(loader.load_data(Path(json_file), is_jsonl=False))
        self.logger.debug(f"Loaded {len(documents)} JSON documents")

        return documents

    def __load_wiki(self):
        """
        Loads the wikipedia pages from the given data directory.

        :return: List of llama-index documents
        """

        wiki_files = self.__get_all_files_with_ext("wikipedia")
        wiki_pages = []
        for wiki_file in wiki_files:
            wiki_pages.extend(self.__get_pages(wiki_file))

        WikipediaReader = download_loader(self.__WIKIPEDIA_READER_LOADER)
        loader = WikipediaReader()

        self.logger.debug(f"Loading Wikipedia pages ...")
        documents = loader.load_data(pages=wiki_pages)
        self.logger.debug(f"Loaded {len(documents)} Wikipedia documents")

        return documents

    def __get_all_files_with_ext(self, file_ext):
        """
        Gets all the files with the given extension from the data directory.

        :param file_ext: The file extension to search for
        :return: List of file paths
        """

        return glob.glob(f"{self.data_dir}/*.{file_ext}")

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
