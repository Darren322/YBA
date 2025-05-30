import os
import config
import discord 
import time
import asyncio
from datetime import datetime 
import jmespath

from pymongo import MongoClient

from discord.ext import commands

from discordHelper import newEmbed, errorMessage, RED, BLUE, GREEN, YELLOW

RED = 0xEF233C
YELLOW = 0xFFB400
ORANGE = 0xFF7106

client = commands.Bot(command_prefix = config.PREFIX, help_command = None)

cluster = MongoClient(config.MongoDBkey)

@client.event
async def on_ready():
    print(f'{client.user} has Awoken Motherfucker')
    print("connected to database")


@client.event
async def on_message(message):
    messagecheck = message.content.split('\n')
    booster = client.get_channel(945172855753158677)
    trusted = client.get_channel(945172630368047114)
    selling = client.get_channel(945170591877591052)
    buying = client.get_channel(945170606603771934)
    ybatrading = client.get_channel(945170625025151046)
    outsideyba = client.get_channel(945172437484601385)
    stafflogs = client.get_channel(940342044780535839)
    msglimit = 15
    errormsg = "Your message needs to be equal to or less than 15 lines!"
    reason = "Going over 15 lines"




    if message.channel == booster:
        if len(messagecheck) > msglimit:
            time.sleep(2)
            await message.channel.purge(limit = 1)
            await message.author.send(errormsg)
            embed = discord.Embed(description=f'Message deleted in {message.channel.mention}', title='', color=ORANGE, timestamp=datetime.utcnow())
            embed.add_field(name='Reason\n',
                            value=f'{reason}', inline=False)
            embed.add_field(name='Content\n',
                            value=f'{message.content}', inline=False)
            embed.add_field(name='ID\n',
                            value=f'```{message.author.id}```', inline=False)
            embed.set_author(name =f'{message.author}', icon_url=message.author.avatar_url)
            embed.set_footer(text=f"{client.user}", icon_url=client.user.avatar_url)
            await stafflogs.send(embed=embed)

            

    if message.channel == trusted:
        if len(messagecheck) > msglimit:
            await message.channel.purge(limit = 1)
            await message.author.send(errormsg)
            embed = discord.Embed(description=f'Message deleted in {message.channel.mention}', title='', color=ORANGE, timestamp=datetime.utcnow())
            embed.add_field(name='Reason\n',
                            value=f'{reason}', inline=False)
            embed.add_field(name='Content\n',
                            value=f'{message.content}', inline=False)
            embed.add_field(name='ID\n',
                            value=f'```{message.author.id}```', inline=False)
            embed.set_author(name =f'{message.author}', icon_url=message.author.avatar_url)
            embed.set_footer(text=f"{client.user}", icon_url=client.user.avatar_url)
            await stafflogs.send(embed=embed)

    if message.channel == selling:
        if len(messagecheck) > msglimit:
            await message.channel.purge(limit = 1)
            await message.author.send(errormsg)
            embed = discord.Embed(description=f'Message deleted in {message.channel.mention}', title='', color=ORANGE, timestamp=datetime.utcnow())
            embed.add_field(name='Reason\n',
                            value=f'{reason}', inline=False)
            embed.add_field(name='Content\n',
                            value=f'{message.content}', inline=False)
            embed.add_field(name='ID\n',
                            value=f'```{message.author.id}```', inline=False)
            embed.set_author(name =f'{message.author}', icon_url=message.author.avatar_url)
            embed.set_footer(text=f"{client.user}", icon_url=client.user.avatar_url)
            await stafflogs.send(embed=embed)

    if message.channel == buying:
        if len(messagecheck) > msglimit:
            await message.channel.purge(limit = 1)
            await message.author.send(errormsg)
            embed = discord.Embed(description=f'Message deleted in {message.channel.mention}', title='', color=ORANGE, timestamp=datetime.utcnow())
            embed.add_field(name='Reason\n',
                            value=f'{reason}', inline=False)
            embed.add_field(name='Content\n',
                            value=f'{message.content}', inline=False)
            embed.add_field(name='ID\n',
                            value=f'```{message.author.id}```', inline=False)
            embed.set_author(name =f'{message.author}', icon_url=message.author.avatar_url)
            embed.set_footer(text=f"{client.user}", icon_url=client.user.avatar_url)
            await stafflogs.send(embed=embed)

    if message.channel == ybatrading:
        if len(messagecheck) > msglimit:
            await message.channel.purge(limit = 1)
            await message.author.send(errormsg)
            embed = discord.Embed(description=f'Message deleted in {message.channel.mention}', title='', color=ORANGE, timestamp=datetime.utcnow())
            embed.add_field(name='Reason\n',
                            value=f'{reason}', inline=False)
            embed.add_field(name='Content\n',
                            value=f'{message.content}', inline=False)
            embed.add_field(name='ID\n',
                            value=f'```{message.author.id}```', inline=False)
            embed.set_author(name =f'{message.author}', icon_url=message.author.avatar_url)
            embed.set_footer(text=f"{client.user}", icon_url=client.user.avatar_url)
            await stafflogs.send(embed=embed)

    if message.channel == outsideyba:
        if len(messagecheck) > msglimit:
            await message.channel.purge(limit = 1)
            await message.author.send(errormsg)
            embed = discord.Embed(description=f'Message deleted in {message.channel.mention}', title='', color=ORANGE, timestamp=datetime.utcnow())
            embed.add_field(name='Reason\n',
                            value=f'{reason}', inline=False)
            embed.add_field(name='Content\n',
                            value=f'{message.content}', inline=False)
            embed.add_field(name='ID\n',
                            value=f'```{message.author.id}```', inline=False)
            embed.set_author(name =f'{message.author}', icon_url=message.author.avatar_url)
            embed.set_footer(text=f"{client.user}", icon_url=client.user.avatar_url)
            await stafflogs.send(embed=embed)



    await client.process_commands(message)


