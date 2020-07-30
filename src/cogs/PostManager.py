import discord
from discord.ext import commands


# Use decorators: @commands.command(), @commands.Cog.listener()
class PostManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='ping')
    @commands.is_owner()
    async def ping(self, ctx: commands.Context, *, member: discord.Member = None):
        member = member or ctx.author
        await ctx.send("<@{}> pong!".format(member.id))

    @ping.error
    async def ping_error(self, ctx: commands.Context, error: commands.CommandError):
        await ctx.send("{}".format(error))
