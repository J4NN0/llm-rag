import configparser
import logging
import sys
import os
import openai


class Config:
    CONFIG_FILE_PATH = "config.ini"

    __OPENAI_API_KEY_ENV_VAR = "OPENAI_API_KEY"

    __LOG_LEVEL_DEBUG = "debug"

    __INDEX_ENGINE_CHAT = "chat"
    __INDEX_ENGINE_QUERY = "query"

    def __init__(self):
        config = configparser.ConfigParser()
        config.read(self.CONFIG_FILE_PATH)

        # OpenAI API key
        self.openai_key = config['OPENAI']['API_KEY']
        self.__set_env_openai_key()

        # Logging
        self.log_level = config['LOGGING']['LEVEL'].casefold()
        self.__set_log_level()

        # Data
        self.data_dir = config['DATA']['DIR']

        # Index
        self.storage_dir = config['INDEX']['STORAGE']
        self.engine = config['INDEX']['ENGINE'].casefold()

        # LLM
        self.model_type = config['LLM']['MODEL_TYPE'].casefold()
        self.model_path = config['LLM']['MODEL_PATH']

    def __set_env_openai_key(self):
        os.environ[self.__OPENAI_API_KEY_ENV_VAR] = self.openai_key
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
