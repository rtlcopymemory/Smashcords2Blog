import psycopg2
from discord.ext import commands

from Smashcords2BlogBot import Smashcords2BlogBot
from cogs import is_mod
from database import categories


class Posts(commands.Cog):
    def __init__(self, bot):
        self.bot: Smashcords2BlogBot = bot

    @commands.command(name='createpost', usage="category",
                      brief="Initiates a new post",
                      aliases=['newpost', 'new'])
    async def create_embed(self, ctx: commands.Context, arg: str):
        if not is_mod(self.bot.conn, ctx):
            await ctx.send("You're not a mod")
            return

    @commands.command(name='createcategory', usage="name",
                      brief="Creates a new category",
                      aliases=['newcategory', 'newcat', 'addcat', 'addcategory'])
    async def create_category(self, ctx: commands.Context, arg: str):
        if not is_mod(self.bot.conn, ctx):
            await ctx.send("You're not a mod")
            return
        try:
            categories.add_category(self.bot.conn, ctx.guild.id, arg)
        except psycopg2.IntegrityError as err:
            await ctx.send("Error: {}".format(err))
            self.bot.conn.rollback()
            return
        await ctx.send("Category `{}` successfully created".format(arg))
