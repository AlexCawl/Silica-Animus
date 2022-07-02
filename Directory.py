from config import *


def is_console():
    def predicate(ctx):
        return ctx.message.channel == bot.get_channel(db.get_directory(ctx.guild.id).data[0])

    return commands.check(predicate)


class DirectoryModule(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def set_cd(self, ctx, console_id, log_id, info_id):
        """
            Установка рабочих директорий
        """
        console_id = int(console_id)
        log_id = int(log_id)
        info_id = int(info_id)

        res = db.set_directory(ctx.guild.id, bot.get_guild(ctx.guild.id).name, console_id, log_id, info_id)

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
            Вывод рабочих директорий
        """

        res = db.get_directory(ctx.guild.id)

        await ctx.message.channel.send(f'```Рабочие директории установлены следующим образом:\n'
                                       f'Консоль: {bot.get_channel(res.data[0])}\n'
                                       f'Логи: {bot.get_channel(res.data[1])}\n'
                                       f'Объявления: {bot.get_channel(res.data[2])}```')