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



client = commands.Bot(command_prefix = config.PREFIX, help_command = None)

cluster = MongoClient(config.MongoDBkey)

@client.event
async def on_ready():
    print(f'{client.user} has Awoken Motherfucker')
    print("connected to database")

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
