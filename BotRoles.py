from config import *
from DBCommands import *


def is_console():
    def predicate(ctx):
        return ctx.message.channel == bot.get_channel(DirectoryModule_ShowDirectory(ctx.guild.id)[0])

    return commands.check(predicate)


@bot.command()
@is_console()
async def set_roles(ctx, *args):
    """
        Эта команда устанавливает список ролей в соответствии с определенным рейтингом на конкретном сервере.
        Пример:
            $set_roles            | вызов команды
            1 5783754375 0 10     | роль с id = 5783754375 установится с key = 1 для рейтинга от 0 до 10
            2 5747543875 10 20    | роль с id = 5747543875 установится с key = 2 для рейтинга от 10 до 20
            3 9423423945 20 30    | роль с id = 9423423945 установится с key = 3 для рейтинга от 20 до 30
    """

    channel_output = bot.get_channel(DirectoryModule_ShowDirectory(ctx.guild.id)[1])
    args = list(map(int, args))

    for i in range(0, len(args), 4):
        try:
            key = args[i]
            role_id = args[i + 1]
            rating_lower = args[i + 2]
            rating_upper = args[i + 3]

            print(ctx.guild.id, str(bot.get_guild(ctx.guild.id).name),
                  key, role_id, str(bot.get_guild(ctx.guild.id).get_role(role_id)),
                  rating_lower, rating_upper)

            res = RatingModule_SetAutoRoles(ctx.guild.id, str(bot.get_guild(ctx.guild.id).name),
                                            key, role_id, str(bot.get_guild(ctx.guild.id).get_role(role_id)),
                                            rating_lower, rating_upper)

            if not res:
                await channel_output.send(
                    f'```Role [{key}] [{role_id} : {str(bot.get_guild(ctx.guild.id).get_role(role_id))}] in [{rating_lower}:{rating_upper}] changed successfully```')
            else:
                await channel_output.send(f'```[ERROR] [An error in the database!]```')

        except:
            await channel_output.send(
                f'```[ERROR] [An error due to missing parameters!]```')

    await ctx.message.channel.send(
        f"```Автоматическое присвоение ролей установлено следующим образом:\n{RatingModule_ShowAutoRoles(ctx.guild.id)}```")


@bot.command()
@is_console()
async def clear_roles(ctx, *args):
    """
        Эта команда удаляет роли из списка автоматического присвоения на сервере по указанным ключам.
    """


    channel_output = bot.get_channel(DirectoryModule_ShowDirectory(ctx.guild.id)[1])

    for key in args:
        try:
            res = RatingModule_ClearAutoRoles(ctx.guild.id, int(key))

            if not res:
                await channel_output.send(f"```Role with key [{key}] deleted successfully```")
            else:
                await channel_output.send(f"```Role with key [{key}] delete failed```")
        except:
            await channel_output.send(f"```Role with key [{key}] is not in database```")

    await ctx.message.channel.send(
        f"```Автоматическое присвоение ролей установлено следующим образом:\n{RatingModule_ShowAutoRoles(ctx.guild.id)}```")


@bot.command()
@is_console()
async def roles(ctx):
    """
        Эта команда показывает список автоматического присвоения ролей на сервере.
    """
    await ctx.message.channel.send(
        f"```Автоматическое присвоение ролей установлено следующим образом:\n{RatingModule_ShowAutoRoles(ctx.guild.id)}```")
