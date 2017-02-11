from discord.ext import commands
from cogs.utils import checks
import datetime
from cogs.utils.dataIO import fileIO
import discord
import asyncio
import os
from random import choice, randint

inv_settings = {"Channel": None, "toggleedit": False, "toggledelete": False, "toggleuser": False, "toggleroles": False,
                "togglevoice": False,
                "toggleban": False}


class invitemirror:
    def __init__(self, bot):
        self.bot = bot
        self.direct = "data/modlogset/settings.json"

    @checks.admin_or_permissions(administrator=True)
    @commands.group(name='modlogtoggle', pass_context=True, no_pm=True)
    async def modlogtoggles(self, ctx):
        """toggle which server activity to log"""
        if ctx.invoked_subcommand is None:
            db = fileIO(self.direct, "load")
            embed=discord.Embed(description="""{}modlogtoggle

toggle which server activity to log

Commands:
  ban    toggle notifications when a user is banned
  delete toggle notifications when a member delete theyre message
  edit   toggle notifications when a member edits theyre message
  roles  toggle notifications when roles change
  user   toggle notifications when a user changes his profile
  voice  toggle notifications when voice status change""".format(ctx.prefix), colour=discord.Colour.blue())
            try:
                embed.add_field(name="Current settings:", value="Edit: {}\nDelete: {}\nUser: {}\nRoles: {}\nVoice: {}\nBan: {}".format(str(db[ctx.message.server.id]['toggleedit']), str(db[ctx.message.server.id]['toggledelete']), str(db[ctx.message.server.id]['toggleuser']), str(db[ctx.message.server.id]['toggleroles']), str(db[ctx.message.server.id]['togglevoice']), str(db[ctx.message.server.id]['toggleban'])))
            except KeyError:
                return
        await self.bot.say(embed=embed)

    @checks.admin_or_permissions(administrator=True)
    @commands.group(pass_context=True, name='modlogset', no_pm=True)
    async def modlogset(self, ctx):
        """Change modlog settings"""
        if ctx.invoked_subcommand is None:
            await self.bot.send_cmd_help(ctx)

    @modlogset.command(pass_context=True, name='channel', no_pm=True)
    async def channel(self, ctx):
        """Set the channel to send notifications too"""
        server = ctx.message.server
        db = fileIO(self.direct, "load")
        if ctx.message.server.me.permissions_in(ctx.message.channel).send_messages:
            if server.id in db:
                db[server.id]['Channel'] = ctx.message.channel.id
                fileIO(self.direct, "save", db)
                await self.bot.say("Channel changed.")
                return
            if not server.id in db:
                db[server.id] = inv_settings
                db[server.id]["Channel"] = ctx.message.channel.id
                fileIO(self.direct, "save", db)
                await self.bot.say("I will now send toggled modlog notifications here")
        else:
            return

    @modlogset.command(name='disable', pass_context=True, no_pm=True)
    async def disable(self, ctx):
        """disables the modlog"""
        server = ctx.message.server
        db = fileIO(self.direct, "load")
        if not server.id in db:
            await self.bot.say("Server not found, use modlogset to set a channnel")
            return
        del db[server.id]
        fileIO(self.direct, "save", db)
        await self.bot.say("I will no longer send modlog notifications here")

    @modlogtoggles.command(name='edit', pass_context=True, no_pm=True)
    async def edit(self, ctx):
        """toggle notifications when a member edits theyre message"""
        server = ctx.message.server
        db = fileIO(self.direct, "load")
        if db[server.id]["toggleedit"] == False:
            db[server.id]["toggleedit"] = True
            fileIO(self.direct, "save", db)
            await self.bot.say("Edit messages enabled")
        elif db[server.id]["toggleedit"] == True:
            db[server.id]["toggleedit"] = False
            fileIO(self.direct, "save", db)
            await self.bot.say("Edit messages disabled")

    @modlogtoggles.command(name='delete', pass_context=True, no_pm=True)
    async def delete(self, ctx):
        """toggle notifications when a member delete theyre message"""
        server = ctx.message.server
        db = fileIO(self.direct, "load")
        if db[server.id]["toggledelete"] == False:
            db[server.id]["toggledelete"] = True
            fileIO(self.direct, "save", db)
            await self.bot.say("Delete messages enabled")
        elif db[server.id]["toggledelete"] == True:
            db[server.id]["toggledelete"] = False
            fileIO(self.direct, "save", db)
            await self.bot.say("Delete messages disabled")

    @modlogtoggles.command(name='user', pass_context=True, no_pm=True)
    async def user(self, ctx):
        """toggle notifications when a user changes his profile"""
        server = ctx.message.server
        db = fileIO(self.direct, "load")
        if db[server.id]["toggleuser"] == False:
            db[server.id]["toggleuser"] = True
            fileIO(self.direct, "save", db)
            await self.bot.say("User messages enabled")
        elif db[server.id]["toggleuser"] == True:
            db[server.id]["toggleuser"] = False
            fileIO(self.direct, "save", db)
            await self.bot.say("User messages disabled")

    @modlogtoggles.command(name='roles', pass_context=True, no_pm=True)
    async def roles(self, ctx):
        """toggle notifications when roles change"""
        server = ctx.message.server
        db = fileIO(self.direct, "load")
        if db[server.id]["toggleroles"] == False:
            db[server.id]["toggleroles"] = True
            fileIO(self.direct, "save", db)
            await self.bot.say("Role messages enabled")
        elif db[server.id]["toggleroles"] == True:
            db[server.id]["toggleroles"] = False
            fileIO(self.direct, "save", db)
            await self.bot.say("Role messages disabled")

    @modlogtoggles.command(name='voice', pass_context=True, no_pm=True)
    async def voice(self, ctx):
        """toggle notifications when voice status change"""
        server = ctx.message.server
        db = fileIO(self.direct, "load")
        if db[server.id]["togglevoice"] == False:
            db[server.id]["togglevoice"] = True
            fileIO(self.direct, "save", db)
            await self.bot.say("Voice messages enabled")
        elif db[server.id]["togglevoice"] == True:
            db[server.id]["togglevoice"] = False
            fileIO(self.direct, "save", db)
            await self.bot.say("Voice messages disabled")

    @modlogtoggles.command(name='ban', pass_context=True, no_pm=True)
    async def ban(self, ctx):
        """toggle notifications when a user is banned"""
        server = ctx.message.server
        db = fileIO(self.direct, "load")
        if db[server.id]["toggleban"] == False:
            db[server.id]["toggleban"] = True
            fileIO(self.direct, "save", db)
            await self.bot.say("Ban messages enabled")
        elif db[server.id]["toggleban"] == True:
            db[server.id]["toggleban"] = False
            fileIO(self.direct, "save", db)
            await self.bot.say("Ban messages disabled")

    async def on_message_delete(self, message):
        server = message.server
        db = fileIO(self.direct, "load")
        if not server.id in db:
            return
        if db[server.id]['toggledelete'] == False:
            return
        if message.author is message.author.bot:
            pass
        channel = db[server.id]["Channel"]
        time = datetime.datetime.now()
        fmt = '%H:%M:%S'
        delete = discord.Embed(colour=discord.Colour.blue())
        delete.set_author(name="A message by {} has been deleted!".format(message.author), icon_url=message.author.avatar_url)
        delete.add_field(name="Channel", value=message.channel.mention)
        delete.add_field(name="Time", value=time.strftime(fmt))
        delete.add_field(name="Message", value=message.content, inline=False)
        delete.set_footer(text="User ID: {}.".format(message.author.id))
        await self.bot.send_message(server.get_channel(channel),
                                    embed=delete)

    async def on_message_edit(self, before, after):
        server = before.server
        db = fileIO(self.direct, "load")
        if not server.id in db:
            return
        if db[server.id]['toggleedit'] == False:
            return
        if before.content == after.content:
            return
        if before.author.bot:
            return
        channel = db[server.id]["Channel"]
        time = datetime.datetime.now()
        fmt = '%H:%M:%S'
        edit = discord.Embed(colour=discord.Colour.blue())
        edit.set_author(name="A message by {} has been edited!".format(before.author), icon_url=before.author.avatar_url)
        edit.add_field(name="Channel", value=before.channel.mention)
        edit.add_field(name="Time", value=time.strftime(fmt))
        edit.add_field(name="Message Before", value=before.content, inline=False)
        edit.add_field(name="Message After", value=after.content, inline=False)
        edit.set_footer(text="User ID: {}.".format(before.author.id))
        await self.bot.send_message(server.get_channel(channel),
                                    embed=edit)

    async def on_voice_state_update(self, before, after):
        server = before.server
        db = fileIO(self.direct, "load")
        if not server.id in db:
            return
        if db[server.id]['togglevoice'] == False:
            return
        if before.bot:
            return
        channel = db[server.id]["Channel"]
        time = datetime.datetime.now()
        fmt = '%H:%M:%S'
        voice=discord.Embed(colour=discord.Colour.blue())
        voice.set_author(name="{} has updated thier voice state!".format(before.name), icon_url=before.avatar_url)
        voice.add_field(name="Time", value=time.strftime(fmt))
        voice.add_field(name="User ID", value="{}".format(before.id))
        voice.add_field(name="Voice Before", value=before.voice_channel, inline=False)
        voice.add_field(name="Voice After", value=after.voice_channel, inline=False)
        await self.bot.send_message(server.get_channel(channel),
                                    embed=voice)

    async def on_member_update(self, before, after):
        server = before.server
        db = fileIO(self.direct, "load")
        if not server.id in db:
            return
        if db[server.id]['toggleuser'] and db[server.id]['toggleroles'] == False:
            return
        channel = db[server.id]["Channel"]
        time = datetime.datetime.now()
        fmt = '%H:%M:%S'
        if not before.nick == after.nick:
            nickname=discord.Embed(colour=discord.Colour.blue())
            nickname.set_author(name="{}'s nickname has changed!".format(before.name), icon_url=before.avatar_url)
            nickname.add_field(name="Time", value=time.strftime(fmt))
            nickname.add_field(name="User ID", value="{}".format(before.id))
            nickname.add_field(name="Nick Before", value=before.nici, inline=False)
            nickname.add_field(name="Nick After", value=after.nick, inline=False) 
            await self.bot.send_message(server.get_channel(channel),
                                        embed=nickname)

    async def on_member_update(self, before, after):
        server = before.server
        db = fileIO(self.direct, "load")
        if not server.id in db:
            return
        if db[server.id]['toggleuser'] and db[server.id]['toggleroles'] == False:
            return
        channel = db[server.id]["Channel"]
        time = datetime.datetime.now()
        fmt = '%H:%M:%S'
        if not before.roles == after.roles:
            roles=discord.Embed(colour=discord.Colour.blue())
            roles.set_author(name="{}'s roles have changed!".format(before.name), icon_url=before.avatar_url)
            roles.add_field(name="Time", value=time.strftime(fmt))
            roles.add_field(name="User ID", value="{}".format(before.id))
            roles.add_field(name="Roles Before", value=", ".join([r.name for r in before.roles if r.name != "@everyone"]), inline=False)
            roles.add_field(name="Roles After", value=", ".join([r.name for r in after.roles if r.name != "@everyone"]), inline=False)            
            await self.bot.send_message(server.get_channel(channel),
                                        embed=roles)

    async def on_member_ban(self, member, before):
        server = before.server
        db = fileIO(self.direct, "load")
        if not server.id in db:
            return
        if db[server.id]['toggleuser'] == False:
            return
        channel = db[server.id]["Channel"]
        time = datetime.datetime.now()
        fmt = '%H:%M:%S'
        ban = discord.Embed(colour=discord.Colour.blue())
        ban.add_field(name="Status", value="Ban")
        ban.add_field(name="User", value=member)
        ban.add_field(name="User ID", value=member.id)
        ban.add_field(name="Time", value=time.strftime(fmt))
        await self.bot.send_message(server.get_channel(channel),
                                    embed=ban)


def check_folder():
    if not os.path.exists('data/modlogset'):
        print('Creating data/modlogset folder...')
        os.makedirs('data/modlogset')


def check_file():
    f = 'data/modlogset/settings.json'
    if not fileIO(f, 'check'):
        print('Creating default settings.json...')
        fileIO(f, 'save', {})


def setup(bot):
    check_folder()
    check_file()
    bot.add_cog(invitemirror(bot))
