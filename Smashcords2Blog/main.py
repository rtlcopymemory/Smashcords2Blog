import os

import psycopg2

from Smashcords2BlogBot import Smashcords2BlogBot
from cogs import PermissionsManager, Utils
from cogs.Posts import Posts

if __name__ == "__main__":
    connection = psycopg2.connect(dbname=os.getenv("DBNAME"), user=os.getenv("DBUSER"), password=os.getenv("DBPASS"),
                                  host=os.getenv("DBHOST"), port=os.getenv("DBPORT"))
    bot = Smashcords2BlogBot(connection, command_prefix='$')
    bot.add_cog(Utils(bot))
    bot.add_cog(PermissionsManager(bot))
    bot.add_cog(Posts(bot))
    bot.run(os.getenv("BOT_TOKEN"))
