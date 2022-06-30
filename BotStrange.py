from config import *
from DBCommands import *


@bot.command()
async def sh(ctx):
    """Краткая справка по командам от разработчика"""
    output = """```
Изменение рейтинга:
    $rating [id | *] - вывод рейтинга [пользователя | всех пользователей]
    $set_rating [id] [value] - установка рейтинга пользователя с id на значение value
    $add_rating [id] [value] - изменение рейтинга пользователя с id на значение value
Изменение ролей:
    $roles [...] - вывод списка автоматической установки ролей
    $set_roles ([key] [id] [r_lower] [r_upper]), ... - обновление ролей с key и id на промежуток [r_lower, r_upper]
    $clear_roles ([key]), ... - полное удаление ролей с key
Изменение рабочей директории:
    $cd [...] - вывод рабочих директорий бота
    $set_cd [console] [logs] [info] - установка рабочих директорий
    ```"""
    await ctx.message.channel.send(output)


@bot.command()
async def update(ctx):
    output = DirectoryModule_ShowDirectory(ctx.guild.id)[1]
    server_users = get_BigBrother(ctx.guild.id)
    server_roles = get_Ranks(ctx.guild.id)

    for user in server_users:
        current_user = bot.get_guild(ctx.guild.id).get_member(user)
        for role in server_roles:
            current_role = bot.get_guild(ctx.guild.id).get_role(role)
            if current_role not in current_user.roles:
                if server_roles[role][0] <= server_users[user] <= server_roles[role][1]:
                    await current_user.add_roles(current_role)
                    await bot.get_channel(output).send(f"```Roles of {current_user} updated as [+{current_role}]```")
            else:
                if not (server_roles[role][0] <= server_users[user] <= server_roles[role][1]):
                    await current_user.remove_roles(current_role)
                    await bot.get_channel(output).send(f"```Roles of {current_user} updated as [-{current_role}]```")
    await bot.get_channel(output).send(f"```Обновления ролей завершены```")


