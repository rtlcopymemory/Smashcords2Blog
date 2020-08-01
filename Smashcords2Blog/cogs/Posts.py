import discord
import psycopg2
from discord.ext import commands

from Smashcords2BlogBot import Smashcords2BlogBot
from cogs import is_mod
from database import categories


class Posts(commands.Cog):
    def __init__(self, bot):
        self.bot: Smashcords2BlogBot = bot
        self.temp_posts: dict = {}  # Dictionary mapping server id -> current embed

    @commands.command(name='createpost', usage="",
                      brief="Initiates a new post",
                      aliases=['newpost', 'new'])
    async def create_embed(self, ctx: commands.Context):
        if not is_mod(self.bot.conn, ctx):
            await ctx.send("You're not a mod")
            return
        self.temp_posts[ctx.guild.id] = discord.Embed(color=discord.Color.from_rgb(106, 252, 228))
        await ctx.send("New post initiated")

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

    @commands.command(name='listcategories', usage="name",
                      brief="Creates a new category",
                      aliases=['listcat', 'lc', 'categories'])
    async def list_categories(self, ctx: commands.Context):
        if not is_mod(self.bot.conn, ctx):
            await ctx.send("You're not a mod")
            return
        categories_list: list = categories.get_server_categories(self.bot.conn, ctx.guild.id)
        message: str = "Available categories:\n"
        for category in categories_list:
            message += "{}\n".format(category)
        await ctx.send(message)
