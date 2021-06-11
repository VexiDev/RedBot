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

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def help(self, ctx):
        await ctx.send("Redbot is currently undergoing a recode and has no available features")

def setup(bot):
    bot.add_cog(Help(bot))