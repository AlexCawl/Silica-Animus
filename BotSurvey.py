import random
import time

from config import *
from DBCommands import *
import random


def survey_reactions(cases, reactions_result):
    text_result = ''
    survey_statistics = {}

    for i in range(len(cases)):
        text_result += f"{cases[i]} [{reactions_result[i]}]\n"
        survey_statistics.update({reactions_result[i]: 1})

    return text_result, survey_statistics


def is_console():
    def predicate(ctx):
        return ctx.message.channel == bot.get_channel(DirectoryModule_ShowDirectory(ctx.guild.id)[0])

    return commands.check(predicate)


@bot.event
async def on_raw_reaction_add(payload):
    if payload.message_id in show_SRV(payload.guild_id) and payload.member.bot is False:
        current_statistics = eval(get_SRV(payload.guild_id, payload.message_id))
        if str(payload.emoji) in list(current_statistics.keys()):
            current_statistics[str(payload.emoji)] += 1
            logs_output = DirectoryModule_ShowDirectory(payload.guild_id)[1]  # logs
            if not add_SRV(payload.guild_id, payload.message_id, current_statistics):
                await bot.get_channel(logs_output).send(
                    f"```Survey [{payload.message_id}] get {str(payload.emoji)} from {payload.member.name}```")
            else:
                await bot.get_channel(logs_output).send(f"```Error in survey [{payload.message_id}] reaction check!```")


@bot.event
async def on_raw_reaction_remove(payload):
    if payload.message_id in show_SRV(payload.guild_id):
        current_statistics = eval(get_SRV(payload.guild_id, payload.message_id))
        if str(payload.emoji) in list(current_statistics.keys()):
            current_statistics[str(payload.emoji)] -= 1
            logs_output = DirectoryModule_ShowDirectory(payload.guild_id)[1]  # logs
            if not add_SRV(payload.guild_id, payload.message_id, current_statistics):
                await bot.get_channel(logs_output).send(
                    f"```Survey [{payload.message_id}] lost {str(payload.emoji)}```")
            else:
                await bot.get_channel(logs_output).send(f"```Error in survey [{payload.message_id}] reaction check!```")


@bot.command()
@is_console()
async def set_survey(ctx, *, body):
    """Создание опроса"""

    survey_output = DirectoryModule_ShowDirectory(ctx.guild.id)[2]  # info
    logs_output = DirectoryModule_ShowDirectory(ctx.guild.id)[1]  # logs
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
    text, stats = survey_reactions(cases, reactions)
    # создаем тело опроса
    embed = discord.Embed(
        title=f"{title}",
        description=f"{text}",
        colour=discord.Colour.from_rgb(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    )
    survey_message = await bot.get_channel(survey_output).send(embed=embed)

    # проставляем реакции
    for emj in reactions:
        await survey_message.add_reaction(emj)

    # записываем в базу данных
    if not set_SRV(ctx.guild.id, str(bot.get_guild(ctx.guild.id).name), survey_message.id, title, str(stats)):
        await bot.get_channel(logs_output).send(
            f"```Survey [{survey_message.id}] [{title}] {reactions} is created successfully```")
    else:
        await bot.get_channel(logs_output).send(f"```Survey is not created successfully :(```")


@bot.command()
@is_console()
async def clear_survey(ctx, message_id: int):
    """Завершение опроса и вывод результатов"""

    info = DirectoryModule_ShowDirectory(ctx.guild.id)[2]  # info
    logs = DirectoryModule_ShowDirectory(ctx.guild.id)[1]  # logs
    channel = bot.get_channel(info)
    message = await channel.fetch_message(message_id)

    result = dict(eval(get_SRV(ctx.guild.id, message_id)))

    all_votes = sum(result.values())

    output = "Опрос закончился!\nРезультаты опроса:\n"
    for key in result:
        percentage = result[key] / all_votes * 100
        output += f"[{key}] - {result[key]} | {percentage:.1f}%\n"

    await message.reply(f"""```{output}```""")
    if not clear_SRV(ctx.guild.id, message_id):
        await bot.get_channel(logs).send(f"""```Survey with [id = {message_id}] deleted successfully```""")
    else:
        await bot.get_channel(logs).send(f"""```Survey with [id = {message_id}] doesn't deleted!```""")


@bot.command()
@is_console()
async def check_survey(ctx, message_id: int):
    """Проверка текущей статистики опроса"""

    result = dict(eval(get_SRV(ctx.guild.id, message_id)))
    all_votes = sum(result.values())

    output = "Текущие результаты опроса:\n"
    for key in result:
        percentage = result[key] / all_votes * 100
        output += f"[{key}] - {result[key]} | {percentage:.1f}%\n"

    await bot.get_channel(ctx.channel.id).send(f"""```{output}```""")


@bot.command()
@is_console()
async def hello_world(ctx):
    """Приветственное сообщение новичкам"""

    output = "**Привет всем новичкам!**\n" \
                     "Добро пожаловать на сервер _Центра Олимпиадного Программирования_ ЮУрГУ\n" \
                     "Центр олимпиадного программирования ЮУрГУ занимается подготовкой студентов к личным и командным соревнованиям по программированию.\n" \
                     "Программа подготовки студентов к участию в командных и личных соревнованиях по программированию рассчитана на **три года**. Каждый год соответствует уровню подготовки студента:\n" \
                     "\t**Уровень 1:** Программа «Базовая подготовка» рассчитана на студентов, которые только начинают заниматься олимпиадным программированием.\n" \
                     "\t**Уровень 2:** Программа «Олимпиадная подготовка» рассчитана на студентов, которые готовятся к выходу в полуфинал ACM ICPC.\n" \
                     "\t**Уровень 3:** Программа «Продвинутая олимпиадная подготовка» рассчитана на опытных студентов, которые готовы хорошо выступить на полуфинале и пройти в финал ACM ICPC."
    await bot.get_channel(973612910171533412).send(f"""{output}""")
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
    await bot.get_channel(973612910171533412).send(f"""{output}""")
    output = "**Особенности сервера**\n" \
             "\t1. Система социального рейтинга\n" \
             "\t2. Автоматизированное создание опросов\n" \
             "\t3. Автоматическое присвоение ролей согласно рейтингу\n" \
             "\t4. Распределение рабочих директорий для управления ботом\n" \
             "\t5. Перенос игры Wordle в Discord и собственный банк слов\n" \
             "\t6. Музыкальный бот\n"
    await bot.get_channel(973612910171533412).send(f"""{output}""")
    output = "```Нажимай на эту реакцию, и начинай программировать вместе с нами)```"
    message = await bot.get_channel(973612910171533412).send(f"""{output}""")
    await message.add_reaction("💻")

