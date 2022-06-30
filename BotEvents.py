from config import *
from DBCommands import *


@bot.event
async def on_ready():
    db_create()

    for guild in bot.guilds:
        for member in guild.members:
            RatingModule_NewUser(member.id, member.name, guild.id, guild.name, 0)

    print('We have logged in as {0.user}'.format(bot))