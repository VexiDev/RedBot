import discord
from discord.ext import commands
from  builtins import any
from discord import Intents
import requests
import os
import random
import asyncio
import datetime
import psycopg2
import threading

class Setup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    
    loop = asyncio.get_event_loop()

    async def _checkstreamthread(self):
        while True:
            twitch = self.bot.get_cog("AutoTwitch")
            try:
                await twitch.checkstream()
            except:
                pass

    def checkstreamthread(self):
        t = threading.Thread(target=asyncio.run, args=(self._checkstreamthread(),))
        t.start()
        print("started thread")

    def connectdb(self):
        conn = psycopg2.connect(        
        host="host",
        database="dbname",
        user="user",
        password="pass") 
        return(conn)

    def getpermission(self, ctx):
        conn = self.connectdb()
        print("connected")
        c = conn.cursor()
        print("cursored")
        command= f"select * from permission where uid={ctx.author.id} and guild_id = {ctx.guild.id}"
        print(command)
        c.execute(command)
        print("executed")
        permissions = c.fetchall()
        print(permissions)
        conn.commit()
        c.close()
        conn.close()
        return permissions

    @commands.Cog.listener()
    async def on_ready(self):
        print("Sucessfully connected to RedBot!")
        self.checkstreamthread()
        await self.change_status()

    async def change_status(self):
        statusType=0
        while True:
            if statusType == 0:
                await self.bot.change_presence(status=discord.Status.dnd, activity=discord.Activity(type=discord.ActivityType.watching, name="twitch.tv/Redlumux"))
                statusType = 1
            else:
                await self.bot.change_presence(status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.watching, name="twitch.tv/Qloomii"))
                statusType=0
            await asyncio.sleep(60)


    @commands.command()
    async def setup(self, ctx):
        await ctx.send("Not available.")
        # updateEmbed = discord.Embed(title=f"Updated to v{results}", description=f"{ctx.author.name} updated RedBot", color=0xf5e642)
        # updateEmbed.add_field(name="Changelog:", value=f"{updated}",inline=False)
        # updateEmbed.set_thumbnail(url="https://cdn1.iconfinder.com/data/icons/lightly-selected/30/loop-480.png")

def setup(bot):
    bot.add_cog(Setup(bot))
