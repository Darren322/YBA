import random
import string
import discord
import jmespath
import datetime
import config
from pymongo import MongoClient
import bson
import os

RED = 0xEF233C
BLUE = 0x00A6ED
GREEN = 0x3EC300
YELLOW = 0xFFB400
ORANGE = 0xFF7106
PINK = 0xFF1493
WHITE = 0xFFFFFF
AQUA = 0x00FFFF
LBLUE = 0x00FFFF
L2BLUE = 0x4682B4
L3BLUE = 0x008080
L4BLUE = 0x191970
L5BLUE =0x1d0550
GREY = 0x999999


cluster = MongoClient(config.MongoDBkey)
obj_id = bson.ObjectId(config.obj_id)

class Vouch:
    def __init__(self, vouchData: dict):
        self.vouchID = vouchData.get('ID', -1)
        self.message = vouchData.get('Message', '')
        self.rating = vouchData.get('Rating', 0)
        self.giverID = vouchData.get('Giver', 0)
        self.receiverID = vouchData.get('Receiver', 0)
        self.isPositive = vouchData.get('IsPositive', True)

    def toDict(self) -> dict:
        '''
            Represents the Vouch object as a dictionary
        '''
        return {
            'ID': self.vouchID,
            'Message': self.message,
            'Giver': self.giverID,
            'Receiver': self.receiverID,
            'IsPositive': self.isPositive,
            'Rating': self.rating
        }


class User:
    def __init__(self, userID: int, allData: dict = None):
        db = cluster[config.database][config.collection]  
        for document in db.find():
            self.allData = document
        search_users = 'Users[]'
        self.userID = int(userID)
        self.users = jmespath.search(search_users, self.allData)
        search_vouches = "Users[*].Vouches[*].Giver[]"
        search_ratings = 'Users[?ID==`'+ str(userID) +'`].Vouches[].Rating[]'
        

        # Find the user in the database
        for i in self.users:
            if userID == i['ID']:
                userData = i
                self.isNewUser = False
                break
        else:
            self.isNewUser = True
            userData = {}


        if db.find_one({'_id': obj_id, 'Masters': {"$in": [userID]}}):
            IsMaster = 'true'
        else:
            IsMaster = 'false'

        self.isMaster = IsMaster
        self.dwc = userData.get('DWC',0)
        if self.dwc is False or self.dwc is True:
            self.dwc = 0
        self.link = userData.get('Link', '')
        self.dwcReason = userData.get('DWC Reason', '')
        self.isScammer = userData.get('Scammer', False)
        self.token = userData.get('Token', generateToken())
        self.verified = userData.get('Verified', False)
        # Convert the data to Vouch objects
        totalvouchesgiven = jmespath.search(search_vouches, self.allData)
        totalratingsgiven = jmespath.search(search_ratings, self.allData)        
        self.vouches = [Vouch(i) for i in userData.get('Vouches', [])]
        self.vouchesgiven = totalvouchesgiven.count(userID)
        self.fiveratingsgiven = totalratingsgiven.count(5)
        self.fourratingsgiven = totalratingsgiven.count(4)
        self.threeratingsgiven = totalratingsgiven.count(3)
        self.tworatingsgiven = totalratingsgiven.count(2)
        self.oneratingsgiven = totalratingsgiven.count(1)
        self.posVouchCount = len([i for i in self.vouches if i.isPositive])
        self.negVouchCount = len(self.vouches) - self.posVouchCount

        if self.isNewUser:
            self.save()


    def formatVouches(self) -> string:
        '''
            Lists the vouches in an organized string
        '''
        vouches = ''
        prevLength = 0
        # Combine all the vouch messages into a list
        for i in self.vouches[::-1]:
            s = f'**ID** {i.vouchID} | {i.message}\n'
            # We have to make sure the string total is less than
            # 2048 characters otherwise discord wont send it
            if len(vouches) + prevLength <= 2048:
                prevLength += len(s)
                vouches += s
            else:
                break

        return vouches.strip()

    def setScammer(self, scammer: bool, user: int):
        '''
            Sets the user as a scammer or not
        '''
        self.isScammer = scammer
        db = cluster[config.database][config.collection]  
        db.update_one({'_id': obj_id, 'Users.ID': user}, {'$set': {'Users.$[i].Scammer': scammer}}, array_filters= [{'i.ID': user}])

    def removeVouch(self, vouchID: int, user: int):
        '''
            Removes a vouch from the user and database
        '''
        db = cluster[config.database][config.collection]
        print("tesets")
        for i, x in enumerate(self.vouches):
            if x.vouchID == vouchID:
                print("ass")
                db.update_one({'_id': obj_id, 'Users.ID': user}, {'$pull': {'Users.$[i].Vouches': {'ID': vouchID}}}, array_filters= [{'i.ID': user}])
                print("Gay")
                break
        else:
            return False

        return True


    def save(self):
        '''
            Saves the current user into the database
        '''
        collection = cluster[config.database][config.collection]         
        d = {
            'ID': self.userID,
            'Token': self.token,
            'DWC': self.dwc,
            'DWC Reason': self.dwcReason,
            'Vouches': [i.toDict() for i in self.vouches],
            'Link': self.link,
            'Scammer': self.isScammer,
            'Verified': self.verified,
            'PositiveVouches': len([i for i in self.vouches if i.isPositive]),
            'NegativeVouches': len(self.vouches) - self.posVouchCount,
            '5 Ratings': self.fiveratingsgiven,
            '4 Ratings': self.fourratingsgiven,
            '3 Ratings': self.threeratingsgiven,
            '2 Ratings': self.tworatingsgiven,
            '1 Ratings': self.oneratingsgiven,
        }

        for i, x in enumerate(self.users):
            if x['ID'] == self.userID:
                self.users[i] = d
                break
        else:
            collection.update_one({'_id': obj_id},{'$push': {'Users': d}}) 
        

async def errorMessage(message: str, channel: discord.TextChannel):
    '''
        Sends an error message to a channel
    '''
    embed = newEmbed(message, color=RED, title='Error')
    await channel.send(embed=embed)


def newEmbed(description: str,
             color: hex = BLUE,
             title: str = config.Server_Name) -> discord.Embed:
    '''
        Creates a new Embed object
    '''
    return discord.Embed(
        title=title,
        description=description,
        color=color,
    )


def generateToken() -> str:
    return ''.join(random.choices(string.hexdigits, k=16)).upper()

def convert_timedelta(duration):
    days, seconds = duration.days, duration.seconds
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = (seconds % 60)
    return days, hours, minutes, seconds