import discord
from discord.ext import commands
from cogs.utils.dataIO import fileIO
from __main__ import send_cmd_help, settings
from cogs.utils import checks
import os
import aiohttp
import asyncio
from random import *

# weird because 0 indexing
numbs = {
    "1?": 0,
    "2?": 1,
    "3?": 2,
    "4?": 3,
    "5?": 4,
    "6?": 5,
    "7?": 6,
    "8?": 7,
    "9?": 8,
    "??": 9
}


class UtilsMenu:
    def __init__(self, bot):
        self.bot = bot
        self.bot.remove_command("utilsmenu")
        self.bot.remove_command("roles")
        self.bot.remove_command("sendmod")
        self.bot.remove_command("pin")
        self.bot.remove_command("unpin")
        self.bot.remove_command("listmods")
        self.bot.remove_command("permissions")
        self.bot.remove_command("invite")
        self.bot.remove_command("disclaimer")
        self.cogs_file = 'data/red/cogs.json'

    def _perms(self, ctx, perm):
        if ctx.message.author.id == settings.owner:
            return True

        ch = ctx.message.channel
        author = ctx.message.author
        resolved = ch.permissions_for(author)
        return resolved.perm

    async def _prompt(self, ctx, msg: str):
        await self.bot.say(msg)
        msg = await self.bot.wait_for_message(author=ctx.message.author, channel=ctx.message.channel)
        return msg

    @commands.command(pass_context=True, no_pm=True)
    async def utilsmenu(self, ctx):
        await self.bot.say(":warning: | Some menu items may not work for certain users due to permission requirements.")
        author = ctx.message.author
        menu = self.bot.get_cog("Menu")
        cmds = ["Roles", "Send modules", "List modules", "Permissions", "Invite", "Disclaimer", "Cancel"]

        result = await menu.number_menu(ctx, "Utilities menu", cmds, autodelete=True)
        cmd = cmds[result-1]

        if cmd == "Roles" and self._perms(ctx, 'manage_roles'):
            await ctx.invoke(self.roles)
                
        if cmd == "Send modules" and self._perms(ctx, 'manage_roles'):
            await ctx.invoke(self.sendmod)
        
        if cmd == "List modules" and self._perms(ctx, 'manage_messages'):
            await ctx.invoke(self.listmods)
            
        if cmd == "Permissions" and self._perms(ctx, 'manage_roles'):
            await ctx.invoke(self.permissions)
            
        if cmd == "Invite":
            await ctx.invoke(self.invite)
                
        if cmd == "Disclaimer":
            await ctx.invoke(self.disclaimer)    
                
        if cmd == "Cancel":
            return await self.bot.say("Menu cancelled.")

        if cmd is None:
            return await self.bot.say("Menu has expired.")
            

    @checks.mod_or_permissions(manage_roles=True)
    @commands.command(pass_context=True, no_pm=True, hidden=True)
    async def roles(self, ctx):
        """Shows the roles of the server."""
        roles = ""
        for x in ctx.message.server.roles:
            roles += ((str(x.name).ljust(30)) + str(x.id) + "\n")
        await self.bot.say("```{0}```".format(roles))

    @commands.command(pass_context=True, no_pm=True, hidden=True)
    @checks.is_owner()
    async def sendmod(self, ctx):
        """Sends a module."""
        fp = await self._prompt(ctx, "What module do you want to send?")
        fp = "cogs/{0}.py".format(fp.content)
        if os.path.exists(fp):
            await self.bot.send_file(ctx.message.channel, fp)
        else:
            await self.bot.say("Module not found!")

    @commands.command(pass_context=True)
    @checks.mod_or_permissions(manage_messages=True)
    async def pin(self, ctx, text: str, user: discord.User = None):
        """Pin a recent message, useful on mobile.
        Usage:
            pin word
            pin "More than one word"
            pin "More than one word but said by" @someone """
        channel = ctx.message.channel
        if not text:
            return await send_cmd_help(ctx)
        else:
            if user and text:
                async for x in self.bot.logs_from(channel):
                    if x.content.startswith(text) and x.author.id == user.id:
                        return await self.bot.pin_message(x)
            elif text:
                async for x in self.bot.logs_from(channel):
                    if x.content.startswith(text):
                        return await self.bot.pin_message(x)
            else:
                await self.bot.say("Whoops! Looks like something went wrong")

    @commands.command(pass_context=True, hidden=True)
    @checks.mod_or_permissions(manage_messages=True)
    async def unpin(self, ctx, text: str, user: discord.User = None):
        """Unpin a message pinned in the current channel.
        Usage is the same as the pin command"""

        channel = ctx.message.channel
        if not text:
            return await send_cmd_help(ctx)
        for x in (await self.bot.pins_from(channel)):
            if text and user:
                if x.content.startswith(text) and x.author == user:
                    return await self.bot.unpin_message(x)
            elif text and x.content.startswith(text):
                return await self.bot.unpin_message(x)

    async def prefixes(self, message):
        if message.content == "prefixes":
            prefix_list = [x for x in self.bot.command_prefix]
            msg = "```{0}```".format(', '.join(prefix_list))
            await self.bot.send_message(message.channel, msg)

    @commands.command(pass_context=True, no_pm=True, hidden=True)
    @checks.is_owner()
    async def listmods(self, ctx):
        """Shows the status of modules.
        + means the module is loaded
        - means the module is unloaded
        ? means the module couldn't be found (it was probably removed manually)"""

        all_cogs = fileIO(self.cogs_file, 'load')
        loaded, unloaded, other = ("",)*3
        cogs = self.bot.cogs['Owner']._list_cogs()

        for x in all_cogs:
            if all_cogs.get(x):
                if x in cogs:
                    loaded += "+\t{0}\n".format(x.split('.')[1])
                else:
                    other += "?\t{0}\n".format(x.split('.')[1])
            elif x in cogs:
                unloaded += "-\t{0}\n".format(x.split('.')[1])
        msg = "```diff\n{0}{1}{2}```".format(loaded, unloaded, other)
        await self.bot.say(msg)

    @commands.command(pass_context=True, no_pm=True, hidden=True)
    @checks.admin_or_permissions(manage_roles=True)
    async def permissions(self, ctx):
        user = await self._prompt(ctx, "What user should we display the permissions of?")
        try:
            if user.mentions is not None:
                user = user.mentions[0]
        except:
            try:
                user = discord.utils.get(ctx.message.server.members, name=str(user.content))
            except:
                await self.bot.say("User not found!")
                return 
                
        perms = iter(ctx.message.channel.permissions_for(user))
        perms_we_have = "```diff\n"
        perms_we_dont = ""
        for x in perms:
            if "True" in str(x):
                perms_we_have += "+\t{0}\n".format(str(x).split('\'')[1])
            else:
                perms_we_dont += ("-\t{0}\n".format(str(x).split('\'')[1]))
        await self.bot.say("{0}{1}```".format(perms_we_have, perms_we_dont))
        
    @commands.command(pass_context=True, hidden=True)
    async def disclaimer(self, ctx):
        await self.bot.say("*Sigh...* Either you [" + ctx.message.author.mention + "] found this by accident (in which case fair enough, sorry about this) or you're another one of those individuals that I had to make this command for. \n If this was an accident, write 'No', if this wasn't an accident, write 'Yes'")
        answer = await self.bot.wait_for_message(timeout=15, author=ctx.message.author)
        
        if answer is None:
            await self.bot.say("Since you apparently don't know whether you found this by accident or not, I'll stick to the safe side and not display the disclaimer.")
            return
        elif "yes" not in answer.content.lower() and "no" not in answer.content.lower():
            await self.bot.say(":warning: | ***__INVALID ANSWER. CHOOSE EITHER 'Yes' OR 'No' NEXT TIME.__***")
            return
        elif "yes" in answer.content.lower():
            await self.bot.say("In an ideal world, where people didn't just make assumptions, this command wouldn't have to exist.")
            await self.bot.say(":warning: | ***__DISCLAIMER:__*** \n \n Brooklyn, is made by Young. \n He did **__NOT__** create all of the modules and has never claimed to (*__module credit goes to their respective developers__*). \n There seems to be some confusion somewhere, so I'd like to clear it up. \n \n Brooklyn and Red **__ARE NOT__** the same thing. Brooklyn may have some of Red's modules (props to Twentysix as he's an amazing developer) but only ones that Young couldn't get to work or couldn't be bothered to create. \n However, the ones he has 'taken' are extensively modified to the point where you'll almost never have the same version. Quite a few things were still made by Young though, including the base framework of the bot. \n Thanks for understanding. ~Young ")
            return
        elif "no" in answer.content.lower():
            await self.bot.say("Oh, you found this by accident. Ok. I won't display the disclaimer.")
            


def setup(bot):
    n = UtilsMenu(bot)
    bot.add_listener(n.prefixes, 'on_message')
    bot.add_cog(n)