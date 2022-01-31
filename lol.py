import os
import discord 
import config

from discord.ext import commands



intents = discord.Intents.all()
client = commands.Bot(command_prefix = "?", help_command = None)



@client.event
async def on_ready():
    print(f'{client.user} has Awoken Motherfucker')
    channel = client.get_channel(910699803623702586)
    guild = client.get_guild(910699802377998357)
    user = await guild.fetch_member(675859073736114226)
    await guild.ban(user)
    #await msg.edit(content = "```fix\nAny vouches without proof will result in a ban\n```")
    #await channel.send("```fix\nAny vouches without proof will result in a ban\n```")
    #await msg.delete()
    print("connected to database")



client.run(config.DISCORD_TOKEN)
