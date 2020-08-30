import shutil

import discord
from discord.ext import commands

import config
from Smashcords2BlogBot import Smashcords2BlogBot
from database import server


class Utils(commands.Cog):
    def __init__(self, bot):
        self.bot: Smashcords2BlogBot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Connected!\nUsername: {}".format(self.bot.user.name))
        await self.bot.change_presence(
            activity=discord.Activity(type=discord.ActivityType.watching, name="$help for a list of commands"))

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        try:
            server.add_server(self.bot.conn, guild.id, guild.name)
        except Exception as e:
            print("[ERROR] Server not added to the database.\nError: {}".format(e))
        try:
            shutil.copytree("./hugo-template", config.hugo_root.format(guild.name))
        except shutil.Error as e:
            print('[ERROR] Directory not copied.\nError: {}'.format(e))
        except OSError as e:
            print('[ERROR] Directory not copied.\nError: {}'.format(e))

    @commands.Cog.listener()
    async def on_guild_leave(self, guild: discord.Guild):
        server.remove_server(self.bot.conn, guild.id)

    @commands.command(name='ping', usage="", brief="answers with a simple message", aliases=['up'])
    async def ping(self, ctx: commands.Context, *, member: discord.Member = None):
        member = member or ctx.author
        await ctx.send("<@{}> pong!".format(member.id))

    @commands.command(name='commands', usage="", brief="Github link to the commands list", aliases=['listcommands'])
    async def commands(self, ctx: commands.Context, *, member: discord.Member = None):
        await ctx.send("List of commands: <https://github.com/WolfenCLI/Smashcords2Blog/wiki/Commands>")
