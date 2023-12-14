from dataclasses import dataclass
from dotenv import load_dotenv, find_dotenv
from os import getenv

from sqlalchemy.engine import URL


load_dotenv(find_dotenv())


@dataclass
class DataBaseConfig:
    host: str = getenv("DB_HOST")
    port: str = getenv("DB_PORT")
    user: str = getenv("DB_USER")
    password: str = getenv("DB_PASSWORD")
    database: str = getenv("DB_NAME")

    driver: str = "asyncpg"
    database_system: str = "postgresql"

    @property
    def connection_str(self) -> str:
        # postgresql+asyncpg://postgres:postgres@localhost:5432/stepanmartynov
        return URL.create(
            drivername=f"{self.database_system}+{self.driver}",
            username=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            database=self.database
        ).render_as_string(hide_password=False)


@dataclass
class RedisConfig:
    db: str = getenv("REDIS_DB", "1")
    host: str = getenv("REDIS_HOST", "localhost")
    port: str = getenv("REDIS_PORT", "6379")

    @property
    def url(self) -> str:
        return f"redis://{self.host}:{self.port}/{self.db}"


@dataclass
class BotConfig:
    token: str = getenv("BOT_TOKEN")


@dataclass
class DadataConfig:
    token: str = getenv("DADATA_API")
    secret_key: str = getenv("DADATA_SECRET")


@dataclass
class Configuration:

    debug = bool(getenv("DEBUG"))

    db = DataBaseConfig()
    bot = BotConfig()
    dadata = DadataConfig()
    redis = RedisConfig()


config = Configuration()


if __name__ == "__main__":
    print(config.bot.token)
    print(config.db.connection_str)
