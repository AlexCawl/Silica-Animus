import requests

from config import *


def is_console():
    def predicate(ctx):
        return ctx.message.channel == bot.get_channel(db.get_directory(ctx.guild.id).data[0])

    return commands.check(predicate)


class RatingModule(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def roles_output(self, roles_dictionary):
        output = ""

        for key in roles_dictionary:
            output += f"[{key}] {roles_dictionary[key][1][0]:5.0f} {roles_dictionary[key][1][1]:5.0f}\t{roles_dictionary[key][0]}\n"
        return output

    async def SoloUser(self, server_id: int, user_id: int):
        """Процесс добавления конкретному пользователю конкретной роли"""

        value = db.get_rating(server_id, user_id).data[user_id][1]
        current_user = bot.get_guild(server_id).get_member(user_id)
        server_roles = db.get_roles(server_id).data

        msg = ''

        for role_id in server_roles:
            current_role = bot.get_guild(server_id).get_role(role_id)
            limits = server_roles[role_id][1]

            if current_role in current_user.roles:
                if not (limits[0] <= value <= limits[1]):
                    await current_user.remove_roles(current_role)
                    msg += f'[{current_user.name:30}] [-{current_role}]\n'
            else:
                if limits[0] <= value <= limits[1]:
                    await current_user.add_roles(current_role)
                    msg += f'[{current_user.name:30}] [+{current_role}]\n'

        return msg

    async def SoloRole(self, server_id: int, role_id: int, limits: list, delete: bool):
        """Процесс добавления конкретному пользователю возможных ролей на сервере"""

        server_users = db.get_rating(server_id, '*').data
        current_role = bot.get_guild(server_id).get_role(role_id)

        msg = ''

        for user_id in server_users:
            current_user = bot.get_guild(server_id).get_member(user_id)
            value = db.get_rating(server_id, user_id).data[user_id][1]

            if current_role in current_user.roles:
                if delete or not (limits[0] <= value <= limits[1]):
                    await current_user.remove_roles(current_role)
                    msg += f'[{current_user.name:30}] [-{current_role}]\n'
            else:
                if not delete and (limits[0] <= value <= limits[1]):
                    await current_user.add_roles(current_role)
                    msg += f'[{current_user.name:30}] [+{current_role}]\n'

        return msg

    async def ServerUpdate(self, server_id: int):
        """Процесс добавления всем пользователям сервера возможных ролей на сервере"""
        server_users = db.get_rating(server_id, '*').data

        msg = ''

        for user_id in server_users:
            msg += await self.SoloUser(server_id, user_id)

        return msg

    @commands.Cog.listener()
    async def on_ready(self):
        """Активация бота"""

        for guild in bot.guilds:
            msg = await self.ServerUpdate(guild.id)
            print(guild.name, guild.id)
            print(msg)

        print('We have logged in as {0.user}'.format(bot))

    @commands.Cog.listener()
    async def on_member_join(self, member):
        """Обновление рейтинга-ролей при присоединении нового участника"""
        result = db.new_user(member.guild.id, member.guild.name, member.id, member.name, 0)
        if result.state:
            msg = await self.SoloUser(member.guild.id, member.id)
            logs = bot.get_channel(db.get_directory(member.guild.id).data[1])
            if msg != '':
                await logs.send(f'```{msg}```')

    @commands.command()
    @is_console()
    async def add_rating(self, ctx, *, args: str):
        """Добавление рейтинга пользователю на сервере"""
        channel_output = bot.get_channel(db.get_directory(ctx.guild.id).data[1])
        args = args.split()

        for i in range(0, len(args), 2):
            try:
                user_id = int(args[i])
                value = int(args[i + 1])
                res = db.add_rating(ctx.guild.id, user_id, value)

                if res.state:
                    await channel_output.send(f'```[{user_id} : {str(bot.get_user(user_id).name)}] [+{value}]```')
                    msg = await self.SoloUser(ctx.guild.id, user_id)
                    if msg != '':
                        await channel_output.send(f'```{msg}```')
                else:
                    await channel_output.send(
                        f'```[ERROR] [[{user_id} : {str(bot.get_user(user_id).name)}] is not in Database!]```')
            except:
                await channel_output.send(f'```Operation for [{args[i]}] is unsuccessful```')

        await ctx.message.add_reaction('👀')

    @commands.command()
    @is_console()
    async def set_rating(self, ctx, *, args: str):
        """Установление рейтинга пользователю на сервере"""
        channel_output = bot.get_channel(db.get_directory(ctx.guild.id).data[1])
        args = args.split()

        for i in range(0, len(args), 2):
            try:
                user_id = int(args[i])
                value = int(args[i + 1])
                res = db.set_rating(ctx.guild.id, user_id, value)

                if res.state:
                    await channel_output.send(f'```[{user_id} : {str(bot.get_user(user_id).name)}] [={value}]```')
                    msg = await self.SoloUser(ctx.guild.id, user_id)
                    if msg != '':
                        await channel_output.send(f'```{msg}```')
                    await ctx.message.add_reaction('👀')
                else:
                    await channel_output.send(
                        f'```[ERROR] [[{user_id} : {str(bot.get_user(user_id).name)}] is not in Database!]```')
            except:
                await channel_output.send(f'```Operation for [{args[i]}] is unsuccessful```')

    @commands.command()
    @is_console()
    async def rating(self, ctx, user_id):
        """Вывод рейтинга пользователей"""
        channel_output = ctx.message.channel

        res = db.get_rating(ctx.guild.id, user_id)
        output = ""
        for key in res.data:
            output += f"[{key}] {res.data[key][1]:5.0f}\t{res.data[key][0]}\n"
        await channel_output.send(f'```{output}```')

    @commands.command()
    @is_console()
    async def set_roles(self, ctx, *args):
        """Установка списка автообновления ролей в соответствии с рейтингом"""

        logs = bot.get_channel(db.get_directory(ctx.guild.id).data[1])
        args = list(map(int, args))

        for i in range(0, len(args), 3):
            role_id = args[i]
            rating_lower = args[i + 1]
            rating_upper = args[i + 2]

            res = db.set_role(ctx.guild.id, ctx.guild.name, role_id, bot.get_guild(ctx.guild.id).get_role(role_id),
                              rating_lower, rating_upper)

            if res.state:
                await logs.send(
                    f'```Role [{role_id}] [{str(bot.get_guild(ctx.guild.id).get_role(role_id))}] in [{rating_lower}:{rating_upper}] changed successfully```')
                msg = await self.SoloRole(ctx.guild.id, role_id, [rating_lower, rating_upper], False)
                if msg != '':
                    await logs.send(f'```{msg}```')
            else:
                await logs.send(f'```[ERROR] [An error in the database!]```')

        await ctx.message.channel.send(
            f"```Автоматическое присвоение ролей установлено следующим образом:\n{self.roles_output(db.get_roles(ctx.guild.id).data)}```")

    @commands.command()
    @is_console()
    async def clear_roles(self, ctx, *args: int):
        """Удаление ролей из списка автообновления"""

        logs = bot.get_channel(db.get_directory(ctx.guild.id).data[1])

        for role_id in args:
            limits = db.get_roles(ctx.guild.id).data[role_id][1]
            msg = await self.SoloRole(ctx.guild.id, role_id, limits, True)
            if msg != '':
                await logs.send(f'```{msg}```')

            res = db.clr_role(ctx.guild.id, role_id)
            if res.state:
                await logs.send(f"```Role with key [{role_id}] deleted successfully```")
            else:
                await logs.send(f"```Role with key [{role_id}] delete failed```")

        await ctx.message.channel.send(
            f"```Автоматическое присвоение ролей установлено следующим образом:\n{self.roles_output(db.get_roles(ctx.guild.id).data)}```")

    @commands.command()
    @is_console()
    async def roles(self, ctx):
        """Вывод списка автоматического обновления ролей"""
        res = db.get_roles(ctx.guild.id)

        await ctx.message.channel.send(
            f"```Автоматическое присвоение ролей установлено следующим образом:\n{self.roles_output(res.data)}```")

    @commands.command()
    @is_console()
    async def ipc(self, ctx, url):
        """Результаты с соревнования на ipc"""
        def smart_split(line: str, args: list) -> list:
            for sep in args:
                line = line.replace(sep, '|*|')

            out = [x if (x != '' and x != '\n') else None for x in line.split('|*|')]
            while None in out: out.remove(None)
            return out

        r = requests.get(url).text.split('\n')[57]
        r = smart_split(r, ['<tr>', '</tr>', '</table>'])
        out = ""

        for element in r:
            tmp = smart_split(element, ['<td>', '</td>', '<td align="right">'])
            login = tmp[0].split(', ')
            cur = f"{tmp[-1]:5} {tmp[-3]:10} {login[-1]:16} {login[0]} \n"

            if len(out + cur) > 1994:
                await ctx.message.channel.send(f"```{out}```")
                out = ""

            out += cur
        await ctx.message.channel.send(f"```{out}```")
