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

class Permission(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def permission(self, ctx, action, user: discord.User, *, permission=""):
        
        if action == "add":
            connect = self.bot.get_cog("Setup")
            conn = connect.connectdb()
            print("connected")
            c = conn.cursor()
            command = f"insert into permission(uid,perm,guild_id) values ({user.id},'{permission}',{ctx.guild.id})"
            print(command)
            c.execute(command)
            conn.commit()
            c.close()
            conn.close()
            await ctx.send(f"Permission {permission} added to <@{user.id}>")
            log = self.bot.get_cog("Logger")
            await log.logger(command=f"**Gave permision** {permission} to {user.name}", user=ctx.author, channel=ctx.channel, color="#0ff231", guild=ctx.message.guild.id)

        elif action == "remove":
            connect = self.bot.get_cog("Setup")
            conn = connect.connectdb()
            c = conn.cursor()
            command = f"delete from permission where perm = '{permission}' and uid = {user.id} and guild_id = {ctx.guild.id}"
            print(command)
            c.execute(command)
            conn.commit()
            c.close()
            conn.close()
            await ctx.send(f"Permission {permission} removed to <@{user.id}>")
            log = self.bot.get_cog("Logger")
            await log.logger(command=f"**Removed permision** {permission} from {user.name}", user=ctx.author, channel=ctx.channel, color="#f20f0f", guild=ctx.message.guild.id)

        elif action == "show":
            connect = self.bot.get_cog("Setup")
            conn = connect.connectdb()
            c = conn.cursor()
            command = f"SELECT * FROM permission WHERE uid = {user.id} and guild_id = {ctx.guild.id}"
            print(command)
            c.execute(command)
            results = c.fetchall()
            conn.commit()
            c.close()
            conn.close()
            if len(results) != 0:
                embedVar7 = discord.Embed(title=f"Permissions for {user.name}:", color=0x00ff00)
                print(results)
                for i in range(len(results)):
                    embedVar7.add_field(name=f"{results[i][2]}", value=f"$PLACEHOLDER_DESCRIPTION$", inline=False)
                await ctx.send(embed=embedVar7)
            else:
                embedVar7 = discord.Embed(title=f"{user.name} has no permissions", color=0x00ff00)
                await ctx.send(embed=embedVar7)
            

    @permission.error
    async def permission_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You are not an administrator!")
            log = self.bot.get_cog("Logger")
            await log.logger(command=f"Tried to use **permission** but lacks discord ***Administrator*** permission", user=ctx.author, channel=ctx.channel, color="#f54242", guild=ctx.message.guild.id)
    

def setup(bot):
    bot.add_cog(Permission(bot))