import discord
import os 
from discord import Intents
from discord import Streaming
from discord.utils import get
from discord.ext import commands

TOKEN = 'secwet'
intents = discord.Intents(messages=True, guilds=True, reactions=True, members=True)
bot = commands.Bot(command_prefix='!',intents=intents)
bot.remove_command('help')
bot.remove_command('kick')

@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name="twitch.tv/RedLumux"))
    print("Sucessfully connected to RedLumux!")

@bot.command()
async def test(ctx):
    await ctx.send('hello')


#---------------Text Mute/UnMute | VC Mute/Unmute------------------------
@bot.command()
@commands.has_permissions(manage_messages=True)
async def mute(ctx, user: discord.Member):
    role_name = 'Text Mute'
    guild = bot.get_guild(530284930119499776)
    role = discord.utils.get(guild.roles, name=role_name)
    await user.add_roles(role)
    await ctx.send(f"User {user} has been silenced!")
@mute.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You cant do that!")
#-----------------------------------------------------------------------
@bot.command()
@commands.has_permissions(manage_messages=True)
async def unmute(ctx, user: discord.Member):
    role_name = 'Text Mute'
    guild = bot.get_guild(530284930119499776)
    role = discord.utils.get(guild.roles, name=role_name)
    await user.remove_roles(role)
    await ctx.send(f"User {user} can type again!")
@unmute.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You cant do that!")
#-----------------------------------------------------------------------
@bot.command()
@commands.has_permissions(manage_messages=True)
async def vcmute(ctx, user: discord.Member):
    role_name = 'VC Mute'
    guild = bot.get_guild(530284930119499776)
    role = discord.utils.get(guild.roles, name=role_name)
    await user.add_roles(role)
    await ctx.send(f"User {user} can no longer speak!")
@vcmute.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You cant do that!")
#-----------------------------------------------------------------------
@bot.command()
@commands.has_permissions(manage_messages=True)
async def vcunmute(ctx, user: discord.Member):
    role_name = 'VC Mute'
    guild = bot.get_guild(530284930119499776)
    role = discord.utils.get(guild.roles, name=role_name)
    await user.remove_roles(role)
    await ctx.send(f"User {user} can speak again!")
@vcunmute.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You cant do that!")

#-----------------Kick/Ban-------------------------
@bot.command()
@commands.has_permissions(manage_messages=True)
async def kick(ctx, user: discord.Member, *, reason="No reason provided"):
        await user.kick(reason=reason)
        kick = discord.Embed(title=f" Kicked {user.name}!", description=f"Reason: {reason}\nBy: {ctx.author.mention}", color=0xff4a4a)
        await ctx.channel.send(embed=kick)
        await user.send(embed=kick)
@kick.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You cant do that!")
#-----------------------------------------------------------------------
@bot.command()
@commands.has_permissions(manage_messages=True)
async def ban(ctx, user: discord.Member, *, reason="No reason provided"):
        await user.ban(reason=reason)
        ban = discord.Embed(title=f" Banned {user.name}!", description=f"Reason: {reason}\nBy: {ctx.author.mention}", color=0xff0000)
        await ctx.channel.send(embed=ban)
        await user.send(embed=ban)
@ban.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You cant do that!")

#-----------------RulesMessage--------------------
@bot.command(pass_context=True)
@commands.has_permissions(manage_messages=True)
async def help(ctx):
#-------Staff---------
    embedVar1 = discord.Embed(title="RedLumux Bot Help Menu", description="Displays all available commands for the RedLumux Bot", color=0x00ff00)
    embedVar1.add_field(name="!help", value="displays this message", inline=False)
    embedVar1.add_field(name="!mute", value="usage: !mute <@user>\n Denys user the ability to talk in text channels", inline=False)
    embedVar1.add_field(name="!unmute", value="usage: !unmute <@user>\n Allows user to talk in text channels again", inline=False)
    embedVar1.add_field(name="!vcmute", value="usage: !vcmute <@user> \n Denys user from speak in VCs", inline=False)
    embedVar1.add_field(name="!vcunmute", value="usage: !vcunmute <@user> \n Allows user to speak in VCs", inline=False)
    embedVar1.add_field(name="!purge", value="usage: !purge <amount>\n Deletes <amount> of messages from channel", inline=False)
    embedVar1.add_field(name="!announceStream", value="usage: !announceStream <message>\n Sends a stream notification for RedLumux to #Announcements\n\n Developped by Vexi",inline=False)
    await ctx.send(embed=embedVar1)

