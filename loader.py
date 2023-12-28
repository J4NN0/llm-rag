import logging
import os.path
from llama_index import (
    SimpleDirectoryReader,
    download_loader,
    ServiceContext,
    VectorStoreIndex,
    StorageContext,
    load_index_from_storage
)


class DataLoader:
    def __init__(self, storage_dir, simple_data_dir, wiki_pages_file_path):
        # Set logger
        self.logger = logging.getLogger("data_loader")

        # Index storage directory
        self.storage_dir = storage_dir

        # Data directories and files to load
        self.simple_data_dir = simple_data_dir
        self.wiki_pages_file_path = wiki_pages_file_path

    def load(self):
        """
        Loads the documents from the given simple data directory and web pages
        :return: The index from the documents
        """

        if not self.__storage_exists():
            documents = self.__load_simple()
            documents.extend(self.__load_wiki())

            self.logger.info("Building index over the documents ...")
            service_context = ServiceContext.from_defaults(chunk_size=512)
            index = VectorStoreIndex.from_documents(documents, service_context=service_context, show_progress=True)

            self.logger.info(f"Persisting index to {self.storage_dir} storage ...")
            index.storage_context.persist(persist_dir=self.storage_dir)
        else:
            self.logger.info(f"Creating existing index from {self.storage_dir} storage ...")
            storage_context = StorageContext.from_defaults(persist_dir=self.storage_dir)

            self.logger.info("Loading index from storage ...")
            index = load_index_from_storage(storage_context)

        return index

    def __storage_exists(self):
        return os.path.exists(self.storage_dir)

    def __load_simple(self):
        """
        Loads the documents from the given simple data directory
        :return: List of llama-index documents
        """

        self.logger.info(f"Loading documents from {self.simple_data_dir} directory ...")
        documents = SimpleDirectoryReader(self.simple_data_dir).load_data()

        return documents

    def __load_wiki(self):
        """
        Loads the wikipedia pages from the given wikipedia file path
        :return: List of llama-index documents
        """

        self.logger.debug("Downloading Wikipedia reader ...")
        WikipediaReader = download_loader("WikipediaReader")
        loader = WikipediaReader()

        wiki_pages = self.__get_pages(self.wiki_pages_file_path)
        self.logger.info(f"Found {len(wiki_pages)} tot pages to load")

        self.logger.info("Loading Wikipedia pages ...")
        documents = loader.load_data(pages=wiki_pages)

        return documents

    @staticmethod
    def __get_pages(file_path):
        """
        Reads the pages/links/documents from the given file path
        :param file_path: The path to the file containing the pages
        :return: List of pages
        """

        with open(file_path, "r") as f:
            links = f.readlines()
        return links
