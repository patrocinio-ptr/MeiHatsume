import discord
from discord import app_commands
from discord.ext import commands
import random
from typing import Union
import os
import sys
from utility import is_owner, get_members, get_server, owner, is_mestre #type: ignore
import asyncio

#Classe:--------------------------------------------------------------------------------
#Classe:--------------------------------------------------------------------------------
#Classe:--------------------------------------------------------------------------------
class Misc(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    #Funções:--------------------------------------------------------------------------------
    #Funções:--------------------------------------------------------------------------------
    #Funções:--------------------------------------------------------------------------------
    async def dm_purge_all_function(self):
        server = self.client.guilds[0]
        members = server.members
        await self.client.change_presence(activity=discord.Game(name="Deletando Mensagens"))
        
        print(f"Purjando dm dos membros")
        for member in members:
            try:
                async for message in member.history(limit = None):
                    if message.author == self.client.user:
                        try:
                            footer = message.embeds[0].footer.text
                            if footer.find("tuuty") == -1: #type: ignore
                                await message.delete()
                                print("Mensagem deletada")
                        except:
                            await message.delete()
                            print("Mensagem deletada")
            except Exception as e:
                print(f"Não foi possível purjar: {member} /n {e}")
        await self.client.change_presence(activity=discord.Game(name="BNHA"))
    #Eventos: --------------------------------------------------
    #Eventos: --------------------------------------------------
    #Eventos: --------------------------------------------------
    @commands.Cog.listener()
    async def on_ready(self):
        await self.dm_purge_all_function()
        return
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if isinstance(message.channel, discord.channel.DMChannel) and (await owner(message.author)):
            if message.content.startswith(";restart"):     
                await message.channel.send("Reiniciando o bot...")
                os.execv(sys.executable, ['python'] + sys.argv)
        '''if "tuty" in message.content:
            await message.channel.send("Boiola")'''

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        ptr = await self.client.fetch_user(286540943056830474)
        tuty = await self.client.fetch_user(252150507345281024)
        channel = await self.client.fetch_channel(1065721164657336370)
        if after.channel != before.channel and (after.channel):
            if not (member == tuty):
                await tuty.send(f"{member.mention} entrou no canal de voz: {after.channel}, {tuty.mention}")
            if member == ptr:
                return
            await channel.send(f"{member.mention} entrou no canal de voz: {after.channel}, {ptr.mention}")
            if member.id == 882491278581977179 or member == self.client.user:
                try:
                    await member.edit(suppress = False)
                    print("Chamou pra entrar")
                except:
                    print("Bot de música entrou num canal, mas não era stage então não precisou dar permissão para falar")
            
            #await ptr.send(f"{member.mention} entrou no canal de voz: {after.channel}, {ptr.mention}")
        if not after.channel:
            if not (member == tuty):
                await tuty.send(f"{member.mention} saiu do canal de voz: {before.channel}, {tuty.mention}")
            if member == ptr:
                return
            await channel.send(f"{member.mention} saiu do canal de voz: {before.channel}, {ptr.mention}")
            #ptr = await self.client.fetch_user(286540943056830474)
            #await ptr.send(f"{member.mention} saiu do canal de voz: {before.channel}")
    
    #Comandos: --------------------------------------------------
    #Comandos: --------------------------------------------------
    #Comandos: --------------------------------------------------
    '''/bibar''' #Biba o cara i vezes
    @app_commands.command() 
    @app_commands.check(is_owner)
    async def bibar(self, interaction: discord.Interaction, user : discord.Member): 
        """Biba"""
        i=1
        await interaction.response.send_message(f"{user.mention} está sendo bibbado")
        while i>0:
            await user.send("biba")
            print(f"Bibada em {user} número {i}")
            i -=1
        print("Bibada terminada")
        
        
    '''/editar'''
    @app_commands.command()
    async def editar(self, interaction: discord.Interaction, message_id: str, content: str = "",title: str = "", description:str = "" ):
        '''Edita o embed da mensagem cujo id condiza com o colocado, usando os parametros fornecidos para a edição'''
        message_id_int = int(message_id)
        channel = interaction.channel
        if not isinstance(channel, discord.abc.Messageable):
            return
        message = await channel.fetch_message(message_id_int)
        if not message.embeds:
            return
        embed = message.embeds[0]
        
        if title == "":
            pass
        else:
            embed.title = title
            
        if description == "":
            pass
        else:
            embed.description = description
            
        if content == "":
            content = message.content
        
        
        await message.edit(content = content,embed= embed)
        await interaction.response.send_message("Editadas com sucesso.", delete_after= 5)
        
        
    '''/purge''' #Deleta todas as mensagens enviadas pelo bot em um canal
    @app_commands.command()
    @app_commands.check(is_owner)
    async def purge(self, interaction: discord.Interaction, limite: int):
        """Deleta todas as mensagens do bot de um canal de texto específico(com limite)"""
        if not isinstance (interaction.channel, discord.abc.Messageable):
                return # or send an error
        await interaction.response.send_message("Purjando", delete_after=1)
        await self.client.change_presence(activity=discord.Game(name="Deletando Mensagens"))
        async for message in interaction.channel.history(limit = limite):
            await message.delete()  
            ''' if message.author == client.user:
                await message.delete()'''
        await interaction.channel.send("Purjado", delete_after = 1)
        await self.client.change_presence(activity=discord.Game(name="BNHA"))
    
    
    '''/holocausto''' #Deleta todas as mensagens enviadas pelo bot em um canal
    @app_commands.command()
    @app_commands.check(is_owner)
    async def holocausto(self, interaction: discord.Interaction, channel : discord.TextChannel):
        """Deleta todas as mensagens do bot de um canal de texto específico"""
        if not isinstance (channel, discord.abc.Messageable):
                return # or send an error
        await interaction.response.send_message("Purjando", delete_after=1)
        await self.client.change_presence(activity=discord.Game(name="Deletando Mensagens"))
        async for message in channel.history(limit = None):
            await message.delete()  
            ''' if message.author == client.user:
                await message.delete()'''
        await channel.send("Purjado", delete_after = 1)
        await self.client.change_presence(activity=discord.Game(name="BNHA"))


    '''/dmpurge [Player]'''#Deleta todas as msgs da dm de um player, menos as de sessões
    @app_commands.command()
    @app_commands.check(is_owner)
    async def dmpurge(self, interaction: discord.Interaction, user : discord.Member):
        """Deleta todas as mensagens do bot na DM de um Player específico"""
        channel = interaction.channel
        if not isinstance (channel, discord.abc.Messageable):
                return # or send an error
        try:
                await interaction.response.send_message("Purjando")
                await self.client.change_presence(activity=discord.Game(name="Deletando Mensagens"))
                await self.client.change_presence(activity=discord.Game(name="BNHA"))
                async for message in user.history(limit = None):
                    if message.author == self.client.user:
                        try:
                            footer = message.embeds[0].footer.text
                            if footer.find("tuuty") == -1: #type: ignore
                                await message.delete()
                                print("Mensagem deletada")
                        except:
                            await message.delete()
                            print("Mensagem deletada")
        except:
                print(f"{user}")
                await interaction.response.send_message("Deu ruim.")
                await self.client.change_presence(activity=discord.Game(name="BNHA"))


    '''/dmpurgeall''' #Deleta todas as msgs da dm de todos os players, menos as de sessões
    @app_commands.command()
    @app_commands.check(is_owner)
    async def dmpurgeall(self, interaction: discord.Interaction):
        """Deleta todas as mensagens do bot em todas as DMs"""
        await interaction.response.send_message("DMs sendo purjadas!", delete_after= 1)
        await self.dm_purge_all_function(interaction= interaction)
        if not isinstance (interaction.channel, discord.abc.Messageable):
            return
        await interaction.channel.send("Todas as DMs foram purjadas!:D")


    '''/delembed_dm [Conteúdo no titulo do embed]'''
    @app_commands.command()
    async def delembed_dm(self, interaction, title: str):
        '''Deleta as mensagens que contenham o título fornecido, na dm de todo mundo'''
        await interaction.response.send_message("Deletando mensagens...", delete_after = 1)
        members = await get_members(self.client)
        if not members:
            print("Members deu None")
            return
        for member in members:
            try:
                async for message in member.history(limit = None):
                    try:
                        if message.embeds[0].title.find(title)!=-1: #type: ignore
                            await message.delete()
                    except:
                        pass
            except Exception as e: 
                print(f"Não consegui deletar msg de {member.name}, exceção :\n{e}")


    '''/dmholocausto''' #Deleta todas as msgs da dm de todos os players(todas mesmo)
    @app_commands.command()
    @app_commands.check(is_owner)
    async def dmholocausto(self, interaction: discord.Interaction):
        """Deleta todas as mensagens do bot em todas as DMs"""
        await interaction.channel.send("DM holocausto será efetuado em 5 minutos, se isso foi um erro, você tem este tempo para parar o bot.")
        asyncio.sleep(300)
        server = self.client.guilds[0]
        members = server.members
        await interaction.response.send_message("DMs sendo purjadas(mesmo)!", delete_after= 1)
        await self.client.change_presence(activity=discord.Game(name="Deletando Mensagens"))
        await self.client.change_presence(activity=discord.Game(name="BNHA"))
        print(f"Purjando dm dos membros")
        for member in members:
            try:
                async for message in member.history(limit = None):
                    if message.author == self.client.user:
                    
                                await message.delete()
                                print("Mensagem deletada")
            except Exception as e:
                print(f"Não foi possível purjar: {member} /n {e}")
        if not isinstance (interaction.channel, discord.abc.Messageable):
            return
        await interaction.channel.send("Todas as DMs foram purjadas!:D")
        await self.client.change_presence(activity=discord.Game(name="BNHA"))


    '''/restart''' #Restarta o bot
    @app_commands.command()
    @app_commands.check(is_owner)
    async def restart(self, interaction: discord.Interaction):
        """Reiniciar bot"""
        await interaction.response.send_message("Reiniciando o bot...")
        os.execv(sys.executable, ['python'] + sys.argv)
        
        
    '''/stop''' #Fecha o bot
    @app_commands.command()
    @app_commands.check(is_owner)
    async def stop(self, interaction: discord.Interaction):
        """Desligar o bot"""
        await interaction.response.send_message("Desligando o bot...")
        await self.client.close()


    '''/mail [@player] [Mensagem]''' #Manda uma dm para os players
    @commands.hybrid_command()
    @app_commands.rename(members_or_role='players')
    @app_commands.check(is_mestre)
    @app_commands.describe( 
        members_or_role = 'Players que receberão a mensagem(pode usar @cargo também)'
    )
    async def mail(self,ctx: commands.Context, members_or_role: commands.Greedy[Union[discord.Member, discord.Role]], mensagem : str):
        '''Manda mensagem para os jogadores mencionados'''
        members = []
        for member_or_role in members_or_role:
            if isinstance(member_or_role, discord.Role):
                members.extend(member_or_role.members)
            elif isinstance(member_or_role, discord.Member):
                members.append(member_or_role)
        for member in members:
            try:
                await member.send(mensagem + "\n" + member.mention)
                await ctx.channel.send(f"Mensagem enviada para: {member.mention}")
            except:
                await ctx.channel.send(f"Não foi possível enviar mensagem para: {member.mention}")



async def setup(client): # Must have a setup function
    await client.add_cog(Misc(client)) # Add the class to the cog.