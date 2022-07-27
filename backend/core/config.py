from pydantic import BaseSettings


class Settings(BaseSettings):
    database_url: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


class LogConfig(BaseSettings):
    logger_name: str = "cognitive-api"
    log_format: str = "%(levelprefix)s | %(asctime)s | Line %(lineno)s : %(message)s"
    log_level: str = "DEBUG"

    version = 1
    disable_existing_loggers = False
    formatters = {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": log_format,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    }
    handlers = {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
    }
    loggers = {
        logger_name: {"handlers": ["default"], "level": log_level},
    }
