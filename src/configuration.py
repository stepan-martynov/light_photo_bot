from dataclasses import dataclass
from dotenv import load_dotenv, find_dotenv
from os import getenv


load_dotenv(find_dotenv())

@dataclass
class BotConfig:
    token: str = getenv("BOT_TOKEN")


@dataclass
class Configuration:
    bot = BotConfig()


config = Configuration()


if __name__ == "__main__":
    print(config.bot.token)