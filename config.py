import logging
import sys
import os
import openai


class Config:
    __OPENAI_API_KEY_ENV_VAR = "OPENAI_API_KEY"

    __LOG_LEVEL_DEBUG = "debug"

    __INDEX_ENGINE_CHAT = "chat"
    __INDEX_ENGINE_QUERY = "query"

    def __init__(self):
        # OpenAI API key
        self.openai_key = os.environ.get('OPENAI_API_KEY')
        self.__set_openai_key()

        # Logging
        self.log_level = os.environ.get('LOGGING_LEVEL').casefold()
        self.__set_log_level()

        # Data
        self.data_dir = os.environ.get('DATA_DIR')

        # Index
        self.storage_dir = os.environ.get('INDEX_STORAGE')
        self.engine = os.environ.get('INDEX_ENGINE').casefold()

        # LLM
        self.model_type = os.environ.get('MODEL_TYPE').casefold()
        self.model_path = os.environ.get('MODEL_PATH')

    def __set_openai_key(self):
        openai.api_key = os.environ[self.__OPENAI_API_KEY_ENV_VAR]

    def __set_log_level(self):
        level = logging.INFO
        if self.log_level == self.__LOG_LEVEL_DEBUG:
            level = logging.DEBUG

        logging.basicConfig(stream=sys.stdout, level=level)

    def is_engine_chat(self):
        return self.engine == self.__INDEX_ENGINE_CHAT

    def is_engine_query(self):
        return self.engine == self.__INDEX_ENGINE_QUERY
