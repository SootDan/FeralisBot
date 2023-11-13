from discord.ext import commands
import settings

def is_command_channel():
    def predicate(ctx):
        return ctx.message.channel.id == settings.COMMANDS_CHANNEL
    return commands.check(predicate)