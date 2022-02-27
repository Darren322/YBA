import os
import config
import discord 
import time
import asyncio
import datetime
import jmespath

from pymongo import MongoClient

from discord.ext import commands

from discordHelper import newEmbed, errorMessage, RED, BLUE, GREEN, YELLOW

RED = 0xEF233C

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





    if message.channel == booster:
        if len(messagecheck) > msglimit:
            time.sleep(2)
            await message.channel.purge(limit = 1)
            await message.author.send(errormsg)
            embed = discord.Embed(description=f'Message deleted in {channel.mention}', title='', color=RED, timestamp=datetime.utcnow())
            embed.add_field(name='Content\n',
                            value=f'{messagecheck}', inline=False)
            embed.add_field(name='Content\n',
                            value=f'{messagecheck}', inline=False)
            embed.set_author(name =f'{authorName}', icon_url=targetUser.avatar_url)
            embed.set_footer(text=f"{client}", icon_url=client.user.avatar_url)
            await stafflogs.send(embed=embed)

            

    if message.channel == booster:
        if len(messagecheck) > msglimit:
            await message.channel.purge(limit = 1)
            await message.author.send(errormsg)
            embed = discord.Embed(description=f'Message deleted in {channel.mention}', title='', color=RED, timestamp=datetime.utcnow())
            embed.add_field(name='Content\n',
                            value=f'{messagecheck}', inline=False)
            embed.add_field(name='Content\n',
                            value=f'{messagecheck}', inline=False)
            embed.set_author(name =f'{authorName}', icon_url=targetUser.avatar_url)
            embed.set_footer(text=f"{client}", icon_url=client.user.avatar_url)
            await stafflogs.send(embed=embed)

    if message.channel == selling:
        if len(messagecheck) > msglimit:
            await message.channel.purge(limit = 1)
            await message.author.send(errormsg)
            embed = discord.Embed(description=f'Message deleted in {channel.mention}', title='', color=RED, timestamp=datetime.utcnow())
            embed.add_field(name='Content\n',
                            value=f'{messagecheck}', inline=False)
            embed.add_field(name='Content\n',
                            value=f'{messagecheck}', inline=False)
            embed.set_author(name =f'{authorName}', icon_url=targetUser.avatar_url)
            embed.set_footer(text=f"{client}", icon_url=client.user.avatar_url)
            await stafflogs.send(embed=embed)

    if message.channel == buying:
        if len(messagecheck) > ybatrading:
            await message.channel.purge(limit = 1)
            await message.author.send(errormsg)
            embed = discord.Embed(description=f'Message deleted in {channel.mention}', title='', color=RED, timestamp=datetime.utcnow())
            embed.add_field(name='Content\n',
                            value=f'{messagecheck}', inline=False)
            embed.add_field(name='Content\n',
                            value=f'{messagecheck}', inline=False)
            embed.set_author(name =f'{authorName}', icon_url=targetUser.avatar_url)
            embed.set_footer(text=f"{client}", icon_url=client.user.avatar_url)
            await stafflogs.send(embed=embed)

    if message.channel == ybatrading:
        if len(messagecheck) > msglimit:
            await message.channel.purge(limit = 1)
            await message.author.send(errormsg)
            embed = discord.Embed(description=f'Message deleted in {channel.mention}', title='', color=RED, timestamp=datetime.utcnow())
            embed.add_field(name='Content\n',
                            value=f'{messagecheck}', inline=False)
            embed.add_field(name='Content\n',
                            value=f'{messagecheck}', inline=False)
            embed.set_author(name =f'{authorName}', icon_url=targetUser.avatar_url)
            embed.set_footer(text=f"{client}", icon_url=client.user.avatar_url)
            await stafflogs.send(embed=embed)

    if message.channel == outsideyba:
        if len(messagecheck) > msglimit:
            await message.channel.purge(limit = 1)
            await message.author.send(errormsg)
            embed = discord.Embed(description=f'Message deleted in {channel.mention}', title='', color=RED, timestamp=datetime.utcnow())
            embed.add_field(name='Content\n',
                            value=f'{messagecheck}', inline=False)
            embed.add_field(name='Content\n',
                            value=f'{messagecheck}', inline=False)
            embed.set_author(name =f'{authorName}', icon_url=targetUser.avatar_url)
            embed.set_footer(text=f"{client}", icon_url=client.user.avatar_url)
            await stafflogs.send(embed=embed)



    await client.process_commands(message)

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
