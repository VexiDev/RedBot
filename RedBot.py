from discord.ext import commands
from discord.voice_client import VoiceClient
from discord.ext.commands import CommandNotFound
from  builtins import any
from discord import Intents
import discord
import requests
import os
import asyncio
import random
import psycopg2
import threading

TOKEN = 'TOKEN'
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!',intents=intents)
bot.remove_command('help')
bot.remove_command('kick')


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        await ctx.send("Unkown command! Use **!help** for a list of available commands")

@bot.command()
async def load(ctx, extension):
    bot.load_extension(f'cogs.{extension}')
    await ctx.send(f"loaded {extension} c(p)og")

@bot.command()
async def unload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')
    await ctx.send(f"unloaded {extension} c(p)og")

@bot.command()
async def reload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')
    bot.load_extension(f'cogs.{extension}')
    await ctx.send(f"reloaded {extension} c(p)og")

#---------RUN--------------
bot.run(TOKEN)
