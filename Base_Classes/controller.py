from .messenger import Messenger
from .bot_handler import BotHandler

class Controller:
    messenger: Messenger
    bot_handler: BotHandler

    def __init__(self, bot_handler: BotHandler, messenger: Messenger) -> None:
        self.messenger = messenger
        self.bot_handler = bot_handler