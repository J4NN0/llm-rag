import logging
import os.path
from llama_index import (
    ServiceContext,
    VectorStoreIndex,
    StorageContext,
    load_index_from_storage
)
from llama_index.llms import LlamaCPP
from llama_index.llms.llama_utils import messages_to_prompt, completion_to_prompt


class Index:
    __LOGGER_NAME = "index"

    __LLM_DEFAULT = "DEFAULT"
    __LLAMA2_7BQ4 = "LLAMA2-7BQ4"
    __LLAMA2_7BQ4_URL = "https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/resolve/main/llama-2-7b-chat.Q4_K_M.gguf"
    __LLAMA2_7BQ5 = "LLAMA2-7BQ5"
    __LLAMA2_7BQ5_URL = "https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/resolve/main/llama-2-7b-chat.Q5_K_M.gguf"
    __LLAMA2_13BQ4 = "LLAMA2-13BQ4"
    __LLAMA2_13BQ4_URL = "https://huggingface.co/TheBloke/Llama-2-13B-chat-GGUF/resolve/main/llama-2-13b-chat.Q4_K_M.gguf"
    __LLAMA2_13BQ5 = "LLAMA2-13BQ5"
    __LLAMA2_13BQ5_URL = "https://huggingface.co/TheBloke/Llama-2-13B-chat-GGUF/resolve/main/llama-2-13b-chat.Q5_K_M.gguf"

    def __init__(self, storage_dir, documents=None, model_type=None):
        # Set logger
        self.logger = logging.getLogger(self.__LOGGER_NAME)
        self.verbose = self.logger.level == logging.DEBUG

        # List of documents to index and its storage directory
        self.documents = documents
        self.storage_dir = storage_dir

        # LLM model settings
        self.service_context = self.__get_service_context(model_type)

    def __get_service_context(self, model_type):
        """
        It returns the service context for the given model type.

        :param model_type: The LLM model type
        :return: The service context
        """

        match model_type:
            case self.__LLM_DEFAULT:
                llm = "default"
                embed_model = "default"
            case self.__LLAMA2_7BQ4:
                llm = self.__get_llama2_model(self.__LLAMA2_7BQ4_URL, self.verbose)
                embed_model = "local"
            case self.__LLAMA2_7BQ5:
                llm = self.__get_llama2_model(self.__LLAMA2_7BQ5_URL, self.verbose)
                embed_model = "local"
            case self.__LLAMA2_13BQ4:
                llm = self.__get_llama2_model(self.__LLAMA2_13BQ4_URL, self.verbose)
                embed_model = "local"
            case self.__LLAMA2_13BQ5:
                llm = self.__get_llama2_model(self.__LLAMA2_13BQ5_URL, self.verbose)
                embed_model = "local"
            case _:
                raise TypeError(f"LLM model type {model_type} not supported")

        return ServiceContext.from_defaults(llm=llm, chunk_size=512, embed_model=embed_model)

    def persist(self):
        """
        Create the index from the given documents and persist it to the given storage directory.

        :return: The index from documents
        """

        index = None
        if self.documents is not None and self.storage_dir is not None:
            self.logger.info("Building index over the documents ...")
            index = VectorStoreIndex.from_documents(self.documents, service_context=self.service_context, show_progress=self.verbose)

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
            index = load_index_from_storage(storage_context, service_context=self.service_context)
        else:
            self.logger.info(f"No storage found at {self.storage_dir} from which to load the index")

        return index

    def __storage_exists(self):
        return os.path.exists(self.storage_dir)

    @staticmethod
    def __get_llama2_model(model_url, verbose=False):
        """
        :return: The Llama2 model
        """

        return LlamaCPP(
            model_url=model_url,
            # temperature=0.0,
            # max_new_tokens=1024,
            # llama2 has a context window of 4096 tokens, but we set it lower to allow for some wiggle room
            context_window=2048,  # note, this sets n_ctx in the model_kwargs below, so you don't need to pass it there.
            # set to at least 1 to use GPU
            # model_kwargs={"n_gpu_layers": 1},
            # transform inputs into Llama2 format
            messages_to_prompt=messages_to_prompt,
            completion_to_prompt=completion_to_prompt,
            verbose=verbose
        )
