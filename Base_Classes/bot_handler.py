from discord.ext import commands
import settings

class BotHandler:
    bot: commands.Bot

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def fetch_member(self, user_id):
        guild = await self.bot.fetch_guild(settings.GUILD_ID)
        return await guild.fetch_member(user_id)