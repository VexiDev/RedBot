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

class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def testdb(self, ctx):
        print("testing")
        connect = self.bot.get_cog("Setup")
        conn = connect.connectdb()
        print("connected")
        c = conn.cursor()
        print("cursored")
        command = "select * from punishments where type='kick'"
        print(command)
        c.execute(command)
        print("executed")
        results = c.fetchall()
        print(results)
        conn.commit()
        c.close()
        conn.close()
        print("commited and closed connection")

def setup(bot):
    bot.add_cog(Test(bot))