import aiohttp, discord, settings
from Base_Classes.messenger import Messenger

class DiscordMessenger(Messenger):
    async def send_message(self, message: str):
        async with aiohttp.ClientSession() as session:
            webhook = discord.Webhook.from_url(settings.CHATTER_WEBHOOK, session = session)
            await webhook.send(message)
