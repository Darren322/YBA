import os
import config 
import discord 
from commandsfunc import userCommands 
from commandsfunc import adminCommands
import time
import asyncio
import datetime
import jmespath
from pymongo import MongoClient
from discord.ext import commands

from discordHelper import newEmbed, errorMessage, RED, BLUE, GREEN, YELLOW

cluster = MongoClient(config.MongoDBkey)





class vouchadmincommands(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.command()
    @commands.has_role(config.scammer_role)
    async def scammer(self, ctx, member: discord.User):
        success = await adminCommands.scammer(member,
                                ctx.message.channel
                                )  
        if success[0]:
            await ctx.send(f"Added {success[1]} to scammer list")
        else:
            await ctx.send(f"Removed {success[1]} from scammer list")

    @commands.command(name ="removemany", aliases=["delvouches"])
    @commands.has_role(config.vouchadmin_role)
    async def removemany(self, ctx, member: discord.Member, args: int):
        channel = ctx.message.channel
        success = await adminCommands.removemany(member, channel, args)
        if success:
            await ctx.send(f'**{args}** vouches have been removed from {member.mention}')


    async def clearmessages(self, ctx , duration):
        durationdays = duration // 86400
        while True:
            await ctx.channel.purge(limit = 1000)
            await asyncio.sleep(1.5)
            await ctx.send("Channel purged. Next purge in {:.1f} day(s)".format(durationdays))
            await asyncio.sleep(duration)

    @commands.command(name='autoclear')
    @commands.has_role("purgeperm")
    async def autoclear(self, ctx, duration: int):
        global purgetask 
        purgetask = cilent.loop.create_task(clearmessages(self, ctx, duration))


    @commands.command(name='stopclear')
    @commands.has_role("purgeperm")
    async def stopclear(self, ctx):
        purgetask.cancel()
        await ctx.send("autoclear has stopped")


    @commands.command(name ="staff", aliases=["vstaff"])
    async def staff(self, ctx, member: discord.Member):
        db = cluster[config.database][config.collection]  
        for document in db.find():
            allData = document  
        masterIDs = allData['Masters']
        if ctx.author.id not in masterIDs:
            await ctx.send("You have no permsission to use this command!")
            return
        success = await adminCommands.staff(member, ctx.message.channel)
        if success:
            await ctx.send(f"Added {member.mention} to staff list") 
        else:
            await ctx.send(f"Removed {member.mention} from staff list") 

    @commands.command(name ="admin", aliases=["vadmin"])
    async def admin(self, ctx, member: discord.Member):
        db = cluster[config.database][config.collection]  
        for document in db.find():
            allData = document  
        masterIDs = allData['Masters']
        if ctx.author.id not in masterIDs:
            await ctx.send("You have no permsission to use this command!")
            return
        success = await adminCommands.admin(member, ctx.message.channel)
        if success:
            await ctx.send(f"Added {member.mention} to Masters list") 
        else:
            await ctx.send(f"Removed {member.mention} from Masters list") 



    @commands.command(name ="addvouch", aliases=["addvouches"])
    @commands.has_role(config.vouchadmin_role)
    async def addvouch(self, ctx, member: discord.Member, args: int):
        if member == self.client.user:
            await ctx.send("You are not allowed to add vouches to the bot")
            return
        if args > 100:
            await ctx.send("You only can add 100 vouches below at a time")
            return
        isPositive = True
        logChannel = self.client.get_channel(config.LOG_CHANNEL_ID)
        channel = ctx.message.channel
        success = await adminCommands.addVouches(ctx.author,
                                    member,
                                    isPositive,
                                    channel,
                                    logChannel,
                                    args) 
        if success:
            await ctx.send(f"**{args}** vouches have been added to {member.mention}")


    @commands.command()
    @commands.has_role(config.vouchadmin_role)
    async def remove(self, ctx, member: discord.Member, args: int = -1):
        channel = ctx.message.channel
        success = await adminCommands.remove(member, channel, args)
        if success[0]:
            await ctx.send(f"Removed VouchID **{success[1]}** from {member.mention}")
        else:
            await ctx.send(f"VouchID **{success[1]}** doesn't exists")


#==========================================================================================

    @scammer.error
    async def on_command_error_scammer(self, ctx, error):
        if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
            await ctx.send(f'Please follow this format: \n{config.PREFIX}scammer <@!322562448530079745>')
        if isinstance(error, discord.ext.commands.errors.MissingRole):
            await ctx.send('You have no permission to use this command. Idiot')

    @removemany.error
    async def on_command_error_removemany(self, ctx, error):
        if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
            await ctx.send(f'Please follow this format: \n{config.PREFIX}delvouches <@!322562448530079745> 5')
        if isinstance(error, discord.ext.commands.errors.MissingRole):
            await ctx.send('You have no permission to use this command. Idiot')

    @addvouch.error
    async def on_command_error_addvouch(self, ctx, error):
        if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
            await ctx.send(f'Please follow this format: \n{config.PREFIX}addvouches <@!322562448530079745> 50')
        if isinstance(error, discord.ext.commands.errors.MissingRole):
            await ctx.send('You have no permission to use this command. Idiot')

    @remove.error
    async def on_command_error_remove(self, ctx, error):
        if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
            await ctx.send(f'Please follow this format: \n{config.PREFIX}remove <@!322562448530079745>')
        if isinstance(error, discord.ext.commands.errors.MissingRole):
            await ctx.send('You have no permission to use this command. Idiot')

    @staff.error
    async def on_command_error_admin(self, ctx, error):
        if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
            await ctx.send(f'Missing argument\n{config.PREFIX}admin <user>')
            
    @autoclear.error
    async def on_command_error8(self, ctx, error):
        if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
            await ctx.send('Please follow this format: \n ?autoclear [duration]')
        if isinstance(error, discord.ext.commands.errors.MissingRole):
            await ctx.send('You have no permission to use this command. Idiot')

    @stopclear.error
    async def on_command_error9(self, ctx, error):
        if isinstance(error, discord.ext.commands.errors.MissingRole):
            await ctx.send('No permission to use this cunt')
          
def setup(client):
  client.add_cog(vouchadmincommands(client))
