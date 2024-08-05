import discord
from typing import Union
import os
import sys
import random
from discord import app_commands
from discord.ext import commands
import asyncio
from datetime import datetime
from pytz import timezone



MY_GUILD = discord.Object(id=1047320746453643344)
guild_id = 1047320746453643344
music_channel_id = 1053116705704001646
class colors:
  default = 0
  teal = 0x1abc9c
  dark_teal = 0x11806a
  green = 0x2ecc71
  dark_green = 0x1f8b4c
  blue = 0x3498db
  dark_blue = 0x206694
  purple = 0x9b59b6
  dark_purple = 0x71368a
  magenta = 0xe91e63
  dark_magenta = 0xad1457
  gold = 0xf1c40f
  dark_gold = 0xc27c0e
  orange = 0xe67e22
  dark_orange = 0xa84300
  red = 0xe74c3c
  dark_red = 0x992d22
  lighter_grey = 0x95a5a6
  dark_grey = 0x607d8b
  light_grey = 0x979c9f
  darker_grey = 0x546e7a
  blurple = 0x7289da
  greyple = 0x99aab5
brasil = timezone('Brazil/east')

sessões_marcadas = []

#Funções: ---------------------------------------------------------------------------------
#Funções: ---------------------------------------------------------------------------------
#Funções: ---------------------------------------------------------------------------------
async def get_server(client: discord.Client): #Retorna o objeto GUILD
    await client.wait_until_ready()
    server = client.get_guild(guild_id)
    return server

async def get_members(client: discord.Client): #Retorna membros do objeto GUILD
    await client.wait_until_ready()
    server = await get_server(client)
    if not server:
        return
    members = server.members
    return members

async def is_owner(interaction : discord.Interaction):#Retorna True se o interaction.user for dono do server
    if interaction.user.id == 286540943056830474:
        return True
    else:
        return False

async def is_mestre(interaction : discord.Interaction):#Retorna True se o interaction.user for mestre
    if (interaction.user.id == 286540943056830474) or (interaction.user.id == 252150507345281024) :
        return True
    else:
        return False

async def get_mestres(client):
    members = await get_members(client)
    mestres = []
    if members == None:
        print("Memebers deu None")
        return
    for member in members:
        if discord.utils.get(member.roles, name="Mestres"): 
            mestres.append(member)
    return mestres

async def owner(user):
    if user.id == 286540943056830474:
        return True
    else:
        return False
    
async def not_text_channel(channel):
    if not isinstance(channel, discord.abc.Messageable):
        return 1
    else:
        return 0
    #use: if not_text_channel(channel): return
    
async def not_voice_channel(channel):
    if not isinstance(channel, discord.VoiceChannel):
        return 1
    else:
        return 0
    #use: if not_voice_channel(channel) return

async def track_event(event):
    start_time = int(event.start_time.replace(tzinfo=None).timestamp())
    now = int(datetime.utcnow().replace(tzinfo=None).timestamp())
    delta_seconds = (start_time - now)
    if delta_seconds > 0:
        await asyncio.sleep(delta_seconds)
    try:
        await event.start()
        print(f"\n\nIniciando evento: {event}")
    except:
        print("\nTentou começar um evento e não funcionou, ou o evento não existe, ou já começou\n")

async def update_events(client):
    sessões_marcadas = await client.guilds[0].fetch_scheduled_events()
    sessões_marcadas.sort(key=lambda event: event.start_time)
    if len(sessões_marcadas) > 0:
        print('Eventos/sessões marcadas:\n')
        for event in sessões_marcadas:
            print(f"{event.name}, {event.start_time} (-3 horas)\n")
        for event in sessões_marcadas:
            await track_event(event)
    else:
        print('\nSem eventos/sessões no momento.')
    return sessões_marcadas

