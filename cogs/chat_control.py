import discord
from discord.ext import commands
from  builtins import any
from discord import Intents
import requests
import os
import random
import asyncio
import datetime
from io import BytesIO
import psycopg2

class ChatControl(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        user = member
        logtime = datetime.datetime.now()
        logtime = logtime.strftime("%m-%d-%Y at %I:%M %p")
        if not before.channel:
            print(f"{member.name} joined a vc")
            if after.channel.id == 775827793010622475:
                channel = discord.utils.get(member.guild.channels, name="muted-voice-1")
                print(member)
                overwrite = discord.PermissionOverwrite()
                overwrite.view_channel = True
                overwrite.send_messages = True
                await channel.set_permissions(member, overwrite=overwrite)
                await channel.send(f"User {member.name} has joined the VC and can now see this channel")
            elif after.channel.id == 760033559796121630:
                channel = discord.utils.get(member.guild.channels, name="muted-voice-2")
                print(member)
                overwrite = discord.PermissionOverwrite()
                overwrite.view_channel = True
                overwrite.send_messages = True
                await channel.set_permissions(member, overwrite=overwrite)
                await channel.send(f"User {member.name} has joined the VC and can now see this channel")

        if before.channel and not after.channel:
            print("someone left")
            memids = []
            members = before.channel.members
            for member in members:
                memids.append(member.id)
            if len(memids) == 0:
                print("no members left in vc")
                if before.channel.id == 775827793010622475:
                    permchannel = discord.utils.get(user.guild.channels, name="muted-voice-1")
                    print(user)
                    overwrite = discord.PermissionOverwrite()
                    overwrite.view_channel = False
                    overwrite.send_messages = False
                    await permchannel.set_permissions(user, overwrite=overwrite)
                    await permchannel.send(f"{user.name} has left the VC and can no longer see this channel")
                    text_channel = discord.utils.get(member.guild.channels, name="muted-voice-1")
                    await text_channel.send("The VC associated with this channel is empty, the chat will clear in 30 seconds")
                    await asyncio.sleep(30)
                    filename = f'{datetime.datetime.now().strftime("%m-%d-%Y LOG")}.txt'
                    with open(filename, "w") as file:
                        async for msg in text_channel.history(limit=None):
                            file.write(f"{logtime} - {msg.author.name}: {msg.clean_content}\n")
                    file = discord.File(fp=filename, filename=f'{datetime.datetime.now().strftime("%m-%d-%Y LOG")}.txt')
                    guild = member.guild.id
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
                    channel = self.bot.get_channel(results[0][2])
                    await channel.send("**VC-1** is empty, log file created and no-mic chat wiped (log is newest to oldest messages)")
                    await channel.send(file=file)
                    new_text = await text_channel.clone(reason="VC is empty, channel cleared")
                    await text_channel.delete()
                    os.remove(filename)
                    print("user left so purged")

                elif before.channel.id ==  760033559796121630:
                    permchannel = discord.utils.get(user.guild.channels, name="muted-voice-2")
                    print(user)
                    overwrite = discord.PermissionOverwrite()
                    overwrite.view_channel = False
                    overwrite.send_messages = False
                    await permchannel.set_permissions(user, overwrite=overwrite)
                    text_channel = discord.utils.get(member.guild.channels, name="muted-voice-2")
                    await permchannel.send(f"{user.name} has left the VC and can no longer see this channel")
                    await text_channel.send("The VC associated with this channel is empty, the chat will clear in 30 seconds")
                    await asyncio.sleep(30)
                    filename = f'{datetime.datetime.now().strftime("%m-%d-%Y LOG")}.txt'
                    with open(filename, "w") as file:
                        async for msg in text_channel.history(limit=None):
                            file.write(f"{logtime} - {msg.author.name}: {msg.clean_content}\n")
                    file = discord.File(fp=filename, filename=f'{datetime.datetime.now().strftime("%m-%d-%Y LOG")}.txt')
                    guild = member.guild.id
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
                    channel = self.bot.get_channel(results[0][2])
                    await channel.send("**VC-2** is empty, log file created and no-mic chat wiped (log is newest to oldest messages)")
                    await channel.send(file=file)
                    new_text = await text_channel.clone(reason="VC is empty, channel cleared")
                    await text_channel.delete()
                    os.remove(filename)
                    print("user left so purged")
                else: 
                    print("not correct vc")

            elif len(members) != 0:
                if before.channel == 775827793010622475:
                    permchannel = discord.utils.get(user.guild.channels, name="muted-voice-1")
                    print(user)
                    overwrite = discord.PermissionOverwrite()
                    overwrite.view_channel = False
                    overwrite.send_messages = False
                    await permchannel.set_permissions(user, overwrite=overwrite)
                    await permchannel.send(f"{user.name} has left the VC and can no longer see this channel")

                elif before.channel == 760033559796121630:
                    permchannel = discord.utils.get(user.guild.channels, name="muted-voice-1")
                    print(user)
                    overwrite = discord.PermissionOverwrite()
                    overwrite.view_channel = False
                    overwrite.send_messages = False
                    await permchannel.set_permissions(user, overwrite=overwrite)
                    await permchannel.send(f"{user.name} has left the VC and can no longer see this channel")


def setup(bot):
    bot.add_cog(ChatControl(bot))