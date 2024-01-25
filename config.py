import logging
import sys
import os
import openai


class Config:
    __OPENAI_API_KEY_ENV_VAR = "OPENAI_API_KEY"

    __LOG_LEVEL_DEBUG = "DEBUG"

    def __init__(self):
        # OpenAI API key
        self.openai_key = os.environ.get('OPENAI_API_KEY')
        self.__set_openai_key()

        # Logging
        self.log_level = os.environ.get('LOGGING_LEVEL').upper()
        self.__set_log_level()

        # Data and Index storage directories
        self.data_dir = os.environ.get('DATA_DIR')
        self.storage_dir = os.environ.get('INDEX_STORAGE')

        # LLM
        self.model_type = os.environ.get('MODEL_TYPE').upper()

    def __set_openai_key(self):
        openai.api_key = os.environ[self.__OPENAI_API_KEY_ENV_VAR]

    def __set_log_level(self):
        level = logging.INFO
        if self.log_level == self.__LOG_LEVEL_DEBUG:
            level = logging.DEBUG

        logging.basicConfig(stream=sys.stdout, level=level)
