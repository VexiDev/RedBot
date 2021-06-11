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

class Joiner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def setwelcomer(self, ctx):
        print(f"Channel {ctx.channel.id} selected")
        channel = ctx.channel.id
        print(channel)
        guild = ctx.guild.id
        print(guild)
        connect = self.bot.get_cog("Setup")
        conn = connect.connectdb()
        c = conn.cursor()
        print("Connected and cursored")
        command = f"select id from channels where guild_id={guild} and type='welcome'"
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
            command5 = f"INSERT INTO channels(guild_id, channel_id, type) VALUES ({guild},{channel}, 'welcome')"
            print(command5)
            c.execute(command5)
            print("executed")
        else:
            command5 = f"UPDATE channels SET channel_id={channel} where id = {results};" 
            command6 = f"UPDATE channels SET type='welcome' where id = {results};"
            print(command5)
            print(command6)
            c.execute(command5)
            c.execute(command6)
            print("Logger set")
        conn.commit()
        c.close()
        conn.close()
        message=f"Chat <#{ctx.channel.id}> has been set as the welcome channel"
        print("message var set")
        await ctx.send(message)
        print("message sent")
        print("Channel succesfully set to welcome")


    @commands.command()
    async def setleaver(self, ctx):
        print(f"Channel {ctx.channel.id} selected")
        channel = ctx.channel.id
        print(channel)
        guild = ctx.guild.id
        print(guild)
        connect = self.bot.get_cog("Setup")
        conn = connect.connectdb()
        c = conn.cursor()
        print("Connected and cursored")
        command = f"select id from channels where guild_id={guild} and type='leaver'"
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
            command5 = f"INSERT INTO channels(guild_id, channel_id, type) VALUES ({guild},{channel}, 'leaver')"
            print(command5)
            c.execute(command5)
            print("executed")
        else:
            command5 = f"UPDATE channels SET channel_id={channel} where id = {results};" 
            command6 = f"UPDATE channels SET type='leaver' where id = {results};"
            print(command5)
            print(command6)
            c.execute(command5)
            c.execute(command6)
            print("Logger set")
        conn.commit()
        c.close()
        conn.close()
        message=f"Chat <#{ctx.channel.id}> has been set as the leaver channel"
        print("message var set")
        await ctx.send(message)
        print("message sent")
        print("Channel succesfully set to leaver")

    @commands.command()
    async def autorole(self, ctx, roles):
        print("Currently incomplete")

#------------EVENTS--------------

    @commands.Cog.listener()
    async def on_member_join(self, member):
        joinEmbed = discord.Embed(color=0xaa42f5)
        joinEmbed.set_thumbnail(url=member.avatar_url)
        joinEmbed.add_field(name=f"{member.name}", value=f"**has joined the server!**\n\n**Say Hello!**")
        connect = self.bot.get_cog("Setup")
        conn = connect.connectdb()
        c = conn.cursor()
        print("connected and cursored")
        command = f"select * from channels where type = 'welcome' and guild_id = {member.guild.id}"
        print(command)
        c.execute(command)
        print("executed")
        results = c.fetchall()
        print(results)
        conn.commit()
        c.close()
        conn.close()
        if len(results)!=0:
            await self.bot.get_channel(results[0][2]).send(embed=joinEmbed)
            await member.send(f"Welcome to {member.guild.name}. Before you continue make sure you read the rules and verify you're not a bot! If you have any questions feel free to ask the staff! Enjoy your stay")
        else:
            print("No welcome channel set")

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        embedVar2 = discord.Embed(color=0xaa42f5)
        embedVar2.set_thumbnail(url=member.avatar_url)
        embedVar2.add_field(name=f"{member.name}", value=f"**has left the server!**\n\n**Have a good life!! We'll miss you <3**")
        connect = self.bot.get_cog("Setup")
        conn = connect.connectdb()
        c = conn.cursor()
        print("connected and cursored")
        command = f"select * from channels where type = 'leaver' and guild_id = {member.guild.id}"
        print(command)
        c.execute(command)
        print("executed")
        results = c.fetchall()
        print(results)
        conn.commit()
        c.close()
        conn.close()
        if len(results)!=0:
            await self.bot.get_channel(results[0][2]).send(embed=embedVar2)
        else:
            print("No leave channel set")


def setup(bot):
    bot.add_cog(Joiner(bot))