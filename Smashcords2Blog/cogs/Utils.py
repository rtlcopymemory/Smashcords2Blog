import discord
from discord.ext import commands

from Smashcords2BlogBot import Smashcords2BlogBot
from database import server


class Utils(commands.Cog):
    def __init__(self, bot):
        self.bot: Smashcords2BlogBot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Connected!\nUsername: {}".format(self.bot.user.name))
        await self.bot.change_presence(activity=discord.CustomActivity("Prefix: $"))

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        server.add_server(self.bot.conn, guild.id, guild.name)

    @commands.command(name='ping')
    async def ping(self, ctx: commands.Context, *, member: discord.Member = None):
        member = member or ctx.author
        await ctx.send("<@{}> pong!".format(member.id))
