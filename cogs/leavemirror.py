from discord.ext import commands
from cogs.utils import checks
from cogs.utils.dataIO import dataIO
from random import choice, randint
import discord
from random import choice
import os
from datetime import datetime
import datetime

JSON = 'leavemirror/settings.json'


class MessageMirror:
    def __init__(self, bot):
        self.bot = bot
        self.settings = dataIO.load_json(JSON)

    def save(self):
        dataIO.save_json(JSON, self.settings)

    @checks.is_owner()
    @commands.group(name='leavemirror', pass_context=True)
    async def servermonitor(self, ctx):
        """Configure message mirror cog"""
        if ctx.invoked_subcommand is None:
            await self.bot.send_cmd_help(ctx)

    @servermonitor.command(name='toggle')
    async def mtoggle(self, on_off: bool=None):
        if on_off is None:
            on_off = self.settings.get('enabled')
            adv = 'currently'
        else:
            self.settings['enabled'] = on_off
            self.save()
            adv = 'now'
        adj = 'enabled' if on_off else 'disabled'
        await self.bot.say('Leave / join mirror is %s %s' % (adv, adj))

    @servermonitor.command(name='channel', pass_context=True)
    async def mchannel(self, ctx, channel: discord.Channel=None):
        if not channel:
            channel_id = self.settings.get('channel')
            if not channel_id:
                await self.bot.say('Mirror channel is not set.')
                return
            channel = self.bot.get_channel(channel_id)
            if not channel:
                await self.bot.say('Mirror channel not found. Maybe deleted?')
                return
            await self.bot.say('Messages are mirrored to %s in %s' %
                               (channel, channel.server))
            return
        self.settings['channel'] = channel.id
        self.save()
        await self.bot.say('Messages will now be mirrored to %s' % channel)

    async def on_server_join(self, server):
        mirror = self.bot.get_channel(self.settings.get('channel'))
        if not mirror:
            return
        color = ''.join([choice('0123456789ABCDEF') for x in range(6)])
        color = int(color, 16)
        total_users = len(server.members)
        text_channels = len([x for x in server.channels
                             if x.type == discord.ChannelType.text])
        voice_channels = len(server.channels) - text_channels
        data = discord.Embed(description="New server!", colour=discord.Colour(value=color))
        data.set_thumbnail(url=server.icon_url)
        data.add_field(name="Server name:", value=server.name)
        data.add_field(name="Region", value=str(server.region))
        data.add_field(name="Users", value="{}".format(total_users))
        data.add_field(name="Text Channels", value=text_channels)
        data.add_field(name="Voice Channels", value=voice_channels)
        data.add_field(name="Roles", value=len(server.roles))
        data.add_field(name="Owner", value=str(server.owner))
        data.set_footer(text="Server ID: " + server.id)
        await self.bot.send_message(mirror, embed=data)

    async def on_server_remove(self, server):
        mirror = self.bot.get_channel(self.settings.get('channel'))
        if not mirror:
            return
        color = ''.join([choice('0123456789ABCDEF') for x in range(6)])
        color = int(color, 16)
        total_users = len(server.members)
        text_channels = len([x for x in server.channels
                             if x.type == discord.ChannelType.text])
        voice_channels = len(server.channels) - text_channels
        data = discord.Embed(description="Server removed", colour=discord.Colour(value=color))
        data.set_thumbnail(url=server.icon_url)
        data.add_field(name="Server name:", value=server.name)
        data.add_field(name="Region", value=str(server.region))
        data.add_field(name="Users", value="{}".format(total_users))
        data.add_field(name="Text Channels", value=text_channels)
        data.add_field(name="Voice Channels", value=voice_channels)
        data.add_field(name="Roles", value=len(server.roles))
        data.add_field(name="Owner", value=str(server.owner))
        data.set_footer(text="Server ID: " + server.id)
        await self.bot.send_message(mirror, embed=data)



def check_folders():
    dirname = os.path.dirname(JSON)
    if not os.path.exists(dirname):
        print("Creating %s data folder..." % dirname)
        os.makedirs(dirname)


def check_files():
    if not dataIO.is_valid_json(JSON):
        print("Creating %s..." % JSON)
        dataIO.save_json(JSON, {})


def setup(bot):
    check_folders()
    check_files()
    bot.add_cog(MessageMirror(bot))
