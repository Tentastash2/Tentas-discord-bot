import discord
from discord import FFmpegPCMAudio
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions
from discord import member
from discord_slash import SlashCommand
import requests
import json
import os

from apikeys import *

intents = discord.Intents.all ()
intents.members = True

queues = {}

def check_queue(ctx, id):
    if queues[id] != []:
        voice = ctx.guild.voice_client
        source = queues[id].pop(0)
        player = voice.play(source)

client = commands.Bot(command_prefix='_')
slash = SlashCommand(client, sync_commands=True)


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------------------')


@client.command()
async def hello(ctx):
    await ctx.send('Hello!')


@client.event
async def on_member_join(member):
    with open('my_image.png', 'rb') as f:
        picture = discord.File(f)
        channel = client.get_channel(920870360012968036)
        await channel.send(f'Hello {member}! Its not safe to go alone! Here take this!', file=picture)


@client.command()
async def goodbye(ctx):
    await ctx.send('Bye! Have a good one!')


@client.command()
async def selfdestruct(ctx):
    with open('explosion-boom.gif', 'rb') as f:
        gif = discord.File(f)
    await ctx.send('We going boom!!!', file=gif)


@client.command(pass_context=True)
async def join(ctx):
    if (ctx.author.voice):
        channel = ctx.message.author.voice.channel
        voice = await channel.connect()
        source = FFmpegPCMAudio('Turret_turret_autosearch_4.wav')
        await ctx.send('I have arrived!')
        player = voice.play(source)
    else:
        await ctx.send('Sorry but your not in a voice channel')


@client.command(pass_context=True)
async def leave(ctx):
    if (ctx.voice_client):
        await ctx.guild.voice_client.disconnect()
        await ctx.send('I have left the VC.')
    else:
        await ctx.send('I am not in a VC right now.')


@client.command(pass_context=True)
async def neko(ctx):
    if (ctx.author.voice):
        channel = ctx.message.author.voice.channel
        voice = await channel.connect()
        source = FFmpegPCMAudio('No_kitty.wav')
        await ctx.send('I have arrived!')
        player = voice.play(source)
    else:
        await ctx.send('Sorry but your not in a voice channel')


@client.command(pass_context=True)
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause
    else:
        await ctx.send('There is nothing playing.')


@client.command(pass_context=True)
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send('At the moment there is no audio paused')


@client.command(pass_context=True)
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice.stop()


@client.command(pass_context=True)
async def play(ctx, arg):
    voice = ctx.guil.voice_client
    song = arg + '.wav'
    source = FFmpegPCMAudio(song)
    player = voice.play(source, after=lambda x=None: check_queue(ctx, ctx.message.guild.id))


@client.command(pass_context=True)
async def queue(ctx, arg):
    voice = ctx.guil.voice_client
    song = arg + '.wav'
    source = FFmpegPCMAudio(song)

    guild_id = ctx.message.guild.id

    if guild_id in queues:
        queues[guild_id].append(source)

    else:
        queues[guild_id] = [source]

    await ctx.send('Added to queue')

@client.event
async def on_message(message):

    if message.content == [""]:
        await message.delete()
        await message.channel.send("Don't send that again or there will be actions taken.")


@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member : discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'User {member} has been kicked.')

@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send('You do not have permission to kick people.')


@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member : discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'User {member} has been banned.')

@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send('You do not have permission to ban people.')


@slash.slash(description='says hello to the users')
async def hello(ctx):
    await ctx.send('Hello!')


@slash.slash(description='bot will detonate')
async def selfdestruct(ctx):
    with open('explosion-boom.gif', 'rb') as f:
        gif = discord.File(f)
    await ctx.send('We going boom!!!', file=gif)


@slash.slash(description='Says goodbye to the users')
async def goodbye(ctx):
    await ctx.send('Bye! Have a good one!')


@slash.slash(description='Bot will join the VC.')
async def join(ctx):
    if (ctx.author.voice):
        channel = ctx.author.voice.channel
        voice = await channel.connect()
        source = FFmpegPCMAudio('Turret_turret_autosearch_4.wav')
        await ctx.send('I have arrived!')
        player = voice.play(source)
    else:
        await ctx.send('Sorry but your not in a voice channel')


@slash.slash(description='Bot will leave the VC')
async def leave(ctx):
    if (ctx.voice_client):
        await ctx.guild.voice_client.disconnect()
        await ctx.send('I have left the VC.')
    else:
        await ctx.send('I am not in a VC right now.')


@slash.slash(description='Plays a neko sound')
async def neko(ctx):
    if (ctx.author.voice):
        channel = ctx.author.voice.channel
        voice = await channel.connect()
        source = FFmpegPCMAudio('No_kitty.wav')
        await ctx.send('I have arrived!')
        player = voice.play(source)
    else:
        await ctx.send('Sorry but your not in a voice channel')


client.run(BOTTOKEN)
