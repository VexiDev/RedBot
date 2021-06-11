import discord
from discord.ext import commands
import discord.utils
from  builtins import any
from discord import Intents
import requests
import os
import json
import random
import asyncio
import datetime
import psycopg2
import ast
import unicodedata
import codecs
import re

class ReactionRoles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

#----------------primary command------------



    @commands.command()
    async def rr(self, ctx, method=None):
        if method == 'create':
            await self.rr_create(ctx)

        elif method == "delete":
            await self.rr_delete(ctx)

        elif method == None:
            await ctx.send("Please enter a method (methods: create/delete")
        else:
            await ctx.send(f"{method} is not a valid method (methods: create/delete")



#--------------command functions---------------------



    async def rr_create(self, ctx):
        def check(msg):
            return msg.author.id == ctx.author.id
        await ctx.send("Please select what type of reaction role you would like to create (types: multi/unique)")
        rr_type_select = await self.bot.wait_for("message", check=check)
        if rr_type_select.content == 'multi':
            await ctx.send("Welcome to the reaction role creator! (cancel any time by just replying **cancel**)\n- - - - - - - - - - - - - -")
            title = await self.settitle(ctx)
            await asyncio.sleep(0.5)
            all_roles = await self.setroles(ctx)
            emote_list = await self.setemotes(ctx)
            await asyncio.sleep(0.5)
            color = await self.setcolor(ctx)
            await asyncio.sleep(0.5)
            final_desc = self.combine_lists(emote_list, all_roles)
            rr_embed = await self.printmenu(ctx, title, final_desc, color)
            await asyncio.sleep(0.5)
            await self.checkmenu(ctx, title, emote_list, all_roles, color,rr_embed)
        elif rr_type_select.content == 'unique':
            await ctx.send("unique reaction roles are not currently available")
        else:
            await ctx.send(f"**{rr_type_select.content}** is not a valid menu type")


    async def rr_delete(self, ctx):
        connect = self.bot.get_cog("Setup")
        found_menu = False
        print("going")
        def check(msg):
            return msg.author.id == ctx.author.id
        conn = connect.connectdb()
        print("connected")
        c = conn.cursor()
        print("cursored")
        command= f"select * from reaction_roles where guild_id={ctx.guild.id}"
        print(command)
        c.execute(command)
        print("executed")
        all_menus = c.fetchall()
        print(str(len(all_menus)))
        # print(all_menus)
        conn.commit()
        c.close()
        conn.close()
        final_menu = ""
        if len(all_menus) != 0:
            for menus in all_menus:
                print(menus[5])
                final_menu = final_menu+" "+str(menus[5])+"\n"
            await ctx.send("Please select, by name, which menu you would like to delete")
            # await asyncio.sleep(2)
            all_menu_embed = discord.Embed(title="All role menus for this server", description=f"{final_menu}", color=0x14ffd0)
            await ctx.send(embed=all_menu_embed)
            menu_select_response = await self.bot.wait_for('message', check = check)
            for menu in all_menus:
                print(str(menu[5]))
                print(str(menu_select_response.content))
                if str(menu_select_response.content) == str(menu[5]):
                    print("is the menu")
                    conn = connect.connectdb()
                    print("connected")
                    c = conn.cursor()
                    print("cursored")
                    command= f"select * from reaction_roles where guild_id={ctx.guild.id} and title='{menu_select_response.content}'"
                    print(command)
                    c.execute(command)
                    print("executed")
                    rr_info = c.fetchall()
                    print(rr_info)
                    print(str(len(all_menus)))
                    # print(all_menus)
                    conn.commit()
                    c.close()
                    conn.close()
                    title = rr_info[0][5]
                    print(title)
                    all_emotes = ast.literal_eval(rr_info[0][7])
                    print(all_emotes)
                    all_roles = ast.literal_eval(rr_info[0][4])
                    print(all_roles)
                    final_all_roles = []
                    for roles in all_roles:
                        print(f"getting {roles} from discord.utils")
                        role = discord.utils.get(ctx.guild.roles, id=int(roles))
                        print(role.name)
                        final_placeholder_role = "<@&"+str(role.id)+">"
                        final_all_roles.append(final_placeholder_role)
                    print(final_all_roles)
                    final_desc = self.combine_lists(all_emotes, final_all_roles)
                    print(final_desc)
                    print(rr_info[0][7])
                    rr_embed = discord.Embed(title=f"{title}", description=f"{final_desc}", color=int(rr_info[0][6]))
                    print("set embed")
                    await ctx.send(embed=rr_embed)
                    await ctx.send("Please confirm this is the menu you wish to delete? (yes/no)")
                    confirm_menu_select = await self.bot.wait_for('message', check = check)
                    if confirm_menu_select.content == 'yes':
                        for channels in ctx.guild.channels:
                            try:
                                print(f"looking for message in {channels.name}")
                                message = await channels.fetch_message(rr_info[0][1])
                                print("got message")
                                conn = connect.connectdb()
                                print("connected")
                                c = conn.cursor()
                                print("cursored")
                                print(ctx.guild.id)
                                print(title)
                                command= f"delete from reaction_roles where guild_id = {ctx.guild.id} and title='{title}'"
                                print(command)
                                c.execute(command)
                                print("executed")
                                conn.commit()
                                c.close()
                                conn.close()
                                await message.delete()
                                print("Deleted")
                                print(f"Menu {title} deleted")
                                await ctx.send(f"Menu **{title}** has been deleted")
                            except:
                                print("Error: An error has occured")
                                pass 
                    elif confirm_menu_select.content == 'no':
                        await ctx.send("Alright delete canceled")
                    found_menu = True
                else:
                    print("not the menu")
            if found_menu == True:
                pass
            elif found_menu == False:
                print("no matching menu found, input invalid")
                await ctx.send("Not a valid menu name, try again")
        elif len(all_menus) == 0:
            await ctx.send("This server has no reaction roles")
        else:
            print("Error: all_menus is not a number")
            await ctx.send("Error: if this persists please contact vexi#0420")
        



