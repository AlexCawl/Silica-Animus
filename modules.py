from config import *


def is_console():
    def predicate(ctx):
        return ctx.message.channel == bot.get_channel(db.get_directory(ctx.guild.id).data[0])

    return commands.check(predicate)


class Standart(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        res = db.create()
        print('create', res.state, res.data)

        for guild in bot.guilds:
            for member in guild.members:
                result = db.new_user(guild.id, guild.name, member.id, member.name, 0)
                print('new_user', result.state, result.data)

        print('We have logged in as {0.user}'.format(bot))

    @commands.command()
    async def joke(self, ctx):
        await bot.get_channel(ctx.channel.id).send(f"```{random.choice(all_jokes)}```")
        print('joke_send', True, None)

    @commands.command()
    @is_console()
    async def sh(self, ctx):
        """Краткая справка по командам от разработчика"""
        output = "**Изменение рейтинга:**" \
                 "\t$rating [id | *] - вывод рейтинга [пользователя | всех пользователей]\n" \
                 "\t$set_rating [id] [value] - установка рейтинга пользователя с id на значение value\n" \
                 "\t$add_rating [id] [value] - изменение рейтинга пользователя с id на значение value\n" \
                 "**Изменение ролей:**" \
                 "\t$roles [...] - вывод списка автоматической установки ролей\n" \
                 "\t$set_roles ([key] [id] [r_lower] [r_upper]), ... - обновление ролей с key и id на промежуток [r_lower, r_upper]\n" \
                 "\t$clear_roles ([key]), ... - полное удаление ролей с key\n" \
                 "**Изменение рабочей директории:**\n" \
                 "\t$cd [...] - вывод рабочих директорий бота\n" \
                 "\t$set_cd [console] [logs] [info] - установка рабочих директорий\n"
        await ctx.message.channel.send(output)
        print('super_help', True, None)

    @commands.command()
    @is_console()
    async def hello_world(self, ctx, channel_id: int):
        """Приветственное сообщение новичкам"""

        output = "**Привет всем новичкам!**\n" \
                 "Добро пожаловать на сервер _Центра Олимпиадного Программирования_ ЮУрГУ\n" \
                 "Центр олимпиадного программирования ЮУрГУ занимается подготовкой студентов к личным и командным соревнованиям по программированию.\n" \
                 "Программа подготовки студентов к участию в командных и личных соревнованиях по программированию рассчитана на **три года**. Каждый год соответствует уровню подготовки студента:\n" \
                 "\t**Уровень 1:** Программа «Базовая подготовка» рассчитана на студентов, которые только начинают заниматься олимпиадным программированием.\n" \
                 "\t**Уровень 2:** Программа «Олимпиадная подготовка» рассчитана на студентов, которые готовятся к выходу в полуфинал ACM ICPC.\n" \
                 "\t**Уровень 3:** Программа «Продвинутая олимпиадная подготовка» рассчитана на опытных студентов, которые готовы хорошо выступить на полуфинале и пройти в финал ACM ICPC."
        await bot.get_channel(channel_id).send(f"""{output}""")
        output = "**Структура сервера:**\n" \
                 "[1] **Гостевая комната**\n" \
                 "\tЭта категория создана для новоприбывших участников. Здесь вы найдете общую информацию, правила сервера и принцип работы с ним.\n" \
                 "[2] **Информация**\n" \
                 "\tВ этой категории находятся новостные сводки о происходящем на сервере.\n" \
                 "[3] **Текстовые каналы**\n" \
                 "\tНесколько текстовых каналов для общения участников и игры в Wordle.\n" \
                 "[4] **Голосовые каналы**\n" \
                 "\tНесколько голосовых каналов для живого общения.\n" \
                 "[5] **Консоль**\n" \
                 "\t _Эта категория доступна только админам._ Предназначена для работы с администраторским ботом.\n" \
                 "[6-7-8] **Уровни олимпиадной программы**\n" \
                 "\tЭта категория создана для олимпиадной подготовки участников по соответствующему им уровню.\n"
        await bot.get_channel(channel_id).send(f"""{output}""")
        output = "**Особенности сервера**\n" \
                 "\t1. Система социального рейтинга\n" \
                 "\t2. Автоматизированное создание опросов\n" \
                 "\t3. Автоматическое присвоение ролей согласно рейтингу\n" \
                 "\t4. Распределение рабочих директорий для управления ботом\n" \
                 "\t5. Перенос игры Wordle в Discord и собственный банк слов\n" \
                 "\t6. Музыкальный бот\n"
        await bot.get_channel(channel_id).send(f"""{output}""")
        output = "```Нажимай на эту реакцию, и начинай программировать вместе с нами)```"
        message = await bot.get_channel(channel_id).send(f"""{output}""")
        await message.add_reaction("💻")
        print('hello_world', True, None)


class Directory(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def set_cd(self, ctx, console_id, log_id, info_id):
        """
            Эта команда устанавливает рабочие директории для бота, где он будет считывать сообщения, писать логи отработки
            команд, выводить информацию.
        """
        console_id = int(console_id)
        log_id = int(log_id)
        info_id = int(info_id)

        res = db.set_directory(ctx.guild.id, bot.get_guild(ctx.guild.id).name, console_id, log_id, info_id)
        print('set_directory', res.state, res.data)

        await ctx.message.channel.send(f'```Рабочие директории изменены следующим образом:\n'
                                       f'Консоль: {bot.get_channel(console_id)}\n'
                                       f'Логи: {bot.get_channel(log_id)}\n'
                                       f'Объявления: {bot.get_channel(info_id)}```')
        await bot.get_channel(console_id).send(f'```Этот канал теперь является рабочей директорией: [Консоль]```')
        await bot.get_channel(log_id).send(f'```Этот канал теперь является рабочей директорией: [Логи]```')
        await bot.get_channel(info_id).send(f'```Этот канал теперь является рабочей директорией: [Объявления]```')

    @commands.command()
    async def cd(self, ctx):
        """
            Эта команда показывает рабочие директории для бота, где он будет считывать сообщения, писать логи отработки
            команд, выводить информацию.
        """

        res = db.get_directory(ctx.guild.id)
        print('get_directory', res.state, res.data)

        await ctx.message.channel.send(f'```Рабочие директории установлены следующим образом:\n'
                                       f'Консоль: {bot.get_channel(res.data[0])}\n'
                                       f'Логи: {bot.get_channel(res.data[1])}\n'
                                       f'Объявления: {bot.get_channel(res.data[2])}```')


class Rating(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def roles_output(self, roles_dictionary):
        output = ""

        for key in roles_dictionary:
            output += f"[{key}] {roles_dictionary[key][1][0]:5.0f} {roles_dictionary[key][1][1]:5.0f}\t{roles_dictionary[key][0]}\n"
        return output

    async def solo_update(self, server_id, user_id):
        output = db.get_directory(server_id).data[1]
        server_roles = db.get_roles(server_id).data

        current_user = bot.get_guild(server_id).get_member(user_id)
        current_value = db.get_rating(server_id, user_id).data
        print(current_user, current_value)

        for role in server_roles:
            current_role = bot.get_guild(server_id).get_role(server_roles[role][2])
            if current_role not in current_user.roles:
                if server_roles[role][1][0] <= current_value <= server_roles[role][1][1]:
                    await current_user.add_roles(current_role)
                    await bot.get_channel(output).send(
                        f"```Roles of {current_user} updated as [+{current_role}]```")
            else:
                if not (server_roles[role][1][0] <= current_value <= server_roles[role][1][1]):
                    await current_user.remove_roles(current_role)
                    await bot.get_channel(output).send(
                        f"```Roles of {current_user} updated as [-{current_role}]```")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        print(dir(member))

    @commands.command()
    @is_console()
    async def update(self, ctx):
        output = db.get_directory(ctx.guild.id).data[1]
        a = db.get_rating(ctx.guild.id, '*')
        b = db.get_roles(ctx.guild.id)

        server_users = a.data
        server_roles = b.data

        for user in server_users:
            current_user = bot.get_guild(ctx.guild.id).get_member(user)
            for role in server_roles:
                current_role = bot.get_guild(ctx.guild.id).get_role(server_roles[role][2])
                if current_role not in current_user.roles:
                    if server_roles[role][1][0] <= server_users[user][1] <= server_roles[role][1][1]:
                        await current_user.add_roles(current_role)
                        await bot.get_channel(output).send(
                            f"```Roles of {current_user} updated as [+{current_role}]```")
                else:
                    if not (server_roles[role][1][0] <= server_users[user][1] <= server_roles[role][1][1]):
                        await current_user.remove_roles(current_role)
                        await bot.get_channel(output).send(
                            f"```Roles of {current_user} updated as [-{current_role}]```")
        await bot.get_channel(output).send(f"```Обновления ролей завершены```")
        print('update_user_roles', a.state, b.state)

    @commands.command()
    @is_console()
    async def add_rating(self, ctx, user_id: int, value: int):
        """Эта команда добавляет рейтинг пользователю на сервере."""
        channel_output = bot.get_channel(db.get_directory(ctx.guild.id).data[1])

        res = db.add_rating(ctx.guild.id, user_id, value)
        print('add_rating', res.state, res.data)

        if res.state:
            await channel_output.send(
                f'```Rating of [{user_id} : {str(bot.get_user(user_id).name)}] for {value} points updated successfully```')
            await self.solo_update(ctx.guild.id, user_id)
        else:
            await channel_output.send(
                f'```[ERROR] [[{user_id} : {str(bot.get_user(user_id).name)}] is not in Database!]```')

    @commands.command()
    @is_console()
    async def set_rating(self, ctx, user_id: int, value: int):
        """Эта команда устанавливает рейтинг пользователя на сервере."""
        channel_output = bot.get_channel(db.get_directory(ctx.guild.id).data[1])

        res = db.set_rating(ctx.guild.id, user_id, value)
        print('set_rating', res.state, res.data)

        if res.state:
            await channel_output.send(
                f'```Rating of [{user_id} : {str(bot.get_user(user_id).name)}] for {value} points set successfully```')
            await self.solo_update(ctx.guild.id, user_id)
        else:
            await channel_output.send(
                f'```[ERROR] [[{user_id} : {str(bot.get_user(user_id).name)}] is not in Database!]```')

    @commands.command()
    @is_console()
    async def rating(self, ctx, user_id):
        """Эта команда показывает рейтинг пользователя/пользователей на сервере."""
        channel_output = ctx.message.channel

        res = db.get_rating(ctx.guild.id, user_id)
        output = ""
        for key in res.data:
            output += f"[{key}] {res.data[key][1]:5.0f}\t{res.data[key][0]}\n"
        await channel_output.send(f'```{output}```')
        print('rating', res.state, None)

    @commands.command()
    @is_console()
    async def set_roles(self, ctx, *args):
        """Эта команда устанавливает список ролей в соответствии с определенным рейтингом на конкретном сервере."""

        channel_output = bot.get_channel(db.get_directory(ctx.guild.id).data[1])
        args = list(map(int, args))

        for i in range(0, len(args), 4):
            try:
                key = args[i]
                role_id = args[i + 1]
                rating_lower = args[i + 2]
                rating_upper = args[i + 3]

                res = db.set_roles(ctx.guild.id, bot.get_guild(ctx.guild.id).name, key, role_id,
                                   bot.get_guild(ctx.guild.id).get_role(role_id), rating_lower, rating_upper)

                if res.state:
                    await channel_output.send(
                        f'```Role [{key}] [{role_id} : {str(bot.get_guild(ctx.guild.id).get_role(role_id))}] in [{rating_lower}:{rating_upper}] changed successfully```')
                else:
                    await channel_output.send(f'```[ERROR] [An error in the database!]```')
                print('set_roles', res.state)

            except:
                await channel_output.send(f'```[ERROR] [An error due to missing parameters!]```')

        await ctx.message.channel.send(
            f"```Автоматическое присвоение ролей установлено следующим образом:\n{self.roles_output(db.get_roles(ctx.guild.id).data)}```")

    @commands.command()
    @is_console()
    async def clear_roles(self, ctx, *args):
        """Эта команда удаляет роли из списка автоматического присвоения на сервере по указанным ключам."""

        channel_output = bot.get_channel(db.get_directory(ctx.guild.id).data[1])

        for key in args:
            try:
                res = db.clr_roles(ctx.guild.id, key)

                if res.state:
                    await channel_output.send(f"```Role with key [{key}] deleted successfully```")
                else:
                    await channel_output.send(f"```Role with key [{key}] delete failed```")
                print('clear_roles', res.state)
            except:
                await channel_output.send(f"```Role with key [{key}] is not in database```")

        await ctx.message.channel.send(
            f"```Автоматическое присвоение ролей установлено следующим образом:\n{self.roles_output(db.get_roles(ctx.guild.id).data)}```")

    @commands.command()
    @is_console()
    async def roles(self, ctx):
        """Эта команда показывает список автоматического присвоения ролей на сервере."""
        await ctx.message.channel.send(
            f"```Автоматическое присвоение ролей установлено следующим образом:\n{self.roles_output(db.get_roles(ctx.guild.id).data)}```")
        print('roles', True, None)


class Survey(commands.Cog):
    def survey_reactions(self, cases, reactions_result):
        text_result = ''
        survey_statistics = {}

        for i in range(len(cases)):
            text_result += f"{cases[i]} [{reactions_result[i]}]\n"
            survey_statistics.update({reactions_result[i]: 1})

        return text_result, survey_statistics

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        surveysDB = db.get_survey(payload.guild_id).data

        if payload.message_id in surveysDB.keys() and payload.member.bot is False:
            current_statistics = eval(surveysDB[payload.message_id][1])
            if str(payload.emoji) in list(current_statistics.keys()):
                current_statistics[str(payload.emoji)] += 1
                res = db.add_survey(payload.guild_id, payload.message_id, current_statistics)
                print('+reaction', res.state, None)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        surveysDB = db.get_survey(payload.guild_id).data

        if payload.message_id in surveysDB.keys():
            current_statistics = eval(surveysDB[payload.message_id][1])
            if str(payload.emoji) in list(current_statistics.keys()):
                current_statistics[str(payload.emoji)] -= 1
                res = db.add_survey(payload.guild_id, payload.message_id, current_statistics)
                print('-reaction', res.state, None)

    @commands.command()
    @is_console()
    async def set_survey(self, ctx, *, body):
        """Создание опроса"""

        info = db.get_directory(ctx.guild.id).data[2]  # info
        logs = db.get_directory(ctx.guild.id).data[1]  # logs
        title, *cases = body.strip().split('\n')  # парсим на заголовок и положения
        reactions = []  # создаем жизнеспособные реакции
        i = 0
        counter = len(cases)

        # генерируем новые реакции
        while i < counter:
            new_emoji = random.choice(all_reactions)
            if new_emoji not in reactions:
                try:
                    await ctx.message.add_reaction(new_emoji)  # если реакция ставится (существует в Дискорд)
                    i += 1
                    reactions.append(new_emoji)
                except:
                    continue

        # создаем текст опроса и генерируем первоначальную статистику
        text, stats = self.survey_reactions(cases, reactions)
        # создаем тело опроса
        embed = discord.Embed(
            title=f"{title}",
            description=f"{text}",
            colour=discord.Colour.from_rgb(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        )
        survey_message = await bot.get_channel(info).send(embed=embed)

        # проставляем реакции
        for emj in reactions:
            await survey_message.add_reaction(emj)

        # записываем в базу данных
        result = db.set_survey(ctx.guild.id, bot.get_guild(ctx.guild.id).name, survey_message.id, title, stats)
        if result.state:
            await bot.get_channel(logs).send(
                f"```Survey [{survey_message.id}] [{title}] {reactions} is created successfully```")
        else:
            await bot.get_channel(logs).send(f"```Survey is not created successfully :(```")
        print('set_survey', result.state, None)

    @commands.command()
    @is_console()
    async def clear_survey(self, ctx, message_id: int):
        """Завершение опроса и вывод результатов"""

        info = db.get_directory(ctx.guild.id).data[2]  # info
        logs = db.get_directory(ctx.guild.id).data[1]  # logs
        channel = bot.get_channel(info)
        message = await channel.fetch_message(message_id)

        result = dict(eval(db.get_survey(ctx.guild.id).data[message_id][1]))

        all_votes = sum(result.values())

        output = "Опрос закончился!\nРезультаты опроса:\n"
        for key in result:
            percentage = result[key] / all_votes * 100
            output += f"[{key}] - {result[key]} | {percentage:.1f}%\n"

        await message.reply(f"""```{output}```""")

        res = db.clr_survey(ctx.guild.id, message_id)
        if res.state:
            await bot.get_channel(logs).send(f"""```Survey with [id = {message_id}] deleted successfully```""")
        else:
            await bot.get_channel(logs).send(f"""```Survey with [id = {message_id}] doesn't deleted!```""")
        print('clear_survey', res.state, None)

    @commands.command()
    @is_console()
    async def check_survey(self, ctx, message_id: int):
        """Проверка текущей статистики опроса"""

        result = eval(db.get_survey(ctx.guild.id).data[message_id][1])
        all_votes = sum(result.values())

        output = "Текущие результаты опроса:\n"
        for key in result:
            percentage = result[key] / all_votes * 100
            output += f"[{key}] - {result[key]} | {percentage:.1f}%\n"

        await bot.get_channel(ctx.channel.id).send(f"""```{output}```""")
        print('check_survey', True, None)

    @commands.command()
    @is_console()
    async def get_survey(self, ctx):
        channel_id = ctx.channel.id
        surveys = db.get_survey(ctx.guild.id).data
        output = ""
        for key in surveys:
            output += f"[{key}]\t[{surveys[key][1]}]\t[{surveys[key][0]}]\n"

        await bot.get_channel(channel_id).send(f"```{output}```")
        print('get_survey', True, None)

