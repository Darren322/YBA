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
from discord.ext import commands, menus
from discordHelper import newEmbed, errorMessage, RED, BLUE, GREEN, YELLOW
from discord.ext.menus import button, First, Last

BLUE = 0x00A6ED
GREY = 0x999999
ass = 0xFFEFD5
cluster = MongoClient(config.MongoDBkey)


class Test:
    def __init__(self, value, comment, giver):
        self.value = value
        self.message = comment
        self.id = giver
    def __repr__(self):
        return f'{self.value}★ : {self.message} - <@!{self.id}>'

async def generate(number, vouches):
    for i in vouches:
        yield Test(i['Rating'], i['Message'], i['Giver'])

class Source(menus.AsyncIteratorPageSource):
    def __init__(self, userID: discord.Member):
        db = cluster[config.database][config.collection]  
        for document in db.find():
            self.allData = document
        search_users = 'Users[]'
        self.users = jmespath.search(search_users, self.allData)
        search_vouches = 'Users[?ID==`'+ str(userID.id) +'`].Vouches[]'
        search_ratings = 'Users[?ID==`'+ str(userID.id) +'`].Vouches[].Rating[]'
        totalvouchesreceived = jmespath.search(search_vouches, self.allData)
        totalratings = jmespath.search(search_ratings, self.allData)
        vouchestotal = int(len(totalvouchesreceived))
        self.user = userID
        super().__init__(generate(vouchestotal, totalvouchesreceived), per_page=10)


    async def format_page(self, menu, entries):
        start = menu.current_page * self.per_page
        return discord.Embed(
        title= f'Page {menu.current_page + 1} - {self.user}\'s reviews',
        description=f'\n'.join(f'`{i + 1}`. {v!r}' for i, v in enumerate(entries, start=start)),
        color= ass,
    )

class vouchcommands(commands.Cog):
  def __init__(self, client):
    self.client = client



  @commands.command(cooldown_after_parsing=True)
  @commands.cooldown(1, 900, type= commands.BucketType.user)
  async def vouch(self, ctx, member: discord.Member, ratings , *args):
      trade = (" ".join(args[:]))
      logChannel = self.client.get_channel(config.LOG_CHANNEL_ID)
      guild = ctx.guild
      vouchChannel = config.VOUCHES_CHANNEL_ID
      if member == ctx.author:
          await ctx.send("You cannot vouch for yourself.")
          ctx.command.reset_cooldown(ctx)
          return
      if member == self.client.user:
          await ctx.send('You cannot vouch for the bot')
          ctx.command.reset_cooldown(ctx)
          return

      try:
        ratings = int(ratings)
      except ValueError:
        await ctx.send(f"Please input a rating number between 1 to 5\n Eg: {config.PREFIX}vouch <@!322562448530079745> 5")
        ctx.command.reset_cooldown(ctx)
        return

      if len(args) < 7:
          await ctx.send("Please provide more details about the trade\n**Be specific**. Describe what you have sold/bought")
          ctx.command.reset_cooldown(ctx) 
          return

      if ctx.message.channel.id not in vouchChannel:
          await ctx.send(f'You only can use {config.PREFIX}vouch in **vouches** channel')
          ctx.command.reset_cooldown(ctx)
          return


      if ratings <= 0 or ratings > 5:
        await ctx.send(f'Please use appropriate rating number. \n Eg: {config.PREFIX}vouch <@!322562448530079745> 5')
        ctx.command.reset_cooldown(ctx)
        return

      if ctx.message.attachments:
          attachment = ctx.message.attachments[0].url
      else:
          attachment = None


      isPositive = 'true'
      success = await userCommands.vouch(ctx.author,
                              member,
                              trade,
                              isPositive,
                              guild,
                              logChannel,
                              ratings,
                              attachment
                              )
      if success == False:
          await ctx.author.send("You have been blacklisted from vouching!")
      elif success == True:
          await ctx.send(f"**{ctx.author}** has vouched **{member}**")




  @commands.command(name ="getrole", aliases=["getroles"])
  async def getrole(self, ctx):
      success = await userCommands.getrole(ctx.author,
      bcGuild= self.client.get_guild(ctx.guild.id),
      channel= ctx.message.channel)
      if success:
          await ctx.send(f"You have been given **{success[1]}**.")
      else:
          await ctx.send("You are not qualified for any new roles.")


  @commands.command(name ="profile", aliases=["vouches"])
  async def profile(self, ctx, member: discord.Member = None):
      if member is None:
          person = ctx.author
      else:
          person = member
      print("hi")
      vc = await userCommands.profile(ctx,
            targetUser=person,
          bcGuild=self.client.get_guild(ctx.guild.id),
          channel= ctx.message.channel)

      print("hi")

      await vc.add_reaction("🔍")  

 
      def check(reaction, user):
          return user == ctx.author and str(reaction.emoji) in ['🔍']
        
      while True:
          try:
              reaction, user = await self.client.wait_for('reaction_add', timeout = 20.0, check= check)
              if reaction.emoji == '🔍':
                  pages = menus.MenuPages(source=Source(person), delete_message_after = True)
                  await pages.start(ctx)
          except asyncio.TimeoutError:
              await vc.remove_reaction
              break


  @commands.command()
  async def vhelp(self, ctx):
      vouchAdmin_role = discord.utils.get(ctx.guild.roles, id=config.vouchadmin_role)
      if vouchAdmin_role in ctx.author.roles:
          isMaster = True
      else:
          isMaster = False
      await userCommands.help(config.PREFIX, ctx.author, isMaster)


  @vouch.error
  async def on_command_error_vouch(self, ctx, error):
      if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
          await ctx.send(f'Please follow this format: \n{config.PREFIX}vouch <@!322562448530079745> 5 Bought suke for $10,000. Easy and fast trade')
      if isinstance(error, discord.ext.commands.errors.MemberNotFound):
          await ctx.send(f'User not in the server!')
      if isinstance(error, commands.CommandOnCooldown):
          await ctx.message.delete()
          msg = '**Still on cooldown**, please try again in {:.2f}s'.format(error.retry_after)
          await ctx.author.send(msg)



  @profile.error
  async def on_command_error10(self, ctx, error):
      if isinstance(error, discord.ext.commands.errors.MemberNotFound):
          message = str(error)
          message2 = message.split()[1]
          memberid = message2.strip('""')
          db = cluster[config.database][config.collection]  
          search_users = 'Users[]'
          for document in db.find():
            allData = document
          users = jmespath.search(search_users, allData)
          for i in users:
            if int(memberid) == i['ID']:
                userid = int(memberid)
                User = await self.client.fetch_user(userid)
                await userCommands.profile2(targetUser = User, 
                bcGuild=self.client.get_guild(config.GUILD_ID), channel = ctx.channel)
                break
          else:
            await ctx.send("User has never been in this server")
            


          
def setup(client):
  client.add_cog(vouchcommands(client))

