from discord.ext import commands


# Use decorators: @commands.command(), @commands.Cog.listener()
class PostManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
