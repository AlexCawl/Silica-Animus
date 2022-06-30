from config import *
from DBCommands import *


async def solo_update(server_id, user_id):
    output = DirectoryModule_ShowDirectory(server_id)[1]
    server_roles = get_Ranks(server_id)

    current_user = bot.get_guild(server_id).get_member(user_id)
    current_value = RatingModule_ShowUserRating(server_id, user_id)

    for role in server_roles:
        current_role = bot.get_guild(server_id).get_role(role)
        if current_role not in current_user.roles:
            if server_roles[role][0] <= current_value <= server_roles[role][1]:
                await current_user.add_roles(current_role)
                await bot.get_channel(output).send(f"```Roles of {current_user} updated as [+{current_role}]```")
        else:
            if not (server_roles[role][0] <= current_value <= server_roles[role][1]):
                await current_user.remove_roles(current_role)
                await bot.get_channel(output).send(f"```Roles of {current_user} updated as [-{current_role}]```")


@bot.command()
async def add_rating(ctx, user_id, value):
    """
        Эта команда добавляет рейтинг пользователю на сервере.
    """
    user_id = int(user_id)
    value = int(value)
    if ctx.message.channel == bot.get_channel(DirectoryModule_ShowDirectory(ctx.guild.id)[0]):
        channel_output = bot.get_channel(DirectoryModule_ShowDirectory(ctx.guild.id)[1])

        res = RatingModule_AddRating(user_id, ctx.guild.id, value)

        if not res:
            await channel_output.send(
                f'```Rating of [{user_id} : {str(bot.get_user(user_id).name)}] for {value} points updated successfully```')
            await solo_update(ctx.guild.id, user_id)
        else:
            await channel_output.send(
                f'```[ERROR] [[{user_id} : {str(bot.get_user(user_id).name)}] is not in Database!]```')


@bot.command()
async def set_rating(ctx, user_id, value):
    """
        Эта команда устанавливает рейтинг пользователя на сервере.
    """
    user_id = int(user_id)
    value = int(value)
    if ctx.message.channel == bot.get_channel(DirectoryModule_ShowDirectory(ctx.guild.id)[0]):
        channel_output = bot.get_channel(DirectoryModule_ShowDirectory(ctx.guild.id)[1])

        res = RatingModule_SetRating(user_id, ctx.guild.id, value)

        if not res:
            await channel_output.send(
                f'```Rating of [{user_id} : {str(bot.get_user(user_id).name)}] for {value} points set successfully```')
            await solo_update(ctx.guild.id, user_id)
        else:
            await channel_output.send(
                f'```[ERROR] [[{user_id} : {str(bot.get_user(user_id).name)}] is not in Database!]```')


@bot.command()
async def rating(ctx, user_id):
    """
        Эта команда показывает рейтинг пользователя/пользователей на сервере.
    """
    if ctx.message.channel == bot.get_channel(DirectoryModule_ShowDirectory(ctx.guild.id)[0]):
        channel_output = ctx.message.channel

        res = RatingModule_ShowServerRating(user_id, ctx.guild.id)
        await channel_output.send(f'```{res}```')
