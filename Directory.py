from config import *


def is_console():
    def predicate(ctx):
        return ctx.message.channel == bot.get_channel(db.get_directory(ctx.guild.id).data[0])

    return commands.check(predicate)


def is_directory():
    def predicate(ctx):
        return ctx.message.channel.id in db.get_directory(ctx.guild.id).data

    return commands.check(predicate)


def is_any():
    def predicate(ctx):
        if not db.get_directory(ctx.guild.id).state:
            return True
        elif ctx.message.channel.id in db.get_directory(ctx.guild.id).data:
            return True
        return False

    return commands.check(predicate)


class DirectoryModule(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @is_any()
    @commands.command()
    async def autocd(self, ctx):
        """Автоматическая установка рабочих директорий"""
        role = await ctx.guild.create_role(name='Tech Personnel', colour=discord.Colour(0x8db6af),
                                           permissions=discord.Permissions(permissions=8))
        await ctx.message.author.add_roles(role)

        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            role: discord.PermissionOverwrite(read_messages=True)
        }

        category = await ctx.guild.create_category("Command line", overwrites=overwrites)
        console = await category.create_text_channel(f"console", overwrites=None)
        logs = await category.create_text_channel(f"logs", overwrites=None)
        info = await category.create_text_channel(f"info", overwrites=None)

        res = db.set_directory(ctx.guild.id, bot.get_guild(ctx.guild.id).name, console.id, logs.id, info.id)

        if res.state:
            await ctx.message.channel.send(f'```Рабочие директории изменены следующим образом:\n'
                                           f'Консоль: {bot.get_channel(console.id)}\n'
                                           f'Логи: {bot.get_channel(logs.id)}\n'
                                           f'Объявления: {bot.get_channel(info.id)}```')
            await console.send(f'```Этот канал теперь является рабочей директорией: [Консоль]```')
            await logs.send(f'```Этот канал теперь является рабочей директорией: [Логи]```')
            await info.send(f'```Этот канал теперь является рабочей директорией: [Объявления]```')
        else:
            await ctx.channel.send(f'```Что-то пошло не так 🤡```')

        await ctx.message.add_reaction('👀')

    @commands.command()
    @is_console()
    async def set_cd(self, ctx, console_id, log_id, info_id):
        """Ручная установка рабочих директорий"""
        console_id = int(console_id)
        log_id = int(log_id)
        info_id = int(info_id)

        res = db.set_directory(ctx.guild.id, bot.get_guild(ctx.guild.id).name, console_id, log_id, info_id)

        if res.state:
            await ctx.message.channel.send(f'```Рабочие директории изменены следующим образом:\n'
                                           f'Консоль: {bot.get_channel(console_id)}\n'
                                           f'Логи: {bot.get_channel(log_id)}\n'
                                           f'Объявления: {bot.get_channel(info_id)}```')
            await bot.get_channel(console_id).send(f'```Этот канал теперь является рабочей директорией: [Консоль]```')
            await bot.get_channel(log_id).send(f'```Этот канал теперь является рабочей директорией: [Логи]```')
            await bot.get_channel(info_id).send(f'```Этот канал теперь является рабочей директорией: [Объявления]```')
        else:
            await ctx.channel.send(f'```Что-то пошло не так 🤡```')

        await ctx.message.add_reaction('👀')

    @commands.command()
    @is_console()
    async def cd(self, ctx):
        """Вывод рабочих директорий"""

        res = db.get_directory(ctx.guild.id)

        if res.state:
            await ctx.message.channel.send(f'```Рабочие директории установлены следующим образом:\n'
                                           f'Консоль: {bot.get_channel(res.data[0])}\n'
                                           f'Логи: {bot.get_channel(res.data[1])}\n'
                                           f'Объявления: {bot.get_channel(res.data[2])}```')
        else:
            await ctx.channel.send(f'```Что-то пошло не так 🤡```')

        await ctx.message.add_reaction('👀')

    @commands.command()
    @is_directory()
    async def clear(self, ctx, amount=None):
        """Автоматическое удаление сообщений"""
        if amount == None:
            await ctx.channel.purge(limit=1000000)
        else:
            try:
                await ctx.channel.purge(limit=int(int(amount) + 1))
            except:
                pass

    @commands.command()
    @is_console()
    async def contest(self, ctx, time: int):
        """Временное создание категории для общения"""
        category = await ctx.guild.create_category("Contest time 🥳", overwrites=None, reason=None)
        chat = await category.create_text_channel(f"Chat", overwrites=None, reason=None)
        voice = await category.create_voice_channel(f"Voice", overwrites=None, reason=None)

        await asyncio.sleep(time)

        await chat.delete()
        await voice.delete()
        await category.delete()
