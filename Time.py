from config import *


def is_console():
    def predicate(ctx):
        return ctx.message.channel == bot.get_channel(db.get_directory(ctx.guild.id).data[0])

    return commands.check(predicate)


class RatingModule(commands.Cog):
    def __init__(self, bot):
        self.bot = bot







