import os
import discord 
import config

from discord.ext import commands




client = commands.Bot(command_prefix = "?", help_command = None)



@client.event
async def on_ready():
    print(f'{client.user} has Awoken Motherfucker')
    channel = client.get_channel(910699803623702586)
    msg = await channel.fetch_message(937355958768783370)
    #await msg.edit(content = "```fix\nAny vouches without proof will result in a ban\n```")
    #await channel.send("```fix\nAny vouches without proof will result in a ban\n```")
    await msg.delete()
    print("connected to database")



client.run(config.DISCORD_TOKEN)
