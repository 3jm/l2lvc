import nextcord, orjson, aiodns, cchardet, os, requests, aiohttp, json, re, sys
from nextcord import Interaction, SlashOption
from nextcord.ext import commands
import urllib.request
import os
import time

intents = nextcord.Intents.all()


def get_prefix(bot, message):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    return prefixes[str(message.guild.id)]


bot = commands.Bot(command_prefix=get_prefix, intents=intents)
token = json.load(open('config.json'))['Token']


@bot.event
async def on_ready():
    print("bots is ready")

@bot.event
async def on_guild_join(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(guild.id)] = '*'

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f)

@bot.command()
async def set_prefix(ctx, prefix):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    
    prefixes[str(ctx.guild.id)] = prefix

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f)
    await ctx.send(f'Prefix set to `{prefix}`')

@bot.command()
async def quick_setup(ctx):
    await ctx.message.delete()
    start = int(time.time() * 1000)
    em = nextcord.Embed(
        title='Quick Setup Started',
        description=f'This will take a second..',
        color=0x2F3136
    )
    msg = await ctx.send(embed = em)
    category = await ctx.guild.create_category("Events")
    channel = await ctx.guild.create_voice_channel("Last To Leave", category=category)
    end = int(time.time() * 1000)
    duration = int(end - start)
    emb = nextcord.Embed(
        title='Quick Setup Finished',
        description=f'Completed in `{duration}ms`\nConnect: <#{channel.id}>',
        color=0x2F3136
    )
    await msg.edit(embed=emb)

@bot.command()
async def lockvc(ctx, id):
    await ctx.send('Locking VC..')
    vc = bot.get_channel(int(id))
    await vc.set_permissions(ctx.guild.default_role, connect=False)
    await ctx.send('Done')

@bot.command()
async def unlockvc(ctx, id):
    await ctx.send('Unlocking VC..')
    vc = bot.get_channel(int(id))
    await vc.set_permissions(ctx.guild.default_role, connect=True)
    await ctx.send('Done')

bot.run(token)