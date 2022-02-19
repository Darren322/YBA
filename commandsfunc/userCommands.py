#cython: language_level=3


import discord
from datetime import datetime 
import json
from pymongo import MongoClient
import bson
import os
import config


from discordHelper import User, Vouch , newEmbed, errorMessage, RED, BLUE, GREEN, YELLOW, ORANGE, LBLUE, L2BLUE, L3BLUE, L4BLUE, L5BLUE, GREY, PINK, WHITE, AQUA
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType

cluster = MongoClient(config.MongoDBkey)
obj_id = bson.ObjectId(config.obj_id)

async def vouch(user: discord.User,
                targetUser: discord.User,
                message: str,
                isPositive: bool,
                guild: discord.Guild,
                logChannel: discord.TextChannel,
                rating: int,
                URL: str):
    '''
        Leaves a vouch for a user
    '''
    db = cluster[config.database][config.collection]  
    u = User(targetUser.id)
    vouches = u.vouches
    for document in db.find():
      allData = document
    if user.id in u.allData['Blacklist']:
       return False

    # Save to pending vouches
    vouchNum: int = allData['VouchCount'] + 1
    vouch = {
        'ID': vouchNum,
        'Giver': user.id,
        'Receiver': targetUser.id,
        'IsPositive': isPositive,
        'Message': message,
        'Rating': rating
    }

    db.update_one({'_id': obj_id},{'$set': {'VouchCount': vouchNum}})
    target = str(targetUser.id)
    giverr = str(user.id)

    vouch = Vouch(vouch)
    db.update_one({'_id': obj_id, 'Users.ID': targetUser.id}, {'$push': {'Users.$[i].Vouches': vouch.toDict()}}, upsert = False, array_filters= [{'i.ID': targetUser.id}])


    # Send embeds to the user
    embed = newEmbed(description='', title=f'Vouch ID: {vouchNum}')
    embed.add_field(name='Receiver', value=f'<@!{target}>', inline=False)
    embed.add_field(name='Giver', value=f'<@!{giverr}>', inline=False)
    embed.add_field(name='Comment', value=message, inline=False)
    embed.add_field(name='Rating', value=rating, inline=False)
    embed.add_field(name='Server', value=guild.name, inline=False)
    if URL is None:
        await user.send(embed=embed)
    else:
        embed.set_image(url=URL)
        await user.send(embed=embed)

    # Send embed to log channel
    embed = newEmbed(description='', title=f'Vouch ID: {vouchNum}')
    embed.add_field(name='Receiver', value=f'<@!{target}>', inline=False)
    embed.add_field(name='Giver', value=f'<@!{giverr}>', inline=False)
    embed.add_field(name='Comment', value=message, inline=False)
    embed.add_field(name='Rating', value=rating, inline=False)
    embed.add_field(name='Server', value=guild.name, inline=False)
    if URL is None:
        await logChannel.send(embed=embed)
    else:
        embed.set_image(url=URL)
        await logChannel.send(embed=embed)

    return True

        
async def getrole(user: discord.User, bcGuild: discord.Guild, channel: discord.TextChannel):

    trusted_role = discord.utils.get(bcGuild.roles, name="Trusted 1")
    trusted_role2 = discord.utils.get(bcGuild.roles, name="Trusted 2")
    trusted_role3 = discord.utils.get(bcGuild.roles, name="Trusted 3")
    trusted_role4 = discord.utils.get(bcGuild.roles, name="Trusted 4")
    trusted_role5 = discord.utils.get(bcGuild.roles, name="Trusted 5")

    us = User(user.id)
    
    if trusted_role5 not in user.roles and len(us.vouches) >= 250:
        await user.add_roles(trusted_role5)
        await user.remove_roles(trusted_role4)
        await user.remove_roles(trusted_role3)
        await user.remove_roles(trusted_role2)
        await user.remove_roles(trusted_role)
        trustedname = 'Trusted 5'
        return True, trustedname

    elif trusted_role4 not in user.roles and trusted_role5 not in user.roles and len(us.vouches) >= 200:
        await user.add_roles(trusted_role4)
        await user.remove_roles(trusted_role3)
        await user.remove_roles(trusted_role2)
        await user.remove_roles(trusted_role)
        trustedname = 'Trusted 4'
        return True, trustedname


    elif trusted_role3 not in user.roles and trusted_role4 not in user.roles and trusted_role5 not in user.roles and len(us.vouches) >= 150:
        await user.add_roles(trusted_role3)
        await user.remove_roles(trusted_role2)
        await user.remove_roles(trusted_role)
        trustedname = 'Trusted 3'
        return True, trustedname


    elif trusted_role2 not in user.roles and trusted_role3 not in user.roles and trusted_role4 not in user.roles and trusted_role5 not in user.roles and len(us.vouches) >= 100:
        await user.add_roles(trusted_role2)
        await user.remove_roles(trusted_role)
        trustedname = 'Trusted 2'
        return True, trustedname
       

    elif trusted_role not in user.roles and trusted_role2 not in user.roles and len(us.vouches) >= 50:
        await user.add_roles(trusted_role)
        trustedname = 'Trusted 1'
        return True, trustedname
        
    else:
      return False



