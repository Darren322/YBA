#cython: language_level=3

import discord
import os
import config
import bson
from discordHelper import User, Vouch, newEmbed, errorMessage, RED, BLUE, GREEN, YELLOW
from pymongo import MongoClient
import jmespath

cluster = MongoClient(config.MongoDBkey)
obj_id = bson.ObjectId(config.obj_id)




async def removemany(targetUser: discord.User,
                 channel: discord.TextChannel,
                 No: int):
    '''
        Lists vouches for a person and
        deletes a specific vouch
    '''
    db = cluster[config.database][config.collection]  
    for x in range(No):
        for document in db.find():
            alldata = document
        searchuser_vouches = 'Users[?ID==`'+ str(targetUser.id) +'`]'
        searchaddedVouch = '[].Vouches[?Message==`This is added vouch`].ID[]'
        totalvouchesgiven = jmespath.search(searchuser_vouches, alldata)
        totalvouchesadded = jmespath.search(searchaddedVouch, totalvouchesgiven)
        vouchID = totalvouchesadded[0]
        db.update_one({'_id': obj_id, 'Users.ID': targetUser.id}, {'$pull': {'Users.$[i].Vouches': {'ID': vouchID}}}, array_filters= [{'i.ID': targetUser.id}])

    return True



async def scammer(targetUser: discord.User, channel: discord.TextChannel):
    '''
        Toggles Scammer role to mentioned user
    '''
    u = User(targetUser.id)
    vouches = u.vouches
    u.setScammer(not u.isScammer, targetUser.id)

    if u.isScammer:
        return True, targetUser.mention
    else:
        return False, targetUser.mention


async def staff(targetUser: discord.User, channel: discord.TextChannel):
    '''
        Toggles Master privileges to mentioned user
    '''
    db = cluster[config.database][config.collection]  

    if db.find_one({'_id': obj_id, 'Staff': {"$in": [targetUser.id]}}):
        db.update_one({'_id': obj_id},{'$pull': {'Staff': targetUser.id}})
        return False
    else:
        db.update_one({'_id': obj_id},{'$push': {'Staff': targetUser.id}})
        return True

async def admin(targetUser: discord.User, channel: discord.TextChannel):
    '''
        Toggles Master privileges to mentioned user
    '''
    db = cluster[config.database][config.collection]  

    if db.find_one({'_id': obj_id, 'Masters': {"$in": [targetUser.id]}}):
        db.update_one({'_id': obj_id},{'$pull': {'Masters': targetUser.id}})
        return False
    else:
        db.update_one({'_id': obj_id},{'$push': {'Masters': targetUser.id}})
        return True
        

async def addVouches(user: discord.User,
                    targetUser: discord.User,
                    isPositive: bool,
                    curChannel: discord.TextChannel,
                    logChannel: discord.TextChannel,
                    No: int):

    '''
        Leaves a vouch for a user
    '''
    db = cluster[config.database][config.collection]  
    u = User(user.id)
    vouches = u.vouches
    for document in db.find():
        allData = document
    # Create a new vouch
    for x in range(No):
        db = cluster[config.database][config.collection]   
        for document in db.find():
          allData = document
        vouchNum: int = allData['VouchCount'] + 1
        v = {
            'ID': vouchNum,
            'Giver': 0,
            'Receiver': targetUser.id,
            'IsPositive': "true",
            'Message': "This is added vouch",
            'Rating': 5
        }
        db.update_one({'_id': obj_id},{'$set': {'VouchCount': vouchNum}})
        target = str(targetUser.id)
        giverr = str(user.id)

        vouch = Vouch(v)
        db.update_one({'_id': obj_id, 'Users.ID': targetUser.id}, {'$push': {'Users.$[i].Vouches': vouch.toDict()}}, upsert = False, array_filters= [{'i.ID': targetUser.id}])
    
    return True



async def remove(targetUser: discord.User,
                 channel: discord.TextChannel,
                 vouchID: int = -1):
    '''
        Lists vouches for a person and
        deletes a specific vouch
    '''
    u = User(targetUser.id)

    # If a vouch ID wasn't passed in, then list them out
    if vouchID == -1:
        vouches = u.formatVouches()
        if len(vouches) == 0:
            vouches = 'No vouches to show!'
        embed = newEmbed(description=vouches, color=BLUE)
        await channel.send(embed=embed)
        return

    success = u.removeVouch(vouchID, targetUser.id)

    if success:
        return True, vouchID
    else:
        return False, vouchID