@client.event
async def on_message_edit(message_before, message_after):
    messagecheck = message_after.content.split('\n')
    errormsg = "**Nice edit noob**. 15 lines and below please"
    booster = client.get_channel(945172855753158677)
    trusted = client.get_channel(945172630368047114)
    selling = client.get_channel(945170591877591052)
    buying = client.get_channel(945170606603771934)
    ybatrading = client.get_channel(945170625025151046)
    outsideyba = client.get_channel(945172437484601385)
    stafflogs = client.get_channel(940342044780535839)
    msglimit = 15
    reason = "Edited message over 15 lines"

    if message_after.channel == booster:
        if len(messagecheck) > msglimit:
            time.sleep(2)
            await message_after.channel.purge(limit = 1)
            await message_after.author.send(errormsg)
            embed = discord.Embed(description=f'Message deleted in {message_after.channel.mention}', title='', color=YELLOW, timestamp=datetime.utcnow())
            embed.add_field(name='Reason\n',
                            value=f'{reason}', inline=False)
            embed.add_field(name='Before\n',
                            value=f'{message_before.content}', inline=False)
            embed.add_field(name='After\n',
                            value=f'{message_after.content}', inline=False)
            embed.add_field(name='ID\n',
                            value=f'```{message_after.author.id}```', inline=False)
            embed.set_author(name =f'{message_after.author}', icon_url=message_after.author.avatar_url)
            embed.set_footer(text=f"{client.user}", icon_url=client.user.avatar_url)
            await stafflogs.send(embed=embed)

            

    if message_after.channel == trusted:
        if len(messagecheck) > msglimit:
            await message_after.channel.purge(limit = 1)
            await message_after.author.send(errormsg)
            embed = discord.Embed(description=f'Message deleted in {message_after.channel.mention}', title='', color=YELLOW, timestamp=datetime.utcnow())
            embed.add_field(name='Reason\n',
                            value=f'{reason}', inline=False)
            embed.add_field(name='Before\n',
                            value=f'{message_before.content}', inline=False)
            embed.add_field(name='After\n',
                            value=f'{message_after.content}', inline=False)
            embed.add_field(name='ID\n',
                            value=f'```{message_after.author.id}```', inline=False)
            embed.set_author(name =f'{message_after.author}', icon_url=message_after.author.avatar_url)
            embed.set_footer(text=f"{client.user}", icon_url=client.user.avatar_url)
            await stafflogs.send(embed=embed)

    if message_after.channel == selling:
        if len(messagecheck) > msglimit:
            await message_after.channel.purge(limit = 1)
            await message_after.author.send(errormsg)
            embed = discord.Embed(description=f'Message deleted in {message_after.channel.mention}', title='', color=YELLOW, timestamp=datetime.utcnow())
            embed.add_field(name='Reason\n',
                            value=f'{reason}', inline=False)
            embed.add_field(name='Before\n',
                            value=f'{message_before.content}', inline=False)
            embed.add_field(name='After\n',
                            value=f'{message_after.content}', inline=False)
            embed.add_field(name='ID\n',
                            value=f'```{message_after.author.id}```', inline=False)
            embed.set_author(name =f'{message_after.author}', icon_url=message_after.author.avatar_url)
            embed.set_footer(text=f"{client.user}", icon_url=client.user.avatar_url)
            await stafflogs.send(embed=embed)

    if message_after.channel == buying:
        if len(messagecheck) > msglimit:
            await message_after.channel.purge(limit = 1)
            await message_after.author.send(errormsg)
            embed = discord.Embed(description=f'Message deleted in {message_after.channel.mention}', title='', color=YELLOW, timestamp=datetime.utcnow())
            embed.add_field(name='Reason\n',
                            value=f'{reason}', inline=False)
            embed.add_field(name='Before\n',
                            value=f'{message_before.content}', inline=False)
            embed.add_field(name='After\n',
                            value=f'{message_after.content}', inline=False)
            embed.add_field(name='ID\n',
                            value=f'```{message_after.author.id}```', inline=False)
            embed.set_author(name =f'{message_after.author}', icon_url=message_after.author.avatar_url)
            embed.set_footer(text=f"{client.user}", icon_url=client.user.avatar_url)
            await stafflogs.send(embed=embed)

    if message_after.channel == ybatrading:
        if len(messagecheck) > msglimit:
            await message_after.channel.purge(limit = 1)
            await message_after.author.send(errormsg)
            embed = discord.Embed(description=f'Message deleted in {message_after.channel.mention}', title='', color=YELLOW, timestamp=datetime.utcnow())
            embed.add_field(name='Reason\n',
                            value=f'{reason}', inline=False)
            embed.add_field(name='Before\n',
                            value=f'{message_before.content}', inline=False)
            embed.add_field(name='After\n',
                            value=f'{message_after.content}', inline=False)
            embed.add_field(name='ID\n',
                            value=f'```{message_after.author.id}```', inline=False)
            embed.set_author(name =f'{message_after.author}', icon_url=message_after.author.avatar_url)
            embed.set_footer(text=f"{client.user}", icon_url=client.user.avatar_url)
            await stafflogs.send(embed=embed)

    if message_after.channel == outsideyba:
        if len(messagecheck) > msglimit:
            await message_after.channel.purge(limit = 1)
            await message_after.author.send(errormsg)
            embed = discord.Embed(description=f'Message deleted in {message_after.channel.mention}', title='', color=YELLOW, timestamp=datetime.utcnow())
            embed.add_field(name='Reason\n',
                            value=f'{reason}', inline=False)
            embed.add_field(name='Before\n',
                            value=f'{message_before.content}', inline=False)
            embed.add_field(name='After\n',
                            value=f'{message_after.content}', inline=False)
            embed.add_field(name='ID\n',
                            value=f'```{message_after.author.id}```', inline=False)
            embed.set_author(name =f'{message_after.author}', icon_url=message_after.author.avatar_url)
            embed.set_footer(text=f"{client.user}", icon_url=client.user.avatar_url)
            await stafflogs.send(embed=embed)





@client.command()
async def load(ctx, extension):
    if ctx.author.id != 241927483962687488:
        await ctx.send("You are not a chad")
        return
    client.load_extension(f'cogs.{extension}')
    await ctx.send("Loaded")


@client.command()
async def unload(ctx, extension):
    if ctx.author.id != 241927483962687488:
        await ctx.send("You are not a chad")
        return
    client.unload_extension(f'cogs.{extension}')
    await ctx.send("Unloaded")

@client.command()
async def reload(ctx, extension):
    if ctx.author.id != 241927483962687488:
        await ctx.send("You are not a chad")
        return
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')
    await ctx.send("Reloaded")



@load.error
async def on_command_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        await ctx.send(f'Missing arguments')
@reload.error
async def on_command_error2(ctx, error):
    if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        await ctx.send(f'Missing arguments')
@unload.error
async def on_command_error3(ctx, error):
    if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        await ctx.send(f'Missing arguments')


for filename in os.listdir('./cogs'):
    if filename.endswith('py'):
        client.load_extension(f'cogs.{filename[:-3]}')


client.run(config.DISCORD_TOKEN)
