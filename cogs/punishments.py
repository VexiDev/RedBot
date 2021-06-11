import discord
from discord.abc import _Overwrites
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

class Punishments(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def history(self, ctx, target: discord.User):
        connect = self.bot.get_cog("Setup")
        dbresults = { "warn":[] , "mute":[] , "kick":[], "ban":[]}
        #make sure like they have the permission
        permission = self.bot.get_cog("Setup")
        permissions = permission.getpermission(ctx)
        permcount = 0
        for permission in permissions:
            if (permission[2] == 'punishments.history'):
                #-----------getting all punishss----------
                print("adding punishments")
                for types in dbresults:
                    conn = connect.connectdb()
                    print("connected")
                    c = conn.cursor()
                    print("cursored")
                    command= f"select * from punishments where type='{types}' and user_id='{target.id}'"
                    print(command)
                    c.execute(command)
                    print("executed")
                    dbresults[types] = c.fetchall()
                    conn.commit()
                    c.close()
                    conn.close()
                print("Gotten all punishments")
                #-----------doing the message-----------

                total_page = discord.Embed (
                    title = f'All punishments for {target.name}',
                    description = f'React to open up logs for each punishment\n\n**Total Warns:** {len(dbresults["warn"])}\n\n**Total Mutes:** {len(dbresults["mute"])}\n\n**Total Kicks:** {len(dbresults["kick"])}\n\n**Total Bans:** {len(dbresults["ban"])}\n',
                    colour = 0x00ff00
                )
                print("total page set")

            
                allpages = { "warn":[] , "mute":[] , "kick":[], "ban":[]}
                
                print("results going")

                for types in allpages:
                    print(types)
                    print(len(dbresults[types]))

                    if len(dbresults[types])==0:
                        page = discord.Embed (
                            title = f' {target.name} has no {types}s on record',
                            description = f'React with back to return to main page',
                            colour = 0x00ff00
                            )
                        allpages[types] += [page]
                    else:
                        for nb in range(math.ceil(len(dbresults[types])/5)):
                            page = discord.Embed (
                            title = f'All {types}s for {target.name}',
                            description = f'React with back to return to main page',
                            colour = 0x00ff00
                            )
                            print("set page")
                            start =5*nb
                            end = start+5
                            print("set start and end")
                            if end>len(dbresults[types]):
                                end = len(dbresults[types])
                                print("final end")

                            tempresults = dbresults[types][start:end]
                            print("set tempresults")

                            for results in tempresults:
                                print(f"results = {results}")
                                mod = await self.bot.fetch_user(results[2])
                                print(mod)
                                page.add_field(name=f"{types} issued by {mod} || Status: {results[5]}", value=f"reason: {results[4]}\nissued: {results[6]}", inline=False)

                            allpages[types] += [page]

                message = await ctx.send(embed = total_page)
                print("sent")

                await message.add_reaction('🇼')
                await message.add_reaction('🇲')
                await message.add_reaction('🇰')
                await message.add_reaction('🇧')
                

                def check(reaction, user):
                    return user == ctx.author

                i = 0
                reaction = None
                currentkey = None

                while True:
                    if str(reaction) == '🇼':
                        currentkey = "warn"
                        await message.edit(embed = allpages[currentkey][i])
                        await message.add_reaction('⬅️')
                        await message.add_reaction('▶')
                    elif str(reaction) == '🇰':
                        currentkey = "kick"
                        await message.edit(embed = allpages[currentkey][i])
                        await message.add_reaction('⬅️')
                        await message.add_reaction('▶')
                    elif str(reaction) == '🇧':
                        currentkey = "ban"
                        await message.edit(embed = allpages[currentkey][i])
                        await message.add_reaction('⬅️')
                        await message.add_reaction('▶')
                    elif str(reaction) == '🇲':
                        currentkey = "mute"
                        await message.edit(embed = allpages[currentkey][i])
                        await message.add_reaction('⬅️')
                        await message.add_reaction('▶')
                        
                    
                    elif str(reaction) == '⬅️':
                        await message.edit(embed = total_page)
                        await message.add_reaction('🇼')
                        await message.add_reaction('🇲')
                        await message.add_reaction('🇰')
                        await message.add_reaction('🇧')
                        i=0

                    elif str(reaction) == '◀':
                        i = i-1
                        print(i)
                        await message.edit(embed = allpages[currentkey][i])
                        print(allpages[currentkey][i])
                        if i == 0:
                            await message.add_reaction('⬅️')
                            await message.add_reaction('▶')
                        else:
                            await message.add_reaction('⬅️')
                            await message.add_reaction('◀')
                            await message.add_reaction('▶')
                    elif str(reaction) == '▶':
                        print(len(allpages[currentkey]))
                        i = i+1
                        print(i)
                        await message.edit(embed = allpages[currentkey][i])
                        print(allpages[currentkey][i])
                        if i == len(allpages[currentkey])-1:
                            await message.add_reaction('⬅️')
                            await message.add_reaction('◀')
                        else:
                            await message.add_reaction('⬅️')
                            await message.add_reaction('◀')
                            await message.add_reaction('▶')

                    try:
                        reaction, user = await self.bot.wait_for('reaction_add', timeout = 120.0, check = check)
                        await message.remove_reaction(reaction, user)
                    except:
                        break
                    await message.clear_reactions()
            else:
                permcount = permcount+1
        if permcount == len(permissions):
            await ctx.send("You lack permission to see punishment history")
            log = self.bot.get_cog("Logger")
            log.logger(command=f"Tried to see punishment history of {target} but lacks permission", user=ctx.author, channel=ctx.channel, color="#f00000", guild=ctx.punishmessage.guild.id)

        



    @commands.command()
    async def warn(self, ctx, target: discord.User,*, reason: str):
        user = target
        connect = self.bot.get_cog("Setup")
        #make sure like they have the permission
        permission = self.bot.get_cog("Setup")
        permissions = permission.getpermission(ctx)
        permcount = 0
        for permission in permissions:
            if (permission[2] == 'punishments.warn'):
                #-----------get total warns----------
                print("adding warn")
                conn = connect.connectdb()
                print("connected")
                command = "insert into "
                c = conn.cursor()
                print("cursored")
                command= "select * from punishments where type='warn'"
                print(command)
                c.execute(command)
                print("executed")
                results = c.fetchall()
                print(results)
                conn.commit()
                c.close()
                conn.close()
                #-----------auto-mod shit here----------
                #-----------add warn if no auto-mod shit-------
                #ADD IF NO AUTO MOD HERE
                conn = connect.connectdb()
                c = conn.cursor()
                print("connected")
                command = f"""INSERT INTO punishments(user_id, mod_id, "type","reason", "status", "time_issued", guild_id) VALUES ({target.id},{ctx.author.id},'warn', '{reason}','active', '{datetime.datetime.now().strftime("%m-%d-%Y at %H:%M")}', {ctx.guild.id});"""
                print(command)
                c.execute(command)
                print("executed")
                conn.commit()
                c.close()
                conn.close()
                warnmessage = discord.Embed(title=f"User {target.name} has been warned", color=0xf54242)
                warnmessage.add_field(name=f"Reason: {reason}", value=f"id: {target.id}", inline=False)
                warndm = f"""You've been warned in {ctx.guild.name} for "{reason}" || Please be careful too many warns may result in further punishment."""
                await target.send(warndm)
                await ctx.send(embed=warnmessage)
                log = self.bot.get_cog("Logger")
                await log.logger(command=f"Warned {user} for *{reason}*", user=ctx.author, channel=ctx.channel, color="#f54242", guild=ctx.guild.id)
            else:
                permcount = permcount+1
        if permcount == len(permissions):
            await ctx.send("You lack permission to warn users")
            log = self.bot.get_cog("Logger")
            await log.logger(command=f"Tried to warn {target} for {reason} but lacks permission", user=ctx.author, channel=ctx.channel, color="#f00000", guild=ctx.guild.id)

        
    @commands.command()
    async def ban(self, ctx, user: discord.Member, *, reason="No reason provided"):
        target = user
        connect = self.bot.get_cog("Setup")
        #make sure like they have the permission
        permission = self.bot.get_cog("Setup")
        log = self.bot.get_cog("Setup")
        permissions = permission.getpermission(ctx)
        permcount = 0
        for permission in permissions:
            if permissions[2] != 'punishments.ban.bypass':
                if (permission[2] == 'punishments.ban'):
                    print("adding ban")
                    conn = connect.connectdb()
                    print("connected")
                    command = "insert into "
                    c = conn.cursor()
                    print("cursored")
                    command= "select * from punishments where type='ban'"
                    print(command)
                    c.execute(command)
                    print("executed")
                    results = c.fetchall()
                    print(results)
                    conn.commit()
                    c.close()
                    conn.close()
                    #-----------auto-mod shit here----------
                    #-----------add warn if no auto-mod shit-------
                    #ADD IF NO AUTO MOD HERE
                    conn = connect.connectdb()
                    c = conn.cursor()
                    print("connected")
                    command = f"""INSERT INTO punishments(user_id, mod_id, "type","reason", "status", "time_issued", guild_id) VALUES ({target.id},{ctx.author.id},'ban', '{reason}','active', '{datetime.datetime.now().strftime("%m-%d-%Y at %H:%M")}', {ctx.guild.id});"""
                    print(command)
                    c.execute(command)
                    print("executed")
                    conn.commit()
                    c.close()
                    conn.close()
                    await user.ban(reason=reason)
                    ban = discord.Embed(title=f" Banned {user.name}!", description=f"Reason: {reason}\nBy: {ctx.author.mention}", color=0xff0000)
                    await ctx.channel.send(embed=ban)
                    await log.logger(command=f"Banned {user} for *{reason}*", user=ctx.author, channel=ctx.channel, color="#ff0000", guild=ctx.guild.id)
                else:
                    permcount = permcount+1
            else:
                await ctx.send("This user is immune to my bans")
                return
        if permcount == len(permissions):
            await ctx.send("You lack permission to ban users")
            log = self.bot.get_cog("Logger")
            await log.logger(command=f"Tried to ban {target} for {reason} but lacks permission", user=ctx.author, channel=ctx.channel, color="#ff0000", guild=ctx.guild.id)

    @commands.command()
    async def kick(self, ctx, user: discord.Member, *, reason="No reason provided"):
        target = user
        connect = self.bot.get_cog("Setup")
        #make sure like they have the permission
        permission = self.bot.get_cog("Setup")
        log = self.bot.get_cog("Setup")
        permissions = permission.getpermission(ctx)
        permcount = 0
        for permission in permissions:
            if permission[2] != 'punishments.kick.bypass':
                if (permission[2] == 'punishments.kick'):
                    print("adding kick")
                    conn = connect.connectdb()
                    print("connected")
                    c = conn.cursor()
                    print("cursored")
                    command= "select * from punishments where type='kick'"
                    print(command)
                    c.execute(command)
                    print("executed")
                    results = c.fetchall()
                    print(results)
                    conn.commit()
                    c.close()
                    conn.close()
                    #-----------auto-mod shit here----------
                    #-----------add warn if no auto-mod shit-------
                    #ADD IF NO AUTO MOD HERE
                    conn = connect.connectdb()
                    c = conn.cursor()
                    print("connected")
                    command = f"""INSERT INTO punishments(user_id, mod_id, "type","reason", "status", "time_issued", guild_id) VALUES ({target.id},{ctx.author.id},'kick', '{reason}','active', '{datetime.datetime.now().strftime("%m-%d-%Y at %H:%M")}', {ctx.guild.id});"""
                    print(command)
                    c.execute(command)
                    print("executed")
                    conn.commit()
                    c.close()
                    conn.close()
                    await user.kick(reason=reason)
                    kick = discord.Embed(title=f"Kicked {user.name}!", description=f"Reason: {reason}\nBy: {ctx.author.mention}", color=0xff0000)
                    await ctx.channel.send(embed=kick)
                    await log.logger(command=f"Kicked {user} for *{reason}*", user=ctx.author, channel=ctx.channel, color="#ff0000", guild=ctx.guild.id)
                else:
                    permcount = permcount+1
            else:
                await ctx.send("This user is immune to my kicks")
                return
        if permcount == len(permissions):
            await ctx.send("You lack permission to kick users")
            log = self.bot.get_cog("Logger")
            await log.logger(command=f"Tried to kick {target} for {reason} but lacks permission", user=ctx.author, channel=ctx.channel, color="#ff0000", guild=ctx.guild.id)


    @commands.command()
    async def mute(self, ctx, user: discord.Member, reason="No reason provided"):
        target = user
        connect = self.bot.get_cog("Setup")
        #make sure like they have the permission
        permission = self.bot.get_cog("Setup")
        log = self.bot.get_cog("Setup")
        permissions = permission.getpermission(ctx)
        permcount = 0
        for permission in permissions:
            if (permission[2] != 'punishments.mute.bypass'):
                if (permission[2] == 'punishments.mute'):
                    print("adding mute")
                    conn = connect.connectdb()
                    print("connected")
                    command = "insert into "
                    c = conn.cursor()
                    print("cursored")
                    command= "select * from punishments where type='mute'"
                    print(command)
                    c.execute(command)
                    print("executed")
                    results = c.fetchall()
                    print(results)
                    conn.commit()
                    c.close()
                    conn.close()
                    #-----------auto-mod shit here----------
                    #-----------add warn if no auto-mod shit-------
                    #ADD IF NO AUTO MOD HERE
                    conn = connect.connectdb()
                    c = conn.cursor()
                    print("connected")
                    command = f"""INSERT INTO punishments(user_id, mod_id, "type","reason", "status", "time_issued", guild_id) VALUES ({target.id},{ctx.author.id},'mute', '{reason}','active', '{datetime.datetime.now().strftime("%m-%d-%Y at %H:%M")}', {ctx.guild.id});"""
                    print(command)
                    c.execute(command)
                    print("executed")
                    conn.commit()
                    c.close()
                    conn.close()
                    role = discord.utils.get(ctx.guild.roles, name="Muted")
                    print(role.name)
                    await target.add_roles(role, reason=f"{reason}")
                    mute = discord.Embed(title=f"Muted {user.name}!", description=f"Reason: {reason}\nBy: {ctx.author.mention}", color=0xf56969)
                    await ctx.channel.send(embed=mute)
                    await log.logger(command=f"Muted {user} for *{reason}*", user=ctx.author, channel=ctx.channel, color="#f56969", guild=ctx.guild.id)
                else:
                    permcount = permcount+1
            else:
                await ctx.send("This user is immune to mutes")
                return
        if permcount == len(permissions):
            await ctx.send("You lack permission to mute users")
            log = self.bot.get_cog("Logger")
            await log.logger(command=f"Tried to mute {target} for {reason} but lacks permission", user=ctx.author, channel=ctx.channel, color="#f56969", guild=ctx.guild.id)

    @commands.command()
    async def unmute(self, ctx, user: discord.Member):
        target = user
        connect = self.bot.get_cog("Setup")
        #make sure like they have the permission
        permission = self.bot.get_cog("Setup")
        log = self.bot.get_cog("Setup")
        permissions = permission.getpermission(ctx)
        permcount = 0
        for permission in permissions:
            if (permission[2] == 'punishments.unmute'):
                print("adding mute")
                conn = connect.connectdb()
                print("connected")
                command = "insert into "
                c = conn.cursor()
                print("cursored")
                command= "select * from punishments where type='mute'"
                print(command)
                c.execute(command)
                print("executed")
                results = c.fetchall()
                print(results)
                conn.commit()
                c.close()
                conn.close()
                #-----------auto-mod shit here----------
                #-----------add warn if no auto-mod shit-------
                #ADD IF NO AUTO MOD HERE
                conn = connect.connectdb()
                c = conn.cursor()
                print("connected")
                command = f"UPDATE punishments SET status = 'revoked' WHERE status='active' and guild_id = {ctx.guild.id} and user_id = {target.id}"
                print(command)
                c.execute(command)
                print("executed")
                conn.commit()
                c.close()
                conn.close()
                role = discord.utils.get(ctx.guild.roles, name="Muted")
                print(role.name)
                await target.remove_roles(role)
                await ctx.send(f"Unmuted {target}")
                await log.logger(command=f"UnMuted {target}", user=ctx.author, channel=ctx.channel, color="#f56969", guild=ctx.guild.id)
            else:
                permcount = permcount+1
        if permcount == len(permissions):
            await ctx.send("You lack permission to mute users")
            log = self.bot.get_cog("Logger")
            await log.logger(command=f"Tried to unmute {target} but lacks permission", user=ctx.author, channel=ctx.channel, color="#f56969", guild=ctx.guild.id)

    @commands.command()
    async def mutesetup(self, ctx):
        print("mutesetup running")
        permission = self.bot.get_cog("Setup")
        permissions = permission.getpermission(ctx)
        permcount = 0
        for permission in permissions:
            if permission[2] == 'punishments.mutesetup':
                print(ctx.guild.roles)
                if ('Muted' not in str(ctx.guild.roles)): 
                    print(f"setting up muted role for {ctx.guild.name}")
                    muterole = await ctx.guild.create_role(name='Muted', color=0x616161, reason='Muterole setup')
                    for channel in ctx.guild.channels:
                        print(channel)
                        await channel.set_permissions(muterole, send_messages=False)
                        await channel.set_permissions(ctx.guild.default_role, overwrite=None)
                    await ctx.send("Muted role has been created and setup, use !mute to mute users")
                    return
                else:
                    await ctx.send("This server already has the Muted role please delete it and run again")
                    return
            else:
                permcount = permcount+1
        if permcount == len(permissions):
            await ctx.send("You lack permission to setup the mute system")
            log = self.bot.get_cog("Logger")
            await log.logger(command=f"Tried to run **mutesetup** but lacks permission", user=ctx.author, channel=ctx.channel, color="#f56969", guild=ctx.guild.id)




    # #-----------------------------------------------------------------------
    # @commands.command()
    # @commands.has_permissions(manage_messages=True)False
    # async def unmute(self, ctx, user: discord.Member):
    #     role_name = 'Text Mute'
    #     guild = self.bot.get_guild(530284930119499776)
    #     role = discord.utils.get(guild.roles, name=role_name)
    #     await user.remove_roles(role)
    #     await ctx.send(f"User {user} can type again!")
    #     await logger(command=f"Unmuted {user} in all text channels", user=ctx.author, channel=ctx.channel, color="#00ff08", guild=ctx.punishmessage.guild.id)

def setup(bot):
    bot.add_cog(Punishments(bot))