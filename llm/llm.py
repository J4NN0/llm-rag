import logging
from llama_index.core import Settings
from llama_index.llms.llama_cpp import LlamaCPP
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.llama_cpp.llama_utils import (
    messages_to_prompt,
    completion_to_prompt,
)


class Llm:
    __LOGGER_NAME = "LLM"

    __LLM_DEFAULT = "DEFAULT"
    __LLAMA2_7B_Q4 = "LLAMA2-7B_Q4"
    __LLAMA2_7B_Q4_URL = "https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/resolve/main/llama-2-7b-chat.Q4_K_M.gguf"
    __LLAMA2_7B_Q5 = "LLAMA2-7B_Q5"
    __LLAMA2_7B_Q5_URL = "https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/resolve/main/llama-2-7b-chat.Q5_K_M.gguf"
    __LLAMA2_13B_Q4 = "LLAMA2-13B_Q4"
    __LLAMA2_13B_Q4_URL = "https://huggingface.co/TheBloke/Llama-2-13B-chat-GGUF/resolve/main/llama-2-13b-chat.Q4_K_M.gguf"
    __LLAMA2_13B_Q5 = "LLAMA2-13B_Q5"
    __LLAMA2_13B_Q5_URL = "https://huggingface.co/TheBloke/Llama-2-13B-chat-GGUF/resolve/main/llama-2-13b-chat.Q5_K_M.gguf"

    __MIXTRAL_7B_Q4 = "MIXTRAL-7B_Q4"
    __MIXTRAL_7B_Q4_URL = "https://huggingface.co/TheBloke/Mixtral-8x7B-Instruct-v0.1-GGUF/resolve/main/mixtral-8x7b-instruct-v0.1.Q4_K_M.gguf"
    __MIXTRAL_7B_Q5 = "MIXTRAL-7B_Q5"
    __MIXTRAL_7B_Q5_URL = "https://huggingface.co/TheBloke/Mixtral-8x7B-Instruct-v0.1-GGUF/resolve/main/mixtral-8x7b-instruct-v0.1.Q5_K_M.gguf"

    def __init__(self, model_type=None):
        # Set logger
        self.logger = logging.getLogger(self.__LOGGER_NAME)
        self.verbose = self.logger.level == logging.DEBUG

        # LLM model settings
        self.chunk_size = 512
        self.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
        self.llm = self.__get_llm(model_type)

    def set(self):
        Settings.llm = self.llm
        Settings.embed_model = self.embed_model
        Settings.chunk_size = self.chunk_size

    def __get_llm(self, model_type):
        """
        It loads the relative llm for the given model type.

        :param model_type: The LLM model type
        :return: The LLM
        """

        match model_type:
            case self.__LLM_DEFAULT:
                llm = "default"
                self.embed_model = "default"
            case self.__LLAMA2_7B_Q4:
                llm = self.__get_llm_model(self.__LLAMA2_7B_Q4_URL, self.verbose)
            case self.__LLAMA2_7B_Q5:
                llm = self.__get_llm_model(self.__LLAMA2_7B_Q5_URL, self.verbose)
            case self.__LLAMA2_13B_Q4:
                llm = self.__get_llm_model(self.__LLAMA2_13B_Q4_URL, self.verbose)
            case self.__LLAMA2_13B_Q5:
                llm = self.__get_llm_model(self.__LLAMA2_13B_Q5_URL, self.verbose)
            case self.__MIXTRAL_7B_Q4:
                llm = self.__get_llm_model(self.__MIXTRAL_7B_Q4_URL, self.verbose)
            case self.__MIXTRAL_7B_Q5:
                llm = self.__get_llm_model(self.__MIXTRAL_7B_Q5_URL, self.verbose)
            case _:
                raise TypeError(f"LLM model type '{model_type}' not supported")

        return llm

    @staticmethod
    def __get_llm_model(model_url, verbose=False):
        return LlamaCPP(
            model_url=model_url,
            temperature=0.1,
            max_new_tokens=256,
            context_window=2048,
            model_kwargs={"n_gpu_layers": -1},
            messages_to_prompt=messages_to_prompt,
            completion_to_prompt=completion_to_prompt,
            verbose=verbose
        )