#---------------NON COMMAND FUNCTIONS-----------------




    async def checkmenu(self, ctx, title, emote_list, all_roles, color, rr_embed):
        connect = self.bot.get_cog("Setup")
        def check(msg):
            return msg.author.id == ctx.author.id
        await ctx.send("Is this correct? (yes/no)")
        confirm_response = await self.bot.wait_for('message', check = check)
        if "yes" in confirm_response.content:
            await ctx.send("Alright please select a channel (type here in that channel)")
            channel_select = await self.bot.wait_for('message', check = check)
            if "here" in channel_select.content:
                await channel_select.delete()
                rr_channel = self.bot.get_channel(channel_select.channel.id)
                await ctx.send(f"Alright the reaction role menu will go to **{channel_select.channel.name}**")
            else:
                await ctx.send("invalid response, final try")
                await ctx.send("Please select a channel (type **here** in that channel)")
                channel_select = await self.bot.wait_for('message', check = check)
                if "here" in channel_select.content:
                    await channel_select.delete()
                    rr_channel = self.bot.get_channel(channel_select.channel.id)
                    await ctx.send(f"Alright the reaction role menu will go to **{channel_select.channel.name}**")
                else:
                    await ctx.send("invalid response, menu create canceled")
            await asyncio.sleep(3)
            message = await rr_channel.send(embed=rr_embed)
            print(emote_list)
            data_emotes = []
            for emote in emote_list:
                emote = str(emote).replace(" ", "")
                await message.add_reaction(f'{emote}')
                data_emotes.append(emote)
            conn = connect.connectdb()
            print("connected")
            c = conn.cursor()
            print("cursored")
            print(data_emotes)
            data_emotes = str(data_emotes)
            data_emotes = data_emotes.replace("'", "''")
            print(f"data emotes final == {data_emotes}")
            all_roles = str(all_roles).replace("'", "''")
            all_roles = str(all_roles).replace("<@&", "")
            all_roles = str(all_roles).replace(">", "")
            command= f"INSERT INTO reaction_roles(message_id, guild_id, channel_id, roles, title, color, emotes) VALUES ({message.id},{ctx.guild.id}, {rr_channel.id}, '{all_roles}', '{title}', '{color}', '{data_emotes}')"
            print(command)
            c.execute(command)
            conn.commit()
            c.close()
            conn.close()
            await ctx.send("Menu completed and activated")
        
        elif "no" in confirm_response.content:
            await ctx.send("Oops! Which value is wrong? (title, roles, emotes, color)")
            mistake_select = await self.bot.wait_for('message', check = check)
            if mistake_select != 'cancel':
                if "title" in mistake_select.content:
                    await ctx.send("Alright lets try setting the title again")
                    title = await self.settitle(ctx)
                elif "roles" in mistake_select.content:
                    await ctx.send("Alright lets try setting the roles again")
                    all_roles = await self.setroles(ctx)
                elif "emotes" in mistake_select.content:
                    await ctx.send("Alright lets try setting the emotes again")
                    emote_list = await self.setemotes(ctx)
                elif "color" in mistake_select.content:
                    await ctx.send("Alright lets try setting the color again")
                    color = await self.setcolor(ctx)
                final_desc = self.combine_lists(emote_list, all_roles)
                await self.printmenu(ctx, title, final_desc, color)
                print(str(color))
                await self.checkmenu(ctx, title, emote_list, all_roles, color, rr_embed)
            else:
                await ctx.send("Canceled")
        else:
            await ctx.send("Not a valid answer")
            
    def combine_lists(self, emote_list, all_roles):
        desc = [i + " " + j for i, j in zip(emote_list, all_roles)]
        print(desc)
        final_desc = ""
        for i in range(len(desc)):
            final_desc = final_desc + str(desc[i])+"\n"
        return final_desc


    async def settitle(self, ctx):
        def check(msg):
            return msg.author.id == ctx.author.id
        await ctx.send("Give a title to your reaction role menu (e.g. Colors, Age, etc.)")
        title_response = await self.bot.wait_for('message', check = check)
        if title_response.content != 'cancel':
            title = title_response.content
            await ctx.send(f"Alright your title is now **{title}**\n- - - - - - - - - - - - - -")
            return title
        else:
            await ctx.send("Canceled")

    async def setroles(self, ctx):
        rr_roles = []
        rr_role_names = []
        def check(msg):
            return msg.author.id == ctx.author.id  
        await ctx.send("What roles would you like to use? (Please @ them and seperate them with a comma)")
        role_response = await self.bot.wait_for('message', check = check)
        if role_response != 'cancel':
            all_roles = role_response.content.split(",")
            print(all_roles)
            for roles in all_roles:
                print(roles)
                roles = str(roles).replace("<@&", "")
                roles = str(roles).replace(">", "")
                rr_roles.append(roles)
                print(rr_roles)
            for ids in rr_roles:
                role = discord.utils.get(ctx.guild.roles, id=int(ids))
                rr_role_names.append(role.name)
            rr_roles_str = str(rr_role_names)
            rr_roles_str = rr_roles_str.replace("'", "")
            rr_roles_str = rr_roles_str.replace("[", "")
            rr_roles_str = rr_roles_str.replace("]", "")
            await ctx.send(f"Alright your roles are **{rr_roles_str}**\n- - - - - - - - - - - - - -")
            return all_roles
        else:
            await ctx.send("Canceled")

    async def setemotes(self, ctx):
        emote_list = []
        def check(msg):
            return msg.author.id == ctx.author.id
        await ctx.send("What emotes would you like to use for each roles? (Please seperate them with a comma)")
        emote_response = await self.bot.wait_for('message', check = check)
        if emote_response.content != 'cancel':
            all_emotes = emote_response.content.split(",")
            print(all_emotes)
            for emotes in all_emotes:
                emote_list.append(emotes)
            print(emote_list)
            emote_list_str = str(emote_list).replace("'", "")
            emote_list_str = emote_list_str.replace("[", "")
            emote_list_str = emote_list_str.replace("]", "")
            print(emote_list_str)
            await ctx.send(f"Alright your emotes are **{emote_list_str}**\n- - - - - - - - - - - - - -")
            return emote_list
        else:
            await ctx.send("Canceled")

    async def setcolor(self, ctx):
        def check(msg):
            return msg.author.id == ctx.author.id
        await ctx.send("What color would you like your menu to have? (please enter a hex value (e.g. #0f03fc)")
        color_response = await self.bot.wait_for('message', check = check)
        if color_response.content != 'cancel':
            sixteenIntegerHex = int(color_response.content.replace("#", ""), 16)
            readableHex = int(hex(sixteenIntegerHex), 0)
            print(f"readableHex = {readableHex}")
            await ctx.send(f"Alright your menu will have the color **{color_response.content}**\n- - - - - - - - - - - - - -")
            return readableHex
        else:
            await ctx.send("Canceled")

    async def printmenu(self, ctx, title, final_desc, readableHex):
        await ctx.send("Here is what your menu looks like")
        rr_embed = discord.Embed(title=f"{title}", description=f"{final_desc}", color=readableHex)
        print("set embed")
        await ctx.send(embed=rr_embed)
        return rr_embed




