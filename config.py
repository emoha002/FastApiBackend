from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")


class Config(BaseSettings):
    POSTGRESS_URL: str = os.environ.get("DEVELOPMENT_DATABASE_URL", "")
    SECRET_KEY: str = os.environ.get("PRODUCTION_DATABASE_URL", "123456789")
    CONFIG_TYPE: str = ""


class ProductionConfig(Config):
    CONFIG_TYPE: str = "production"
    # oeverride the POSTGRESS_URL
    POSTGRESS_URL: str = os.environ.get("PRODUCTION_DATABASE_URL", "")
    pass


class DevConfing(Config):
    CONFIG_TYPE: str = "development"
    pass


class TestConfig(Config):
    CONFIG_TYPE: str = "test"
    pass


def get_settings(config_type: str = os.environ.get("CONFIG", "dev")) -> Config:
    if config_type == "dev":
        return DevConfing()
    if config_type == "test":
        return TestConfig()
    return ProductionConfig()


initial_config = get_settings()
