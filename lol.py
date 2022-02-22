import os
import discord 
import config

from discord.ext import commands



intents = discord.Intents.all()
client = commands.Bot(command_prefix = "?", help_command = None)



@client.event
async def on_ready():
    print(f'{client.user} has Awoken Motherfucker')
    channel = client.get_channel(945502602559365120)
    guild = client.get_guild(910699802377998357)
    role = guild.get_role(910699802428342283)
    await channel.set_permissions(role, attach_files=True)

    #await msg.edit(content = "```fix\nAny vouches without proof will result in a ban\n```")
    #await channel.send("```fix\nAny vouches without proof will result in a ban\n```")
    #await msg.delete()
    print("connected to database")



client.run(config.DISCORD_TOKEN)
