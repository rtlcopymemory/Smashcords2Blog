import os
import typing
from pathlib import Path

import discord
import psycopg2
from discord.ext import commands

from Smashcords2BlogBot import Smashcords2BlogBot
from cogs import is_mod
from config import frontmatter, owner_id, blog_path
from database import categories, posts
from database.posts import get_server_posts


def create_md_file(path, filename, title, subtitle, content):
    Path("{}".format(path)).mkdir(parents=True, exist_ok=True)
    with open("{}/{}".format(path, filename), "w+") as f:
        f.write(frontmatter.format(title))
        f.write("## {}\n".format(subtitle))
        f.write(content)


class Posts(commands.Cog):
    def __init__(self, bot):
        self.bot: Smashcords2BlogBot = bot
        # The following is a dictionary mapping the server ID to a tuple containing the currently edited embed
        # and the list of messages it references
        self.temp_posts: typing.Dict[int, typing.Tuple[discord.Embed, typing.List[discord.Message]]] = {}

    @commands.command(name='newpost', usage="", brief="Initiates a new post", aliases=['new'])
    async def create_embed(self, ctx: commands.Context):
        if not is_mod(self.bot.conn, ctx):
            await ctx.send("You're not a mod")
            return
        self.temp_posts[ctx.guild.id] = (discord.Embed(color=discord.Color.from_rgb(106, 252, 228)), [])
        await ctx.send("New post initiated\nSet up a **title**, the **content** and then **public** it to a category!")

    @commands.command(name='createcategory', usage="name", brief="Creates a new category",
                      aliases=['newcategory', 'newcat', 'addcat', 'addcategory'])
    async def create_category(self, ctx: commands.Context, *args: str):
        if not is_mod(self.bot.conn, ctx):
            await ctx.send("You're not a mod")
            return
        arg: str = ' '.join(args)
        try:
            categories.add_category(self.bot.conn, ctx.guild.id, arg)
        except psycopg2.IntegrityError as err:
            await ctx.send("Error: {}".format(err))
            self.bot.conn.rollback()
            return
        await ctx.send("Category `{}` successfully created".format(arg))

    @commands.command(name='listcategories', usage="", brief="Lists all categories",
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

    @commands.command(name='removecategory', usage="name", brief="Removes a category",
                      aliases=['deletecategory', 'rmcat', 'yeetcat'])
    async def remove_category(self, ctx: commands.Context, *args: str):
        if not is_mod(self.bot.conn, ctx):
            await ctx.send("You're not a mod")
            return
        arg: str = ' '.join(args)
        categories_list: list = categories.get_server_categories(self.bot.conn, ctx.guild.id)
        if arg not in categories_list:
            await ctx.send("Category does not exist")
            return
        categories.remove_category(self.bot.conn, ctx.guild.id, arg)
        await ctx.send("Category `{}` successfully removed".format(arg))

    @commands.command(name='settitle', usage="name", brief="Sets the title of the current post", aliases=['title'])
    async def title(self, ctx: commands.Context, *args: str):
        if not is_mod(self.bot.conn, ctx):
            await ctx.send("You're not a mod")
            return
        self.temp_posts[ctx.guild.id][0].title = ' '.join(args)
        await ctx.send("Post edited", embed=self.temp_posts[ctx.guild.id][0])

    @title.error
    async def title_error(self, ctx: commands.Context, error: commands.CommandInvokeError):
        if isinstance(error.original, KeyError):
            await ctx.send("Please, create the post first using the `new` command")

    @commands.command(name='setcontent', usage="message IDs", brief="Sets the content of the post",
                      help="Accepts multiple IDs at once, they need to be in order from top to bottom",
                      aliases=['content'])
    async def content(self, ctx: commands.Context, *args: str):
        if not is_mod(self.bot.conn, ctx):
            await ctx.send("You're not a mod")
            return
        current_tuple: typing.Tuple[discord.Embed, typing.List[discord.Message]] = self.temp_posts[ctx.guild.id]
        for messageID in args:
            try:
                current_tuple[1].append(await ctx.channel.fetch_message(int(messageID)))
            except Exception as e:
                await ctx.send("Error while adding the message with ID {}\n{}".format(messageID, e))
        embed_content = '\n'.join([str(message.jump_url) for message in self.temp_posts[ctx.guild.id][1]])
        current_tuple[0].clear_fields()
        current_tuple[0].add_field(name="content", value=embed_content)
        await ctx.send(embed=current_tuple[0])
        self.temp_posts[ctx.guild.id] = current_tuple  # not sure if needed since im not doing a deep copy

    @content.error
    async def content_error(self, ctx: commands.Context, error: commands.CommandInvokeError):
        if isinstance(error.original, KeyError):
            await ctx.send("Please, create the post first using the `new` command")

    @commands.command(name='preview', usage="category", brief="previews the .md file", aliases=['sendpreview'])
    async def preview(self, ctx: commands.Context, subtitle):
        if not is_mod(self.bot.conn, ctx):
            await ctx.send("You're not a mod")
            return
        categories_list: list = categories.get_server_categories(self.bot.conn, ctx.guild.id)
        if subtitle not in categories_list:
            await ctx.send("Category {} does not exist".format(subtitle))
            return
        title: str = self.temp_posts[ctx.guild.id][0].title
        content: str = '\n'.join([message.content for message in self.temp_posts[ctx.guild.id][1]])
        content = content.replace("\n", "  \n")
        create_md_file(path=".", filename="{}.md".format(ctx.guild.name), title=title, subtitle=subtitle,
                       content=content)
        await ctx.send(file=discord.File("{}.md".format(ctx.guild.name)))
        os.remove("{}.md".format(ctx.guild.name))

    @preview.error
    async def preview_error(self, ctx: commands.Context, error: commands.CommandError):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please provide the category")
        elif isinstance(error, commands.CommandInvokeError):
            if isinstance(error.original, KeyError):
                await ctx.send("Please, create the post first using the `new` command")

    @commands.command(name='publish', usage="category", brief="Publish the post on the blog",
                      aliases=['finish', 'submit'])
    async def publish(self, ctx: commands.Context, subtitle):
        if not is_mod(self.bot.conn, ctx):
            await ctx.send("You're not a mod")
            return

        categories_list: list = categories.get_server_categories(self.bot.conn, ctx.guild.id)
        if subtitle not in categories_list:
            await ctx.send("Category {} does not exist".format(subtitle))
            return

        title: str = self.temp_posts[ctx.guild.id][0].title
        content: str = '\n'.join([message.content for message in self.temp_posts[ctx.guild.id][1]])
        content = content.replace("\n", "  \n")

        try:
            posts.add_post(self.bot.conn, ctx.guild.id, subtitle, title, subtitle, content)
        except psycopg2.IntegrityError as err:
            await ctx.send("Error: {}".format(err))
            self.bot.conn.rollback()
            return

        create_md_file(path=blog_path.format(ctx.guild.name) + "{}".format(subtitle),
                       filename="{}.md".format(title),
                       title=title,
                       subtitle=subtitle, content=content)

        self.temp_posts.pop(ctx.guild.id)
        await ctx.send("Post submitted to blog")

    @publish.error
    async def publish_error(self, ctx: commands.Context, error: commands.CommandError):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please provide the category")
        elif isinstance(error, commands.CommandInvokeError):
            if isinstance(error.original, KeyError):
                await ctx.send("Please, create the post first using the `new` command")

    @commands.command(name='build', usage="", brief="[BOT OWNER ONLY] Re-builds the blog from the database entries",
                      aliases=['rebuild'])
    async def build_from_db(self, ctx: commands.Context):
        if not ctx.author.id == owner_id:
            await ctx.send("You're not the owner of this bot")
            return
        for post in get_server_posts(self.bot.conn, ctx.guild.id):
            create_md_file(path=blog_path.format(ctx.guild.name) + "{}".format(post[1]),
                           filename="{}.md".format(post[2]),
                           title=post[2],
                           subtitle=post[1],
                           content=post[4])
        await ctx.send("Done.")

    @build_from_db.error
    async def build_from_db_error(self, ctx: commands.Context, error: commands.CommandInvokeError):
        await ctx.send("Something went wrong:\n```{}```".format(error))
