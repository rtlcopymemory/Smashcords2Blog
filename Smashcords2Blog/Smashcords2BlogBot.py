from discord.ext import commands


class Smashcords2BlogBot(commands.Bot):
    def __init__(self, conn, **kwargs):
        super(Smashcords2BlogBot, self).__init__(**kwargs)
        self.conn = conn