async def help(prefix: str, user: discord.User, isMaster):
    '''
        Displays all the commands that the user can use
    '''
    embed = discord.Embed(title=f'{config.Server_Name} Vouch Commands',
                          color=GREEN)
    embed.add_field(name=f'?vouch @user [message]',
                    value='Leave a positive or negative vouch for the user.',
                    inline=False)
    embed.add_field(name=f'?vouches **OR** ?vouches [user]',
                    value='See a user\'s profile.',
                    inline=False)
    embed.add_field(name=f'?getrole',
                    value='Get trusted role depending on your number of vouches\n',
                    inline=False)

    if isMaster:
        embed.add_field(name=f'{prefix}delvouches @user [Number of vouches]',
                        value=f'Only removes {prefix}addvouch vouches',
                        inline=False)

        embed.add_field(name=f'{prefix}scammer @user',
                        value='Toggles the Scammer tag for the user',
                        inline= False)

        embed.add_field(name=f'{prefix}remove @user -> Lists the vouches the user have \n{prefix}remove @user [vouch id]',
                        value='Removes vouch from user',
                        inline= False)

        embed.add_field(name=f'{prefix}addvouch/addvouches @user [Number of vouches]',
                        value='Added vouches to user')

    await user.send(embed=embed)

async def profile(targetUser: discord.User, bcGuild: discord.Guild,
                  channel: discord.TextChannel):
    '''
        If a user is mentioned, it will display their profiles
        details. If a user isn't mentioned, then the author's
        profile is displayed.
    '''
    u = User(targetUser.id)
    trusted_role = discord.utils.get(bcGuild.roles, name="Trusted 1")
    trusted_role2 = discord.utils.get(bcGuild.roles, name="Trusted 2")
    trusted_role3 = discord.utils.get(bcGuild.roles, name="Trusted 3")
    trusted_role4 = discord.utils.get(bcGuild.roles, name="Trusted 4")
    trusted_role5 = discord.utils.get(bcGuild.roles, name="Trusted 5")

    today = datetime.utcnow()
    accountcreated = targetUser.created_at
    accountserverdate = targetUser.joined_at
    daysLeft = today - accountcreated
    daysLeft2 = today - accountserverdate



    # Decide a proper color


    if trusted_role and trusted_role2 and trusted_role3 and trusted_role4 and trusted_role5 not in targetUser.roles:
        color = GREY
    if trusted_role in targetUser.roles:
        color = PINK
    if trusted_role2 in targetUser.roles:
        color = ORANGE
    if trusted_role3 in targetUser.roles:
        color = BLUE
    if trusted_role4 in targetUser.roles:
        color = GREEN
    if trusted_role5 in targetUser.roles:
        color = AQUA      


    if trusted_role5 in targetUser.roles:
      trusted = '5'
    elif trusted_role4 in targetUser.roles:
      trusted = '4'
    elif trusted_role3 in targetUser.roles:
      trusted = '3'
    elif trusted_role2 in targetUser.roles:
      trusted = '2'
    elif trusted_role in targetUser.roles:
      trusted = '1'
    else:
      trusted = '0'

    if u.isScammer:
      color = RED



    dwcMsg = u.dwcReason + '\n' if u.dwc > 0 else ''
    dwcTitle = '' if u.dwc == 0 else f'**Deal with caution{danger} ** '


    TotalReviews = u.fiveratingsgiven + u.fourratingsgiven + u.threeratingsgiven + u.tworatingsgiven + u.oneratingsgiven
    if TotalReviews == 0:
      TotalReviews = 0
    AverageWeightRating = (u.fiveratingsgiven)*5 + (u.fourratingsgiven)*4 + (u.threeratingsgiven)*3 + (u.tworatingsgiven)*2 + (u.oneratingsgiven)*1
    if AverageWeightRating == 0:
      AverageWeightRating = 0
      
    try:
      AverageRatings = AverageWeightRating/TotalReviews
    except ZeroDivisionError:
      AverageRatings = 0


    if AverageRatings >= 5:
      Ratings = '★★★★★'
    elif AverageRatings >= 4:
      Ratings = '★★★★☆'
    elif AverageRatings >= 3:
      Ratings = '★★★☆☆'
    elif AverageRatings >= 2:
      Ratings = '★★☆☆☆'
    elif AverageRatings >= 1:
      Ratings = '★☆☆☆☆'
    elif AverageRatings >= 0:
      Ratings = '☆☆☆☆☆'

    if u.isScammer:
      IsScammer = "Yes"
    else:
      IsScammer = "No"

    if int(daysLeft2.days) < 7 and int(daysLeft.days) < 10:
      warning = "(Very Risky)"
    elif int(daysLeft2.days) < 7:
      warning = "(Risky)"
    else:
      warning = ""



    totalratings = round(AverageRatings, 1)

    # Add relevant information
    embed = newEmbed(description='', title='', color=color)
    # embed.add_field(name='Vouch Information\n\n',
    #                value=f'\n\n**Vouches Given:** {u.vouchesgiven} \n\n**Vouchs Received:** {len(u.vouches)}')
    embed.add_field(name=f'Rating\n\n',
                    value=f'{Ratings} `{totalratings}/5`')
    embed.add_field(name='Vouches Given\n\n',
                    value=f'{u.vouchesgiven}\n\n')
    embed.add_field(name='Vouches Received\n\n',
                    value=f'{len(u.vouches)}\n\n')
    embed.add_field(name='Trusted Level\n\n',
                    value=f'{trusted}\n\n')
    embed.add_field(name='Scammer:\n\n',
                    value=f'{IsScammer} {warning}')


    if u.isScammer:
        authorName = f'💀{str(targetUser)} 💀'
    elif u.dwc:
        authorName = f'⚠️{str(targetUser)} ⚠️'
    else:
        authorName = f'{str(targetUser)}\'s Profile'
        


    embed.set_author(name=authorName, icon_url=targetUser.avatar_url)
    embed.set_footer(text="Account created " + str(daysLeft.days) +" days ago" + "      Joined market " + str(daysLeft2.days) + " days ago")
    await channel.send(embed=embed)
    