#---------------------EVENTS--------------------





    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.member.bot == False:
            connect = self.bot.get_cog("Setup")
            print(f"emoji = {payload.emoji.name}")
            conn = connect.connectdb()
            print("connected")
            c = conn.cursor()
            print("cursored")
            command= f"select * from reaction_roles where message_id = {payload.message_id} and guild_id = {payload.guild_id}"
            print(command)
            c.execute(command)
            results = c.fetchall()
            print(results)
            conn.commit()
            c.close()
            conn.close()
            if len(results) != 0:
                #convert emojis to a list
                print("convert to list")
                all_emojis = ast.literal_eval(results[0][7])
                print(all_emojis)
                all_roles = ast.literal_eval(results[0][4])
                print(all_roles)
                all_emojis_total = []
                all_roles_total = []
                for total in all_emojis:
                    final_total_emoji = str(total).replace(" ", "")
                    all_emojis_total.append(final_total_emoji)
                for total in all_roles:
                    final_total_roles = str(total).replace(" ", "")
                    all_roles_total.append(final_total_roles)

                print("final lists")

                print(all_emojis_total)
                print(all_roles_total)

                print("loop time")

                for i in range(len(all_emojis)):
                    print(payload.emoji.name)
                    print(all_emojis_total[i])
                    print(int(all_roles_total[i]))
                    if str(payload.emoji.name) == all_emojis_total[i]:
                        print("match")
                        guild_id = payload.guild_id
                        print("getting guild")
                        guild = discord.utils.find(lambda g : g.id == guild_id, self.bot.guilds)
                        print(guild.name)
                        print("getting role")
                        role = discord.utils.get(guild.roles, id=int(all_roles_total[i])) 
                        print(role.name)
                        print("getting member")
                        member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
                        print(member.name)
                        print('adding role')
                        await member.add_roles(role)
                        print("added role")
            else:
                print("no rr menu found")
        else:
            print("a bot")


    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        member = self.bot.get_user(payload.user_id)
        if member.bot == False:
            connect = self.bot.get_cog("Setup")
            print(f"emoji = {payload.emoji.name}")
            conn = connect.connectdb()
            print("connected")
            c = conn.cursor()
            print("cursored")
            command= f"select * from reaction_roles where message_id = {payload.message_id} and guild_id = {payload.guild_id}"
            print(command)
            c.execute(command)
            results = c.fetchall()
            print(results)
            conn.commit()
            c.close()
            conn.close()
            if len(results) != 0:
                #convert emojis to a list
                print("convert to list")
                all_emojis = ast.literal_eval(results[0][7])
                print(all_emojis)
                all_roles = ast.literal_eval(results[0][4])
                print(all_roles)
                all_emojis_total = []
                all_roles_total = []
                for total in all_emojis:
                    final_total_emoji = total.replace(" ", "")
                    all_emojis_total.append(final_total_emoji)
                for total in all_roles:
                    final_total_roles = total.replace(" ", "")
                    all_roles_total.append(final_total_roles)

                print("final lists")

                print(all_emojis_total)
                print(all_roles_total)

                print("loop time")

                for i in range(len(all_emojis)):
                    print(payload.emoji.name)
                    print(all_emojis_total[i])
                    print(int(all_roles_total[i]))
                    if str(payload.emoji.name) == all_emojis_total[i]:
                        print("match")
                        guild_id = payload.guild_id
                        print("getting guild")
                        guild = discord.utils.find(lambda g : g.id == guild_id, self.bot.guilds)
                        print(guild.name)
                        print("getting role")
                        role = discord.utils.get(guild.roles, id=int(all_roles_total[i])) 
                        print(role.name)
                        print("getting member")
                        member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
                        print(member.name)
                        print('removing role')
                        await member.remove_roles(role)
                        print("removed role")
            else:
                print("no rr menu found")
        else:
            print("a bot")

def setup(bot):
    bot.add_cog(ReactionRoles(bot))
