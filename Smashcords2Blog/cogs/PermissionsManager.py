import discord
import psycopg2
from discord.ext import commands

from Smashcords2BlogBot import Smashcords2BlogBot
from database import roles


def roles_from_context(ctx: commands.Context) -> list:
    args: list = ctx.message.content
    roles_list: list = ctx.guild.roles
    return [role for role in roles_list if role.name in args]


def is_mod(conn, ctx: commands.Context):
    author_roles: list = ctx.author.roles
    server_id = ctx.guild.id
    allowed_roles: list = roles.get_server_roles(conn, server_id)
    return any([role for role in author_roles if role.id in allowed_roles])


class PermissionsManager(commands.Cog):
    def __init__(self, bot):
        self.bot: Smashcords2BlogBot = bot

    @commands.command(name='allow', usage="<list of role names>",
                      brief="Adds a list of roles to the mods list of this server", aliases=['add', 'addmod'])
    @commands.is_owner()
    async def allow(self, ctx: commands.Context):
        guild: discord.Guild = ctx.guild
        added: str = ""
        roles_list: list = roles_from_context(ctx)
        role: discord.Role
        for role in roles_list:
            try:
                roles.add_role(self.bot.conn, guild.id, role.id)
                added += " " + role.name
            except psycopg2.IntegrityError:
                await ctx.send("Duplicated item: {}".format(role.name))
            finally:
                self.bot.conn.commit()
        await ctx.send("Added the following roles:\n`{}`".format(added))

    @allow.error
    async def allow_error(self, ctx: commands.Context, error: commands.CommandError):
        if isinstance(error, commands.NotOwner):
            await ctx.send("Sorry, this command is reserved for the owner only")
        print(error)

    @commands.command(name='mods', usage="", brief="lists mod roles for this server", aliases=['showmods', 'listmods'])
    async def mods(self, ctx: commands.Context):
        if not is_mod(self.bot.conn, ctx):
            await ctx.send("You're not a mod")
            return
        allowed_roles: list = roles.get_server_roles(self.bot.conn, ctx.guild.id)
        message: str = "Allowed Roles: "
        for role in allowed_roles:
            message += ctx.guild.get_role(int(role)).name + ", "
        await ctx.send(message[:-2])

    @commands.command(name='revoke', usage="<list of role names>",
                      brief="Removes a list of roles from the mods list of this server",
                      aliases=['remove', 'removemod', 'rmmod'])
    @commands.is_owner()
    async def revoke(self, ctx: commands.Context):
        guild: discord.Guild = ctx.guild
        removed: str = ""
        roles_list: list = roles_from_context(ctx)
        role: discord.Role
        for role in roles_list:
            roles.remove_role(self.bot.conn, guild.id, role.id)
            removed += " " + role.name
        await ctx.send("Removed the following roles:\n`{}`".format(removed))
