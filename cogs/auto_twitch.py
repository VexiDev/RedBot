import discord
from  builtins import any
from discord import Intents
from discord.ext import tasks, commands
from twitchAPI.twitch import Twitch
import requests
import json
import os
import random
import asyncio
import datetime
import psycopg2
notified = {}
loop = asyncio.get_event_loop()

class AutoTwitch(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def checkstream(self):
        global loop
        global notified
        await asyncio.sleep(30)
        # print("going")
        # print("checking for lives")
        # print(notified)
        client_id = 'id'
        client_secret = 'secret'
        stream_data = {}
        # print("attempting to connect")
        connect = self.bot.get_cog("Setup")
        conn = connect.connectdb()
        # print("connected")
        c = conn.cursor()
        # print("cursored")
        command= f"select distinct on (twitchname)id, twitchname, guild_id, notifyrole from streams"
        # print(command)
        c.execute(command)
        # print("executed")
        all_streamers = c.fetchall()
        conn.commit()
        c.close()
        conn.close()
        # print(len(all_streamers))


        for current_name in all_streamers:
            # print(current_name)
            streamer_name = current_name[1]

            body = {
                'client_id': client_id,
                'client_secret': client_secret,
                "grant_type": 'client_credentials'
            }
            r = requests.post('https://id.twitch.tv/oauth2/token', body)

            #data output
            keys = r.json()

            # print(keys)

            headers = {
                'Client-ID': client_id,
                'Authorization': 'Bearer ' + keys['access_token']
            }

            # print(headers)

            stream = requests.get('https://api.twitch.tv/helix/streams?user_login=' + streamer_name, headers=headers)

            stream_data = stream.json()
            # print(len(stream_data['data']))
            # print(str(stream_data))

            # print(stream_data)

            if len(stream_data['data']) == 1 and (streamer_name not in notified.keys() or notified[streamer_name] == False):
                print(notified)
                print(streamer_name + ' is live: ' + stream_data['data'][0]['title'] + ' playing ' + stream_data['data'][0]['game_name'])
                StreamingEmbed = discord.Embed (
                title = f':red_circle:  LIVE  :red_circle: {streamer_name} is live!\n\n',
                description = f"**{stream_data['data'][0]['title']}**  \n// Streaming {stream_data['data'][0]['game_name']}\n\nWatch live now at https://twitch.tv/{streamer_name}",
                colour = 0xae34eb) 
                thumbnail = str(stream_data['data'][0]['thumbnail_url'])
                thumbnail = thumbnail.replace(f"{{width}}", "1920")
                thumbnail = thumbnail.replace(f"{{height}}", "1080")
                time = datetime.datetime.now()  
                time = time.strftime(r"%f")
                thumbnail = thumbnail+f"?={time}"
                print(thumbnail)
                StreamingEmbed.set_image(url=f"{thumbnail}")
                print("set url")
                loop.create_task(self.sendmessage(StreamingEmbed, streamer_name))
                # print("sent")
            elif len(stream_data['data']) == 0:
                # print(streamer_name + ' is not live')
                # print(f"notified = {notified}")
                notified[f"{streamer_name}"] = False
            else:
                # print("Already Notified")
                pass     
    
    
    async def sendmessage(self, StreamingEmbed, streamer):
        global notified 
        connect = self.bot.get_cog("Setup")
        conn = connect.connectdb()
        print("connected")
        c = conn.cursor()
        print("cursored")
        command= f"select * from streams where twitchname = '{streamer}'"
        print(command)
        c.execute(command)
        print("executed")
        all_streamers = c.fetchall()
        conn.commit()
        c.close()
        conn.close()
        conn = connect.connectdb()
        print("connected")
        c = conn.cursor()
        print("cursored")
        command= f"select * from channels where type = 'stream-announce'"
        print(command)
        c.execute(command)
        print("executed")
        all_channels = c.fetchall()
        conn.commit()
        c.close()
        conn.close()
        for streamer in all_streamers:
            await asyncio.sleep(5)
            for channels in all_channels:
                if channels[1] == streamer[2]:
                    guild = channels[1]
                    guild = self.bot.get_guild(guild)
                    notifyrole = discord.utils.get(guild.roles, name=streamer[3])
                    channel = self.bot.get_channel(channels[2])
                    await channel.send(f"[ <@&{notifyrole.id}> ]")
                    await channel.send(embed=StreamingEmbed)
                    print("sent")
                    notified[f"{streamer[1]}"] = True
                else:
                    print("not a match")
        

    @commands.command()
    async def setannouncer(self, ctx):
        permission = self.bot.get_cog("Setup")
        connect = self.bot.get_cog("Setup")
        permissions = permission.getpermission(ctx)
        permcount = 0
        for perms in permissions:
            if(perms[2] == 'channels.set.announcer'):
                print(f"Channel {ctx.channel.id} selected")
                channel = ctx.channel.id
                print(channel)
                guild = ctx.guild.id
                print(guild)
                connect = self.bot.get_cog("Setup")
                conn = connect.connectdb()
                c = conn.cursor()
                print("Connected and cursored")
                command = f"select id from channels where guild_id={guild} and type='stream-announce'"
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
                    command5 = f"INSERT INTO channels(guild_id, channel_id, type) VALUES ({guild},{channel}, 'stream-announce')"
                    print(command5)
                    c.execute(command5)
                    print("executed")
                else:
                    command5 = f"UPDATE channels SET channel_id={channel} where id = {results};" 
                    command6 = f"UPDATE channels SET type='stream-announce' where id = {results};"
                    print(command5)
                    print(command6)
                    c.execute(command5)
                    c.execute(command6)
                    print("Logger set")
                conn.commit()
                c.close()
                conn.close()
                message=f"Chat <#{ctx.channel.id}> has been set as the announcer channel"
                print("message var set")
                await ctx.send(message)
                print("message sent")
                print("Channel succesfully set to announce")
            else:
                permcount = permcount+1
        if permcount == len(permissions):
            await ctx.send("You lack permission to set channel type announcer")
            log = self.bot.get_cog("Logger")
            log.logger(command=f"Tried to set announcer channel but lacks permission", user=ctx.author, channel=ctx.channel, color="#f00000", guild=ctx.punishmessage.guild.id)

    @commands.command()
    async def addtwitch(self, ctx, streamer, notifyrole: discord.Role):
        connect = self.bot.get_cog("Setup")
        permission = self.bot.get_cog("Setup")
        perms = permission.getpermission(ctx)
        print("got perms")
        permcount=0
        for perm in perms:
            print("checking perm")
            if (perm[2] == 'twitch.add'):
                print(f"adding {streamer}")
                guild = ctx.guild
                print(guild)
                role = notifyrole.name
                print(role)
                connect = self.bot.get_cog("Setup")
                conn = connect.connectdb()
                c = conn.cursor()
                print("Connected and cursored")
                command5 = f"INSERT INTO streams(twitchname, guild_id,notifyrole) VALUES ('{streamer}',{guild.id}, '{role}')"
                print(command5)
                c.execute(command5)
                print("executed")
                conn.commit()
                c.close()
                conn.close()
                message=f"Added **{streamer}** to Auto Notify. Using <@&{notifyrole.id}> as the notify role"
                print("message var set")
                await ctx.send(message)
                print("message sent")
            else:
                print("perm is wrong")
                permcount = permcount+1
    
        if permcount == len(perms):
            await ctx.send("You lack permission to add twitch channels")
            log = self.bot.get_cog("Logger")
            log.logger(command=f"Tried to add {streamer} to Auto Notify but lacks permission", user=ctx.author, channel=ctx.channel, color="#f00000", guild=ctx.punishmessage.guild.id)


    @commands.command()
    async def deltwitch(self, ctx, streamer):
        connect = self.bot.get_cog("Setup")
        permission = self.bot.get_cog("Setup")
        permissions = permission.getpermission(ctx)
        permcount=0
        for perm in permissions:
            if (perm[2] == 'twitch.delete'):
                print(f"removing {streamer}")
                guild = ctx.guild.id
                print(guild)
                connect = self.bot.get_cog("Setup")
                conn = connect.connectdb()
                c = conn.cursor()
                print("Connected and cursored")
                command = f"select guild_id from streams where guild_id={guild} and twitchname='{streamer}'"
                c.execute(command)
                print("executed")
                results = c.fetchall()
                if len(results)!=0:
                    print(results)
                    command5 = f"delete from streams where twitchname = '{streamer}' and guild_id = {guild}"
                    print(command5)
                    c.execute(command5)
                    print("executed")
                    conn.commit()
                    c.close()
                    conn.close()
                    message=f"Removed **{streamer}** from Auto Notify"
                    print("message var set")
                    await ctx.send(message)
                    print("message sent")
                else:
                    await ctx.send(f"Could not find **{streamer}** in Auto Notify for this server, please try again")
            else:
                permcount = permcount+1
        if permcount == len(permissions):
            await ctx.send("You lack permission to remove twitch channels")
            log = self.bot.get_cog("Logger")
            log.logger(command=f"Tried to remove {streamer} from Auto Notify but lacks permission", user=ctx.author, channel=ctx.channel, color="#f00000", guild=ctx.punishmessage.guild.id)

def setup(bot):
    bot.add_cog(AutoTwitch(bot))
