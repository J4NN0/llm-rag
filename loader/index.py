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

    def __init__(self, documents, storage_dir, model_type=None, model_path=None):
        # Set logger
        self.logger = logging.getLogger(self.__LOGGER_NAME)

        # List of documents to index and its storage directory
        self.documents = documents
        self.storage_dir = storage_dir

        # LLM model settings
        self.service_context = self.__get_service_context(model_type)
        self.model_path = model_path

    def __get_service_context(self, model_type):
        """
        It returns the service context for the given model type.

        :param model_type: The LLM model type
        :return: The service context
        """

        llm = "default"
        embed_model = "default"
        if model_type == "local":
            llm = self.__get_llama2_model()
            embed_model = "local"

        return ServiceContext.from_defaults(llm=llm, chunk_size=512, embed_model=embed_model)

    def persist(self):
        """
        Create the index from the given documents and persist it to the given storage directory.

        :return: The index from documents
        """

        self.logger.info("Building index over the documents ...")
        index = VectorStoreIndex.from_documents(self.documents, service_context=self.service_context, show_progress=True)

        self.logger.info(f"Persisting index to {self.storage_dir} storage ...")
        index.storage_context.persist(persist_dir=self.storage_dir)

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
