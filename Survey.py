from config import *
import time


def is_console():
    def predicate(ctx):
        try:
            return ctx.message.channel == bot.get_channel(db.get_directory(ctx.guild.id).data[0])
        except:
            return True
    return commands.check(predicate)


class SurveyModule(commands.Cog):
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

    @commands.command(aliases=['ss'])
    @is_console()
    async def set_survey(self, ctx, *, body):
        """Создание опроса"""
        def generator(counter):
            """Генератор реакций"""
            output = []
            i = 0
            while i < counter:
                new_emoji = random.choice(all_reactions)
                if new_emoji not in output:
                    i += 1
                    output.append(new_emoji)
            print(output)
            return output

        def survey_body(case, reactions_result):
            """Компоновщик текста опроса"""
            text_result = ''
            survey_statistics = {}

            for i in range(len(case)):
                text_result += f"{case[i]} [{reactions_result[i]}]\n"
                survey_statistics.update({reactions_result[i]: 1})

            return text_result, survey_statistics

        logs, info = db.get_directory(ctx.guild.id).data[1:]  # находим чаты логов и вывода
        title, *cases = body.strip().split('\n')              # парсим на заголовок и положения
        if len(cases) > 20:
            await bot.get_channel(logs).send(f"```Survey is not created successfully```")
            return None
        reactions = generator(len(cases))                     # генерируем реакции

        # создаем текст опроса и генерируем первоначальную статистику
        text, stats = survey_body(cases, reactions)

        # создаем тело опроса
        embed = discord.Embed(
            title=f"{title}",
            description=f"{text}",
            colour=discord.Colour.from_rgb(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        )
        survey_message = await bot.get_channel(info).send(embed=embed)
        await ctx.message.add_reaction('🥉')                  # статус "Окей"

        # проставляем реакции
        for emj in reactions:
            await survey_message.add_reaction(emj)
        await ctx.message.add_reaction('🥈')                  # статус "Окей"

        # записываем в базу данных
        result = db.set_survey(ctx.guild.id, bot.get_guild(ctx.guild.id).name, survey_message.id, title, stats)
        if result.state:
            await ctx.message.add_reaction('🥇')              # статус "Окей"
            await bot.get_channel(logs).send(
                f"```Survey [{survey_message.id}] [{title}] {reactions} is created successfully```")
        else:
            await bot.get_channel(logs).send(f"```Survey is not created successfully```")

    @commands.command(aliases=['sc'])
    @is_console()
    async def clear_survey(self, ctx, message_id: int):
        """Завершение опроса и вывод результатов"""

        logs, info = db.get_directory(ctx.guild.id).data[1:]
        channel = bot.get_channel(info)
        message = await channel.fetch_message(message_id)

        result = dict(eval(db.get_survey(ctx.guild.id).data[message_id][1]))

        all_votes = sum(result.values())

        output = "Опрос закончился!\nРезультаты опроса:\n"
        for key in result:
            percentage = result[key] / all_votes * 100
            output += f"{percentage:4.1f}% | {result[key]} - [{key}]\n"

        await message.reply(f"""```{output}```""")

        res = db.clr_survey(ctx.guild.id, message_id)
        if res.state:
            await bot.get_channel(logs).send(f"""```Survey with [id = {message_id}] deleted successfully```""")
        else:
            await bot.get_channel(logs).send(f"""```Survey with [id = {message_id}] doesn't deleted!```""")

    @commands.command(aliases=['chk'])
    @is_console()
    async def check_survey(self, ctx, message_id: int):
        """Проверка текущей статистики опроса"""

        res = db.get_survey(ctx.guild.id)
        survey_dict = eval(res.data[message_id][1])
        all_votes = sum(survey_dict.values())

        output = "Текущие результаты опроса:\n"
        for key in survey_dict:
            percentage = survey_dict[key] / all_votes * 100
            output += f"{percentage:4.1f}% | {survey_dict[key]} - [{key}]\n"

        await bot.get_channel(ctx.channel.id).send(f"""```{output}```""")

    @commands.command(aliases=['sg'])
    @is_console()
    async def get_survey(self, ctx):
        """Вывод всех текущих опросов на сервере"""
        channel_id = ctx.channel.id
        res = db.get_survey(ctx.guild.id)
        surveys = res.data
        output = ""
        for key in surveys:
            emojis = ''.join(eval(surveys[key][1]).keys())
            new_pos = f"[{key}]\t[{surveys[key][0]}]\t[{emojis}]\n"
            if len(output) + len(new_pos) >= 2000:
                await bot.get_channel(channel_id).send(f"```{output}```")
                output = ""
            output += new_pos
        await bot.get_channel(channel_id).send(f"```{output}```")