@help.error
async def help_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        embedVar = discord.Embed(title="RedLumux Bot Help Menu", description="Displays all available commands for the RedLumux Bot", color=0x00ff00)
        embedVar.add_field(name="!help", value="displays this message", inline=False)
        embedVar.add_field(name="!f", value="pays respect \n\n Developped by Vexi", inline=True)
        await ctx.send(embed=embedVar)

#------------------ Stream Announce------------------------------
@bot.command(pass_context=True)
@commands.has_permissions(manage_messages=True)
async def announceStream(ctx, *,message="Im live right now, come watch!"):
    channel = bot.get_channel(817075705359630347)
    await channel.send(f"<@&818741406171791380>\n:red_circle:  **LIVE**  :red_circle: {message}\nhttps://twitch.tv/RedLumux")
    await bot.delete_message(ctx.message)

@announceStream.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You cant do that!")

#------------------Give viewer role on join---------------
@bot.event
async def on_member_join(member):
    autorole = discord.utils.get(member.guild.roles, name = 'Viewers')
    await member.add_roles(autorole)
    embedVar2 = discord.Embed(color=0x000000)
    embedVar2.set_thumbnail(url=member.avatar_url)
    embedVar2.add_field(name=f"{member.name}", value=f"**has joined the server!**")
    await bot.get_channel(594189196483362827).send(embed=embedVar2)

#-----------------Purge command-----------------
@bot.command(pass_context=True)
@commands.has_permissions(manage_messages=True)
async def purge(ctx, limit: int):
        await ctx.channel.purge(limit=limit+1)
        await ctx.message.delete()

@purge.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You cant do that!")
#-----------------VERFICATION ROLE----------------
@bot.event
async def on_raw_reaction_add(payload):
    message_id = payload.message_id
    if message_id == 816761584566665306:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g : g.id == guild_id, bot.guilds)
          
        role = discord.utils.get(guild.roles, name='Verified') 
        member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
        await member.add_roles(role)

    if message_id == 818746001778933800:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g : g.id == guild_id, bot.guilds)
          
        role = discord.utils.get(guild.roles, name='Stream Notify') 
        member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
        await member.add_roles(role)
@bot.event
async def on_raw_reaction_remove(payload):
    message_id = payload.message_id
    if message_id == 816761584566665306:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g : g.id == guild_id, bot.guilds)
          
        role = discord.utils.get(guild.roles, name='Verified') 
        member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
        await member.remove_roles(role)
    if message_id == 818746001778933800:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g : g.id == guild_id, bot.guilds)
          
        role = discord.utils.get(guild.roles, name='Stream Notify') 
        member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
        await member.remove_roles(role)
#--------------------   F   --------------------
@bot.command()
async def f(ctx):
    for i in range(5):
        await ctx.send("**F**")

#--------------------- SAY ----------------------
@bot.command()
async def send(ctx, title, desc, text):
    embedVar2 = discord.Embed(title=f"{title}", description=f"{desc}", color=0x30f8ff)
    embedVar2.add_field(name=f"------------------------------------------------------------------------------------------------\n{text}", value="**------------------------------------------------------------------------------------------------**", inline=False)
    await ctx.send(embed=embedVar2)
#---------------------TOKEN-----------------------
bot.run(TOKEN)
