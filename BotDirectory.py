from config import *
from DBCommands import *


@bot.command()
async def set_cd(ctx, console_id, log_id, info_id):
    """
        Эта команда устанавливает рабочие директории для бота, где он будет считывать сообщения, писать логи отработки
        команд, выводить информацию.
    """
    console_id = int(console_id)
    log_id = int(log_id)
    info_id = int(info_id)

    res = DirectoryModule_SetDirectory(ctx.guild.id, str(bot.get_guild(ctx.guild.id).name), console_id, log_id, info_id)

    await ctx.message.channel.send(f'```Рабочие директории изменены следующим образом:\n'
                                   f'Консоль: {bot.get_channel(console_id)}\n'
                                   f'Логи: {bot.get_channel(log_id)}\n'
                                   f'Объявления: {bot.get_channel(info_id)}```')
    await bot.get_channel(console_id).send(f'```Этот канал теперь является рабочей директорией: [Консоль]```')
    await bot.get_channel(log_id).send(f'```Этот канал теперь является рабочей директорией: [Логи]```')
    await bot.get_channel(info_id).send(f'```Этот канал теперь является рабочей директорией: [Объявления]```')


@bot.command()
async def cd(ctx):
    """
        Эта команда устанавливает рабочие директории для бота, где он будет считывать сообщения, писать логи отработки
        команд, выводить информацию.
    """

    res = DirectoryModule_ShowDirectory(ctx.guild.id)

    await ctx.message.channel.send(f'```Рабочие директории изменены следующим образом:\n'
                                   f'Консоль: {bot.get_channel(res[0])}\n'
                                   f'Логи: {bot.get_channel(res[1])}\n'
                                   f'Объявления: {bot.get_channel(res[2])}```')