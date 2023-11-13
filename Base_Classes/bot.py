import discord
from discord.ext import commands
from Database.controller import Ranks
from Messenger.discord import DiscordMessenger
from .bot_handler import BotHandler

class RSBot(commands.Bot):
    ranks: Ranks

    def initialise(self):
        discord_messenger = DiscordMessenger()
        bot_handler = BotHandler(self)
        self.ranks = Ranks(bot_handler, discord_messenger)
    
    async def process_message(self, message: discord.Message):
        await self.ranks.process_message(message)
    
    async def process_reaction(self, payload: discord.RawReactionActionEvent):
        await self.ranks.process_reaction(payload)