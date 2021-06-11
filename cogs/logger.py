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

class Logger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def logger(self, command, user, channel, color, guild):
        print("Started log")
        sixteenIntegerHex = int(color.replace("#", ""), 16)
        readableHex = int(hex(sixteenIntegerHex), 0)
        print("converted to readable hex")
        time = datetime.datetime.now()  
        time = time.strftime(r"%x at %H:%M")
        print("Set time")
        logEmbed = discord.Embed(title=f"{user}", description=f"{command} \n\n <#{channel.id}> | guildID: {guild} | {time}", color=readableHex)
        # logEmbed = discord.Embed(title=f"{user} has logtested", desc=f"{logtest} pog")
        print("Set embed")
        print(user.avatar_url)
        logEmbed.set_author(name=user, url=discord.Embed.Empty, icon_url=user.avatar_url)
        print("set embed author")
        connect = self.bot.get_cog("Setup")
        conn = connect.connectdb()
        c = conn.cursor()
        print("connected and cursored")
        command = f"select * from channels where type = 'logger' and guild_id = {guild}"
        print(command)
        c.execute(command)
        print("executed")
        results = c.fetchall()
        print(results)
        print(results[0][2])
        conn.commit()
        c.close()
        conn.close()
        print("closed connection")
        channelsend = self.bot.get_channel(results[0][2])
        print(channelsend)
        await channelsend.send(embed=logEmbed)
        print("sent")

    # async def logger(self, command, user, channel, color, guild):
    #     print("Started log")
    #     channelsend = self.bot.get_channel(839963726941519873)
    #     print("set log channel")
    #     sixteenIntegerHex = int(color.replace("#", ""), 16)
    #     readableHex = int(hex(sixteenIntegerHex), 0)
    #     print("converted to readable hex")
    #     time = datetime.datetime.now()  
    #     time = time.strftime(r"%x at %H:%M")
    #     print("Set time")
    #     print(command)
    #     logEmbed = discord.Embed(title=f"{user}", description=f"{command} \n\n <#{channel.id}> | guildID: {guild} | {time}", color=readableHex)
    #     print("Set embed")
    #     print(user.avatar_url)
    #     logEmbed.set_thumbnail(url=user.avatar_url)
    #     print("set embed thumbnail")
    #     await channelsend.send(embed=logEmbed)
    #     print("sent")
    #     print(f"{user} | {command} | channelID: {channel.id} | guildID: {guild} | {time}")

    
    @commands.command()
    async def setlogger(self, ctx):
        print(f"Channel {ctx.channel.id} selected")
        channel = ctx.channel.id
        print(channel)
        guild = ctx.guild.id
        print(guild)
        connect = self.bot.get_cog("Setup")
        conn = connect.connectdb()
        c = conn.cursor()
        print("Connected and cursored")
        command = f"select id from channels where guild_id={guild} and type='logger'"
        c.execute(command)
        print("executed")
        results = c.fetchall()
        results = str(results).replace(",)]", "")
        results = str(results).replace("[(", "")
        results = str(results).replace("[", "")
        results = str(results).replace("]", "")
        print(results)
        print(len(results))
        if len(results)==0:
            command5 = f"INSERT INTO channels(guild_id, channel_id, type) VALUES ({guild},{channel}, 'logger')"
            print(command5)
            c.execute(command5)
            print("executed")
        else:
            command5 = f"UPDATE channels SET channel_id={channel} where id = {results};" 
            command6 = f"UPDATE channels SET type='logger' where id = {results};"
            print(command5)
            print(command6)
            c.execute(command5)
            c.execute(command6)
            print("Logger set")
        conn.commit()
        c.close()
        conn.close()
        message=f"Chat <#{ctx.channel.id}> has been set as the log channel"
        print("message var set")
        await ctx.send(message)
        print("message sent")
        print("Channel succesfully set to logger")

def setup(bot):
    bot.add_cog(Logger(bot))