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


class LLM:
    __LOGGER_NAME = "llm"

    __DEFAULT_LLM_TYPE = "default"
    __LOCAL_LLM_TYPE = "local"
    __DEFAULT_EMBED_MODEL = "default"
    __LOCAL_EMBED_MODEL = "local"

    def __init__(self, llm_type, documents, storage_dir):
        # Set logger
        self.logger = logging.getLogger(self.__LOGGER_NAME)

        # LLM settings
        self.llm = self.__DEFAULT_LLM_TYPE
        self.embed_model = self.__DEFAULT_EMBED_MODEL
        self.llm_type = llm_type

        # List of documents to index
        self.documents = documents

        # Index storage directory
        self.storage_dir = storage_dir

    def get_index(self):
        """
        Creates the index from the given documents if it doesn't exist, otherwise loads it from storage.
        :return: The index from documents or from storage context
        """

        if self.__is_llm_type_local():
            self.llm = self.__get_llama2_model()
            self.embed_model = self.__LOCAL_EMBED_MODEL

        service_context = ServiceContext.from_defaults(llm=self.llm, chunk_size=512, embed_model=self.embed_model)

        if not self.__storage_exists():
            self.logger.info("Building index over the documents ...")
            index = VectorStoreIndex.from_documents(self.documents, service_context=service_context, show_progress=True)

            self.logger.info(f"Persisting index to {self.storage_dir} storage ...")
            index.storage_context.persist(persist_dir=self.storage_dir)
        else:
            self.logger.info(f"Creating existing index from {self.storage_dir} storage ...")
            storage_context = StorageContext.from_defaults(persist_dir=self.storage_dir)

            self.logger.info("Loading index from storage ...")
            index = load_index_from_storage(storage_context, service_context=service_context)

        return index

    def __storage_exists(self):
        return os.path.exists(self.storage_dir)

    def __is_llm_type_local(self):
        return self.llm_type == self.__LOCAL_LLM_TYPE

    @staticmethod
    def __get_llama2_model():
        """
        :return: The Llama2 model
        """

        return LlamaCPP(
            model_url="https://huggingface.co/TheBloke/Llama-2-13B-chat-GGUF/resolve/main/llama-2-13b-chat.Q5_K_M.gguf",
            # optionally, you can set the path to a pre-downloaded model instead of model_url
            model_path=None,
            temperature=0.0,
            max_new_tokens=1024,
            # llama2 has a context window of 4096 tokens, but we set it lower to allow for some wiggle room
            context_window=3900,  # note, this sets n_ctx in the model_kwargs below, so you don't need to pass it there.
            # kwargs to pass to __call__()
            generate_kwargs={},
            # kwargs to pass to __init__()
            # set to at least 1 to use GPU
            model_kwargs={"n_gpu_layers": 4},
            # transform inputs into Llama2 format
            messages_to_prompt=messages_to_prompt,
            completion_to_prompt=completion_to_prompt,
            verbose=True
        )
