import os

from discord.ext import commands

from cogs import PostManager, Utils

if __name__ == "__main__":
    bot = commands.Bot(command_prefix='$')
    bot.add_cog(Utils(bot))
    bot.add_cog(PostManager(bot))
    bot.run(os.getenv("BOT_TOKEN"))
