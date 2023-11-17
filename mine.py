from http import client
from typing import Optional
import discord
from discord import app_commands
from discord.ext import commands
import asyncio
from datetime import datetime, timedelta
from pytz import timezone
import aiohttp
from utility import colors, brasil #type:ignore

#Funções: --------------------------------------------------------------------------------
#Funções: --------------------------------------------------------------------------------
#Funções: --------------------------------------------------------------------------------
async def update_mine_button(client):
    Status_Channel = await client.fetch_channel(1065781076909359104)
    if (not Status_Channel) or not (isinstance(Status_Channel, discord.abc.Messageable)) or isinstance(Status_Channel, discord.ForumChannel) or isinstance(Status_Channel, discord.CategoryChannel) or isinstance(Status_Channel, discord.abc.PrivateChannel):
        print("Status_Channel deu None")
        return
    async for message in Status_Channel.history(limit=None): #Restarta a mensagem do status do mine, caso o botão esteja congelado
        for component in message.components:
            if not isinstance(component, discord.Button):
                pass
            if isinstance(component, discord.ActionRow) and component.children[0].custom_id == "Abrir":
                await message.edit(view=MineView(client=client))
                break
            else:
                pass
        if message.content.find("Você poderá tentar abrir o server novamente")!= -1:
            await message.delete()
#Botões: --------------------------------------------------------------------------------
#Botões: --------------------------------------------------------------------------------
#Botões: --------------------------------------------------------------------------------
class MineView(discord.ui.View): # Server Mine
        """Botões para o /server"""
        def __init__(self,client)-> None:
            super().__init__(timeout = None)
            self.client = client
        
        @discord.ui.button(label="Abrir server",custom_id = "Abrir", style=discord.ButtonStyle.green) 
        async def button_callback1(self, interaction, button):
            channel = interaction.channel
            if not isinstance(channel, discord.abc.Messageable):
                print("Algum channel deu None")
                return
            url = ("https://www.triggercmd.com/trigger/bookmark?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJib29rbWFya3VzZXJfaWQiOiI2MThiZGQ4NjNhNmJhYjAwMWE4OTA3MjAiLCJjb21wdXRlcl9pZCI6IjY0N2Y5NmQzMDAyODljMDAxYjUwYjA3MCIsImNvbW1hbmRfaWQiOiI2NDdmOTZmMGJjN2Y3YjAwMWEyNjliMDYiLCJleHBpcmVzSW5TZWNvbmRzIjoiIiwiaWF0IjoxNjg2MDg2MTY3fQ.Uga-UD4AiG82BuYjsRnvNB1YqeP16sv9mZckG7bAHkw")
            async with aiohttp.ClientSession() as session:
                await session.get(url)
            embed = discord.Embed(title="Abrindo", description=f"Request enviado, se o trigger funcionar, em breve o server abrirá, e uma mensagem aparecerá no <#1070728402572685343>")
            await interaction.response.send_message(delete_after = 5, embed = embed)
            
            tempo = discord.utils.format_dt(datetime.now()+(timedelta(seconds=60)), style="R")
            button.disabled = True
            button.label = "Você poderá tentar novamente em 60 segundos"
            await interaction.message.edit(content = "", view = self)
            await channel.send(f"Você poderá tentar abrir o server novamente {tempo}", delete_after=61)
            await asyncio.sleep(61)
            button.disabled = False
            button.label = "Abrir Server"
            await interaction.message.edit(content = "", view = self)


        @discord.ui.button(label="Fechar server",custom_id = "Fechar", style=discord.ButtonStyle.red) 
        async def button_callback2(self, interaction, button):
            await interaction.response.send_message("Fechando o Server...", delete_after = 3)
            channel = interaction.client.get_channel(1065719690661478553)
            if not isinstance (channel, discord.abc.Messageable):
                return 
            await channel.send("stop")


#Classe:--------------------------------------------------------------------------------
#Classe:--------------------------------------------------------------------------------
#Classe:--------------------------------------------------------------------------------
class Mine(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    '''/mine'''
    @app_commands.command()
    async def mine(self, interaction : discord.Interaction):
        '''Comando para o server do Mine'''
        if not isinstance(interaction.channel, discord.abc.Messageable):
            return 
        embed: discord.Embed = discord.Embed(title="Abrir Server", description="Aperte o botão para abrir o server.(Ele fecha automaticamente por inatividade depois de 60 minutos)\n", color=colors().blurple)
        await interaction.response.send_message("Server message", delete_after=0.1)
        await interaction.channel.send("", view = MineView(client), embed= embed)
        
    '''/mapa'''
    @app_commands.command()
    async def mapa(self, interaction : discord.Interaction):
        '''Comando para o mapa do Mine'''
        if not isinstance(interaction.channel, discord.abc.Messageable):
            return 
        status = await self.client.fetch_channel(1065781076909359104)
        embed: discord.Embed = discord.Embed(title="Mapa do RPG", description=f"Para abrir o mapa, é necessário que o server esteja aberto.\nPara ver o status do server e abrí-lo, vá para {status.mention} ou https://discord.com/channels/1047320746453643344/1065781076909359104/1083384265925988544", color=colors().blurple)
        embed.add_field(name="Link do Mapa",value="http://mapamine.duckdns.com:8223/")
        embed.color = colors().light_grey
        await interaction.response.send_message("Map Message", delete_after=0.1)
        await interaction.channel.send("", embed= embed)


#Setup: --------------------------------------------------------------------------------
async def setup(client): # Must have a setup function
    await client.add_cog(Mine(client)) # Add the class to the cog.