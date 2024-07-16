import logging
import os.path
from llama_index.core import VectorStoreIndex, StorageContext, load_index_from_storage


class Index:
    __LOGGER_NAME = "index"

    def __init__(self, storage_dir, documents=None):
        # Set logger
        self.logger = logging.getLogger(self.__LOGGER_NAME)
        self.verbose = self.logger.level == logging.DEBUG

        # List of documents to index and its storage directory
        self.documents = documents
        self.storage_dir = storage_dir

    def persist(self):
        """
        Create the index from the given documents and persist it to the given storage directory.

        :return: The index from documents
        """

        index = None
        if self.documents is not None and self.storage_dir is not None:
            self.logger.info("Building index over the documents ...")
            index = VectorStoreIndex.from_documents(self.documents, show_progress=self.verbose)

            self.logger.info(f"Persisting index to {self.storage_dir} storage ...")
            index.storage_context.persist(persist_dir=self.storage_dir)
        else:
            self.logger.info(f"Documents or index storage path not provided, skipping index creation")

        return index

    def load(self):
        """
        Loads the index from the given storage directory.

        :return: The index from storage context
        """

        index = None
        if self.__storage_exists():
            self.logger.info(f"Loading existing index from {self.storage_dir} storage ...")
            storage_context = StorageContext.from_defaults(persist_dir=self.storage_dir)
            index = load_index_from_storage(storage_context)
        else:
            self.logger.info(f"No storage found at {self.storage_dir} from which to load the index")

        return index

    def __storage_exists(self):
        return os.path.exists(self.storage_dir)
