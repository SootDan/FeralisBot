import asyncio, discord, database
from discord.ext import commands
from Assets.token import token
from Base_Classes.bot import RSBot
from Database.models import UserActivity # folder is Ranks in tutorial
from Users.models import User

def setup_tables():
    database.db.create_tables([User, UserActivity])

def run():
    setup_tables()

    intents = discord.Intents.all()
    bot = RSBot(command_prefix = '!', intents = intents)
    bot.initialise()

    @bot.event
    async def on_ready():
        await bot.load_extension('Database.cog')
        activity = discord.Game(name = 'Of Feral Tendencies', type = 3) # Displays a status
        await bot.change_presence(status = discord.Status.online, activity = activity)
        print(f'Logged on as {bot.user}! ID: {bot.user.id}') # Prints out to console

    @bot.event
    async def on_message(message: discord.Message):
        # checks if something is a bot or a command, if not, gives xp
        ctx = await bot.get_context(message)
        if not ctx.valid:
            if not message.author.bot:
                await bot.process_message(message)
        await bot.process_commands(message)

    @bot.event
    async def on_member_join(member):
        guild = member.guild
        channel = discord.utils.get(guild.text_channels, id = ARRIVALS_DEPARTURES_CHANNEL)
        if channel:
            await channel.send(ARRIVAL_MESSAGE.format(member.mention))

    @bot.event
    async def on_member_remove(member):
        guild = member.guild
        channel = discord.utils.get(guild.text_channels, id = ARRIVALS_DEPARTURES_CHANNEL)
        if channel:
            await channel.send(DEPARTURE_MESSAGE.format(member))

    @bot.event
    async def on_raw_reaction_add(payload: discord.RawReactionActionEvent):
        await bot.process_reaction(payload)

    @bot.event
    async def on_raw_reaction_remove(payload: discord.RawReactionActionEvent):
        await bot.process_reaction(payload)

    bot.run(token)

    async def main():
    # async with bot:
        # await bot.add_cog(greeter) # join/leave tracker
        # await bot.add_cog(levelling)
        await bot.start(token)

if __name__ == '__main__':
    run()