from config import *


class Channels(commands.Cog):
    @staticmethod
    def is_exists_(db_name, channel_id):
        with db:
            if db_name.select().where(db_name.id == channel_id):
                return True
            return False

    @staticmethod
    def print_out(db_name, name):
        channels = list(db_name.select())
        info = '\n'.join(f"`{channels.index(name) + 1}`** **`{name.chat}`** **" for name in channels)
        embed = discord.Embed(title=f'{name} list has been updated', description=info)
        return embed

    @commands.command(aliases=["add"])
    async def add_channel_(self, ctx):
        """Добавляет текстовый канал в базу данных и позволяет в нем играть в wordle"""
        if self.is_exists_(Chats, ctx.channel.id):
            await ctx.send(embed=discord.Embed(title='This channel isn\'t in database!'))
            return

        with db:
            Chats.create(chat=ctx.channel, id=ctx.channel.id)

        await ctx.send(embed=self.print_out(Chats, 'Wordle directory'))
        return

    @commands.command(aliases=["delete"])
    async def delete_channel_(self, ctx):
        """Удаляет текстовый канал из базы данных, что запрещает играть в нем в wordle"""
        if not self.is_exists_(Chats, ctx.channel.id):
            await ctx.send(embed=discord.Embed(title='This channel is already in database!'))
            return

        with db:
            Chats.get(Chats.id == ctx.channel.id).delete_instance()

        await ctx.send(embed=self.print_out(Chats, 'Wordle channel'))
        return

    @commands.command(aliases=['set'])
    async def set_logs_directory_(self, ctx):
        """Устанавливает текстовый канал, в котором будут логи"""
        if self.is_exists_(Logs, ctx.channel.id):
            await ctx.send(embed=discord.Embed(title='This channel is already in database!'))
            return

        with db:
            Logs.create(server=ctx.guild.name, chat=ctx.channel.name, id=ctx.channel.id)

        await ctx.send(embed=discord.Embed(title=f'Logs directory has been updated'))
        return

    @commands.command(aliases=['deldir'])
    async def delete_logs_directory_(self, ctx):
        """Удаляет текстовый канал, в котором логи"""
        if not self.is_exists_(Logs, ctx.channel.id):
            await ctx.send(embed=discord.Embed(title='This channel isn\'t in database!'))
            return

        with db:
            Logs.get(Logs.id == ctx.channel.id).delete_instance()

        await ctx.send(embed=discord.Embed(title=f'Logs directory has been updated'))
        return


def setup(client):
    client.add_cog(Channels(client))
