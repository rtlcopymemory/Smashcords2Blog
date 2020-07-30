import discord
from discord.ext import commands


class Utils(commands.Cog):
    def __init__(self, bot):
        self.bot: discord.Client = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Connected!\nUsername: {}".format(self.bot.user.name))