async def profile2(targetUser: discord.User, bcGuild: discord.Guild,
                  channel: discord.TextChannel):
    '''
        If a user is mentioned, it will display their profiles
        details. If a user isn't mentioned, then the author's
        profile is displayed.
    '''
    u = User(targetUser.id)

    today = datetime.utcnow()
    accountcreated = targetUser.created_at
    daysLeft = today - accountcreated


    # Decide a proper color
    if u.isScammer:
      color = RED
    else:
      color = GREY

    trusted = '0'

    dwcMsg = u.dwcReason + '\n' if u.dwc > 0 else ''
    dwcTitle = '' if u.dwc == 0 else f'**Deal with caution{danger} ** '


    TotalReviews = u.fiveratingsgiven + u.fourratingsgiven + u.threeratingsgiven + u.tworatingsgiven + u.oneratingsgiven
    if TotalReviews == 0:
      TotalReviews = 0
    AverageWeightRating = (u.fiveratingsgiven)*5 + (u.fourratingsgiven)*4 + (u.threeratingsgiven)*3 + (u.tworatingsgiven)*2 + (u.oneratingsgiven)*1
    if AverageWeightRating == 0:
      AverageWeightRating = 0
      
    try:
      AverageRatings = AverageWeightRating/TotalReviews
    except ZeroDivisionError:
      AverageRatings = 0

    if AverageRatings >= 5:
      Ratings = '★★★★★'
    elif AverageRatings >= 4:
      Ratings = '★★★★☆'
    elif AverageRatings >= 3:
      Ratings = '★★★☆☆'
    elif AverageRatings >= 2:
      Ratings = '★★☆☆☆'
    elif AverageRatings >= 1:
      Ratings = '★☆☆☆☆'
    elif AverageRatings >= 0:
      Ratings = '☆☆☆☆☆'

    if u.isScammer:
      IsScammer = "Yes"
    else:
      IsScammer = "No"

     
    totalratings = round(AverageRatings, 1)



    # Add relevant information
    embed = newEmbed(description='', title='', color=color)
    # embed.add_field(name='Vouch Information\n\n',
    #                value=f'\n\n**Vouches Given:** {u.vouchesgiven} \n\n**Vouchs Received:** {len(u.vouches)}')
    embed.add_field(name='Rating\n\n',
                    value=f'{Ratings} `{totalratings}/5`')
    embed.add_field(name='Vouches Given\n\n',
                    value=f'{u.vouchesgiven}\n\n')
    embed.add_field(name='Vouches Received\n\n',
                    value=f'{len(u.vouches)}\n\n')
    embed.add_field(name='Trusted Level\n\n',
                    value=f'{trusted}\n\n')
    embed.add_field(name='Scammer:\n\n',
                    value=f'{IsScammer}')


    if u.isScammer:
        authorName = f'💀{str(targetUser)} 💀'
    elif u.dwc:
        authorName = f'⚠️{str(targetUser)} ⚠️'
    else:
        authorName = f'{str(targetUser)}\'s Profile'
        


    embed.set_author(name=authorName, icon_url=targetUser.avatar_url)
    embed.set_footer(text="Account created " + str(daysLeft.days) +" days ago" + "      Left/Banned")
    await channel.send(embed=embed)