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
import math
import youtube_dl
import os


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @bot.command()
    async def play(ctx, url : str):
        song_there = os.path.isfile("song.mp3")
        try:
            if song_there:
                os.remove("song.mp3")
        except PermissionError:
            await ctx.send("Wait for the current playing music to end or use the 'stop' command")
            return

        voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='General')
        await voiceChannel.connect()
        voice = discord.utils.get(bot.voice_bots, guild=ctx.guild)

        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        for file in os.listdir("./"):
            if file.endswith(".mp3"):
                os.rename(file, "song.mp3")
        voice.play(discord.FFmpegPCMAudio("song.mp3"))
        
    @bot.command()
    async def play(ctx, url : str):
        song_there = os.path.isfile("song.mp3")
        try:
            if song_there:
                os.remove("song.mp3")
        except PermissionError:
            await ctx.send("Wait for the current playing music to end or use the 'stop' command")
            return

        voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='General')
        await voiceChannel.connect()
        voice = discord.utils.get(bot.voice_bots, guild=ctx.guild)

        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        for file in os.listdir("./"):
            if file.endswith(".mp3"):
                os.rename(file, "song.mp3")
        voice.play(discord.FFmpegPCMAudio("song.mp3"))


    @bot.command()
    async def leave(ctx):
        voice = discord.utils.get(bot.voice_bots, guild=ctx.guild)
        if voice.is_connected():
            await voice.disconnect()
        else:
            await ctx.send("The bot is not connected to a voice channel.")


    @bot.command()
    async def pause(ctx):
        voice = discord.utils.get(bot.voice_bots, guild=ctx.guild)
        if voice.is_playing():
            voice.pause()
        else:
            await ctx.send("Currently no audio is playing.")


    @bot.command()
    async def resume(ctx):
        voice = discord.utils.get(bot.voice_bots, guild=ctx.guild)
        if voice.is_paused():
            voice.resume()
        else:
            await ctx.send("The audio is not paused.")

    @bot.command()
    async def help(ctx):
        embedVar.add_field(name='')


    @bot.command()
    async def stop(ctx):
        voice = discord.utils.get(bot.voice_bots, guild=ctx.guild)
        voice.stop()


    @bot.command()
    async def seduce(ctx, url : orville peck dead of night, user: discord.User):
        await ctx.send(f" <@{ctx.author.id}> seduces <@{user.id}> ")

        song_there = os.path.isfile("song.mp3")
        try:
            if song_there:
                os.remove("song.mp3")
        except PermissionError:
            await ctx.send("Wait for the current playing music to end or use the 'stop' command")
            return

        voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='General')
        await voiceChannel.connect()
        voice = discord.utils.get(bot.voice_bots, guild=ctx.guild)

        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        for file in os.listdir("./"):
            if file.endswith(".mp3"):
                os.rename(file, "song.mp3")
        voice.play(discord.FFmpegPCMAudio("song.mp3"))

    @bot.command()
    async def lefish(ctx, url : le fish full version, user: discord.User):
        await ctx.send(f" ITS LE FISH TIME <@{ctx.author.id}> ")

        song_there = os.path.isfile("song.mp3")
        try:
            if song_there:
                os.remove("song.mp3")
        except PermissionError:
            await ctx.send("Wait for the current playing music to end or use the 'stop' command")
            return

        voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='General')
        await voiceChannel.connect()
        voice = discord.utils.get(bot.voice_bots, guild=ctx.guild)

        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        for file in os.listdir("./"):
            if file.endswith(".mp3"):
                os.rename(file, "song.mp3")
        voice.play(discord.FFmpegPCMAudio("song.mp3"))

    @bot.command()
    async def chesstime(ctx, url : yakuza OST baka mitai)
        await ctx.send(f" wow Ann going full tryhard now")

        song_there = os.path.isfile("song.mp3")
        try:
            if song_there:
                os.remove("song.mp3")
        except PermissionError:
            await ctx.send("Wait for the current playing music to end or use the 'stop' command")
            return

        voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='General')
        await voiceChannel.connect()
        voice = discord.utils.get(bot.voice_bots, guild=ctx.guild)

        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        for file in os.listdir("./"):
            if file.endswith(".mp3"):
                os.rename(file, "song.mp3")
        voice.play(discord.FFmpegPCMAudio("song.mp3"))

    @bot.command()
    async def glory(ctx, url : sabaton livgardet)
        await ctx.send(f" Ärat livgardet står, Grundat av landsfader vår, Hängiven tjänst i 500 år, Från tåget över Bält")

        song_there = os.path.isfile("song.mp3")
        try:
            if song_there:
                os.remove("song.mp3")
        except PermissionError:
            await ctx.send("Wait for the current playing music to end or use the 'stop' command")
            return

        voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='General')
        await voiceChannel.connect()
        voice = discord.utils.get(bot.voice_bots, guild=ctx.guild)

        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        for file in os.listdir("./"):
            if file.endswith(".mp3"):
                os.rename(file, "song.mp3")
        voice.play(discord.FFmpegPCMAudio("song.mp3"))

    @bot.command()
    async def shuffle(ctx, url : skyrim shuffle)
        await ctx.send(f" ITS TIME TO SKYRIM SHUFFLE IN PRAISE OF OUR LORD TODD 'THE GOD' HOWARD")

        song_there = os.path.isfile("song.mp3")
        try:
            if song_there:
                os.remove("song.mp3")
        except PermissionError:
            await ctx.send("Wait for the current playing music to end or use the 'stop' command")
            return

        voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='General')
        await voiceChannel.connect()
        voice = discord.utils.get(bot.voice_bots, guild=ctx.guild)

        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        for file in os.listdir("./"):
            if file.endswith(".mp3"):
                os.rename(file, "song.mp3")
        voice.play(discord.FFmpegPCMAudio("song.mp3"))key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        for file in os.listdir("./"):
            if file.endswith(".mp3"):
                os.rename(file, "song.mp3")
        voice.play(discord.FFmpegPCMAudio("song.mp3"))


    @bot.command()
    async def leave(ctx):
        voice = discord.utils.get(bot.voice_bots, guild=ctx.guild)
        if voice.is_connected():
            await voice.disconnect()
        else:
            await ctx.send("The bot is not connected to a voice channel.")


    @bot.command()
    async def pause(ctx):
        voice = discord.utils.get(bot.voice_bots, guild=ctx.guild)
        if voice.is_playing():
            voice.pause()
        else:
            await ctx.send("Currently no audio is playing.")


    @bot.command()
    async def resume(ctx):
        voice = discord.utils.get(bot.voice_bots, guild=ctx.guild)
        if voice.is_paused():
            voice.resume()
        else:
            await ctx.send("The audio is not paused.")

    @bot.command()
    async def help(ctx):
        embedVar.add_field(name='')


    @bot.command()
    async def stop(ctx):
        voice = discord.utils.get(bot.voice_bots, guild=ctx.guild)
        voice.stop()


    @bot.command()
    async def seduce(ctx, url : orville peck dead of night, user: discord.User):
        await ctx.send(f" <@{ctx.author.id}> seduces <@{user.id}> ")

        song_there = os.path.isfile("song.mp3")
        try:
            if song_there:
                os.remove("song.mp3")
        except PermissionError:
            await ctx.send("Wait for the current playing music to end or use the 'stop' command")
            return

        voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='General')
        await voiceChannel.connect()
        voice = discord.utils.get(bot.voice_bots, guild=ctx.guild)

        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        for file in os.listdir("./"):
            if file.endswith(".mp3"):
                os.rename(file, "song.mp3")
        voice.play(discord.FFmpegPCMAudio("song.mp3"))

    @bot.command()
    async def lefish(ctx, url : le fish full version, user: discord.User):
        await ctx.send(f" ITS LE FISH TIME <@{ctx.author.id}> ")

        song_there = os.path.isfile("song.mp3")
        try:
            if song_there:
                os.remove("song.mp3")
        except PermissionError:
            await ctx.send("Wait for the current playing music to end or use the 'stop' command")
            return

        voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='General')
        await voiceChannel.connect()
        voice = discord.utils.get(bot.voice_bots, guild=ctx.guild)

        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        for file in os.listdir("./"):
            if file.endswith(".mp3"):
                os.rename(file, "song.mp3")
        voice.play(discord.FFmpegPCMAudio("song.mp3"))

    @bot.command()
    async def chesstime(ctx, url : yakuza OST baka mitai)
        await ctx.send(f" wow Ann going full tryhard now")

        song_there = os.path.isfile("song.mp3")
        try:
            if song_there:
                os.remove("song.mp3")
        except PermissionError:
            await ctx.send("Wait for the current playing music to end or use the 'stop' command")
            return

        voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='General')
        await voiceChannel.connect()
        voice = discord.utils.get(bot.voice_bots, guild=ctx.guild)

        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        for file in os.listdir("./"):
            if file.endswith(".mp3"):
                os.rename(file, "song.mp3")
        voice.play(discord.FFmpegPCMAudio("song.mp3"))

    @bot.command()
    async def glory(ctx, url : sabaton livgardet)
        await ctx.send(f" Ärat livgardet står, Grundat av landsfader vår, Hängiven tjänst i 500 år, Från tåget över Bält")

        song_there = os.path.isfile("song.mp3")
        try:
            if song_there:
                os.remove("song.mp3")
        except PermissionError:
            await ctx.send("Wait for the current playing music to end or use the 'stop' command")
            return

        voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='General')
        await voiceChannel.connect()
        voice = discord.utils.get(bot.voice_bots, guild=ctx.guild)

        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        for file in os.listdir("./"):
            if file.endswith(".mp3"):
                os.rename(file, "song.mp3")
        voice.play(discord.FFmpegPCMAudio("song.mp3"))

    @bot.command()
    async def shuffle(ctx, url : skyrim shuffle)
        await ctx.send(f" ITS TIME TO SKYRIM SHUFFLE IN PRAISE OF OUR LORD TODD 'THE GOD' HOWARD")

        song_there = os.path.isfile("song.mp3")
        try:
            if song_there:
                os.remove("song.mp3")
        except PermissionError:
            await ctx.send("Wait for the current playing music to end or use the 'stop' command")
            return

        voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='General')
        await voiceChannel.connect()
        voice = discord.utils.get(bot.voice_bots, guild=ctx.guild)

        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        for file in os.listdir("./"):
            if file.endswith(".mp3"):
                os.rename(file, "song.mp3")
        voice.play(discord.FFmpegPCMAudio("song.mp3"))


def setup(bot):
    bot.add_cog(Music(bot))