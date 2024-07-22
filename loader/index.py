import logging
import os.path
from llama_index.core import VectorStoreIndex, StorageContext, load_index_from_storage
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.core.chat_engine.types import ChatMode


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

        if self.documents is None or self.storage_dir is None:
            self.logger.error(f"Documents or index storage path not provided, skipping index creation")
            return

        self.logger.info("Building index over the documents ...")
        index = VectorStoreIndex.from_documents(self.documents, show_progress=self.verbose)

        self.logger.info(f"Persisting index to {self.storage_dir} storage ...")
        index.storage_context.persist(persist_dir=self.storage_dir)

        return index

    def load(self):
        """
        Loads the index from the given storage directory and convert it to a chat engine

        :return: The chat engine
        """

        if not self.__storage_exists():
            self.logger.error(f"No storage found at {self.storage_dir} from which to load the index")
            return

        self.logger.info(f"Loading existing index from {self.storage_dir} storage ...")
        storage_context = StorageContext.from_defaults(persist_dir=self.storage_dir)
        index = load_index_from_storage(storage_context)

        memory = ChatMemoryBuffer.from_defaults(token_limit=1500)

        chat_engine = index.as_chat_engine(
            similarity_top_k=3,
            chat_mode=ChatMode.CONTEXT,
            memory=memory
        )

        return chat_engine

    def __storage_exists(self):
        return os.path.exists(self.storage_dir)
