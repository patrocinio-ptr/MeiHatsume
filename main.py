import discord
from typing import Union
import os
import sys
import random
from discord import app_commands
from discord.utils import get
from discord.ext import commands
import asyncio
from datetime import datetime, timedelta
from pytz import timezone
from utility import guild_id, MY_GUILD, colors, is_owner, get_members, get_server, update_events, owner, get_mestres, brasil #type: ignore
from mine import MineView, update_mine_button #type: ignore
from baralho_de_aventura import Descartar #type: ignore
from Secrets import TOKEN


intents = discord.Intents.all()
intents.members = True
cog_files = ["misc", "mine", "baralho_de_aventura", "rolagens"]

whitelist = [1047320746453643344]

class MyClient(commands.Bot):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents, command_prefix="?")   

    async def setup_hook(self):
        for cog_file in cog_files:
            await self.load_extension(cog_file)
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)
client = MyClient(intents=intents)


#Eventos:----------------------------------------------------------------------------------
#Eventos:----------------------------------------------------------------------------------
#Eventos:----------------------------------------------------------------------------------
@client.event #Ficando pronto
async def on_ready():
    print(f'Logged in as {client.user} (ID: {client.user})')
    print('-----------------------------------------------')
    await client.change_presence(activity=discord.Game(name="BNHA"))
    await update_mine_button(client)
    client.add_view(MineView(client))
    client.add_view(Session())
    client.add_view(Descartar())
    channel = client.get_channel(1065721164657336370)
    if not isinstance(channel, discord.abc.Messageable):
        return
    ptr = await client.fetch_user(286540943056830474)
    await channel.send(f"Bot on {ptr.mention}", delete_after=5)
    await update_events(client)
    
    #Checa se o bot ta no stage channel
    stage_channel = await client.fetch_channel(1086301770545889320)
    if not isinstance(stage_channel, discord.StageChannel):
        print("Stage channel deu errrado")
        return
    connected_members = stage_channel.voice_states.keys()
    flag = 0
    while flag == 0:
        await asyncio.sleep(1800)
        if len(connected_members) > 1:
            await client.voice_clients[0].disconnect(force= True)
            flag = 1


@client.event #whitelist bot
async def on_guild_join(guild):
    if guild.id not in whitelist:
        channel = guild.text_channels[0]
        await channel.send("Saindo do server porque não está na whitelist.")
        await guild.leave()
        print(f"Left {guild.name} because it's not on the whitelist.")


@client.event #quando evento for atualizado
async def on_scheduled_event_update(event, new_event):
    if (event.status == discord.EventStatus.scheduled) and (new_event.status == discord.EventStatus.active):
        channel = await client.fetch_channel(1085684537067053167)
        if not isinstance(channel, discord.abc.Messageable):
            return        
        nome_sessão = event.name.replace("(Sessão confirmada! ✅)", "")
        await channel.send(f"{nome_sessão} vai começar! @here, as cartas de aventura estão chegando na DM!")
        # Cartas são enviadas no event listener do clog Baralho de aventura.py
        stage_channel = await client.fetch_channel(1086301770545889320)
        if stage_channel and (isinstance(stage_channel,discord.StageChannel) or isinstance(stage_channel, discord.VoiceChannel)):
            try:
                await stage_channel.connect()
                print("Conectado no stage channel")
                connected_members = stage_channel.voice_states.keys()
                flag = 0
                while flag == 0:
                    print("Esperando alguém se conectar para sair do canal")
                    await asyncio.sleep(1800)
                    if len(connected_members) > 1:
                        await client.voice_clients[0].disconnect(force= True)
                        flag = 1
            except discord.errors.ClientException:
                print("Não conectado ao stage")
    await update_events(client)


@client.event #quando criar eventos
async def on_scheduled_event_create(event):
    await update_events(client)


@client.event #quando deletar eventos
async def on_scheduled_event_delete(event):
    await update_events(client)

#Botões: -----------------------------------------------------------------------------------------
#Botões: -----------------------------------------------------------------------------------------
#Botões: -----------------------------------------------------------------------------------------
class Session(discord.ui.View): #Botões do /sessão
    """Botões para o /sessão"""
    def __init__(self)-> None:
        super().__init__(timeout = None)
    
    @discord.ui.button(label="Posso participar!",custom_id = "Confirmado", style=discord.ButtonStyle.green) 
    async def button_callback1(self, interaction, button):
        #Pega as variáveis
        embed = interaction.message.embeds[0]
        nome = embed.description
        sessão = embed.title
        mestres = []
        channel = await client.fetch_channel(1047641289451130880) 
        if not isinstance(channel, discord.abc.Messageable):
            return
        members = await get_members(client)
        if not members:
            print("Members deu None")
            return
        
        #Habilita o botão vermelho e desabilita o verde
        for child in self.children: 
            child.disabled = False # type: ignore
            child.label = "Desconfirmar presença :("# type: ignore
        button.disabled = True 
        button.label = "Presença confirmada!" 
        button.emoji = "✅"
        await interaction.response.edit_message(view=self) 
        
        #Responde o user
        await interaction.user.send("Presença confirmada na sessão!")
        
        # manda dm pro mestre e para mim
        for member in members: 
            if discord.utils.get(member.roles, name="Mestres"): 
                await member.send(f"{interaction.user.mention} confirmou disponibilidade para: ", embed = embed)
                mestres.append(member)
            if member.id == 286540943056830474:
                await member.send(f"{interaction.user.mention} confirmou disponibilidade para: ", embed = embed)
                
        #procura no canal mensagens que tenham o mesmo título de sessão
        async for msg in channel.history(limit=None): 
            if not (len(msg.embeds) == 0):
                #pega os embeds da mensagem
                embeds = msg.embeds
                #procura nome e o número da sessão no embed da mensagem
                if (nome in embeds[0].description) and (sessão in embeds[0].title):
                    #pega o embed da mensagem
                    embed = embeds[0] 
                    confirmados = embed.fields[3].value
                    #checa se o membro foi mencionado na aba de confirmados, se não, coloca o nome dele(só para evitar bugs)
                    if not (interaction.user.mention in confirmados):
                        confirmados = embed.fields[3].value + interaction.user.mention + ";"
                        embed.set_field_at(3, name=embed.fields[3].name, value=confirmados)
                        await msg.edit(content = "", embed = embed)
                    
                    #tira o nome do fi da lista de desconfirmados, caso ele esteja la
                    try:
                        desconfirmados = embed.fields[4].value
                        if desconfirmados: #validação do field
                            if (interaction.user.mention in desconfirmados):
                                desconfirmados = desconfirmados.split(";")
                                desconfirmados = [m for m in desconfirmados if m.strip() != interaction.user.mention]
                                desconfirmados_str = ";".join(desconfirmados)
                                embed.set_field_at(4, name=embed.fields[4].name, value=desconfirmados_str, inline= False)
                                if desconfirmados == "":
                                    embed.remove_field(index=4)
                                    if client.user: #validação do bot
                                        await msg.remove_reaction(member = client.user,emoji="❌")
                                await msg.edit(content = "", embed = embed)
                    except Exception as e: #caso não tenha desconfirmados
                        print(f"{e}, {interaction.user.mention} não estava na lista de desconfirmados")

                    players = embed.fields[2].value #players chamados para sessão
                    confirmados = embed.fields[3].value #players confirmados
                    if  (players == None) or (confirmados == None):
                        print("Players ou Players chamados deu none")
                        return
                    
                    #checa se todos os players podem, e da verdinho na mensagem, além de mandar "Sessão confirmada"
                    players_total = len(players.split(","))
                    n_players = len(confirmados.split(";")[:-1])
                    porcent:float = n_players/players_total
                    
                    #Edita o campo de confirmados com um ratio de confirmados/totais
                    embed.set_field_at(3, name=f"Confirmados: ({n_players}/{players_total})", value=embed.fields[3].value)
                    await msg.edit(content = "", embed = embed)
                    
                    #Sessão confirmada
                    if porcent >= 1: 
                        #Pegando variáveis
                        channel = await client.fetch_channel(1085684537067053167)
                        guild = await get_server(client)
                        if not isinstance(channel, discord.abc.Messageable):
                            return
                        if not guild:
                            return

                        #Faz o embed bonitinho
                        embed.color = colors().green
                        embed.title = (sessão + "\nSessão confirmada!:white_check_mark:")
                        await msg.edit(content = "", embed = embed)
                        await msg.add_reaction("✅")
                        
                        jogadores = []
                        try:
                            if not embed.fields[2].value:
                                return
                            mentions_list = []
                            for mention in embed.fields[2].value.split(","):
                                mention = mention.strip(" ")
                                mention = mention.strip("<@")
                                mention = mention.strip(">")
                                mention = mention.strip(".")
                                mentions_list.append(mention)
                            members = []
                            for mention in mentions_list:
                                mention = mention.strip(" ")
                                mention = mention.strip("<@")
                                mention = mention.strip(">")
                                mention = mention.strip(".")
                                member = int(mention)
                                if member:
                                    members.append(member)
                            if not embed.title:
                                return
                            embed.title = embed.title.replace("\nSessão confirmada!✅", "")
                            embed.color = colors().green
                            for member in members: 
                                member = client.get_user(int(member))
                                if not member:
                                    return
                                message = await member.send(f"{embed.title} foi confirmada!✅ {member.mention}", embed=embed)
                                await message.add_reaction("✅")
                                jogadores.append(member.mention)
                            #Avisa o mestre
                            mestre = client.get_user(252150507345281024)
                            if not mestre:
                                print("Mestre não recebeu confirmação de sessão!")
                                return
                            await mestre.send(f"{embed.title} foi confirmada!✅ {mestre.mention}", embed=embed)
                        except:
                            pass
                        
                        
                        #Mensagem de aviso que a sessão foi confirmada
                        embed_sessão = embeds[0]
                        embed_sessão.color = colors().green
                        jogadores_str = ",".join(jogadores)
                        await channel.send(f"{sessão} foi confirmada {jogadores_str}!", embed = embed_sessão )    
                        
                        #Avisa o mestre
                        for mestre in mestres:
                            await mestre.send(f"{sessão} está confirmada com a presença de todos os players!", embed = embed_sessão)
                        
                        #Atualizando lista de eventos e editando nome do evento pra Confirmado
                        sessões_marcadas = await client.guilds[0].fetch_scheduled_events()
                        sessões_marcadas.sort(key=lambda event: event.start_time)
                        for event in sessões_marcadas:
                            if event.name.find(sessão) !=-1:
                                if not event.channel:
                                    print("Sem channel")
                                    return
                                await event.edit(name = (sessão + "(Sessão confirmada! ✅)"), channel = event.channel)
        
        
        embed = interaction.message.embeds[0]
        embed.color = colors().green
        discord_timestamp = discord.utils.format_dt(datetime.utcnow(), style="D")
        await interaction.message.edit(content = f"Presença confirmada em {discord_timestamp}!", embed = embed)             
                    
    @discord.ui.button(label="Não posso participar :(",custom_id = "Não confirmado", style=discord.ButtonStyle.red) 
    async def button_callback2(self, interaction, button):
        #pega variáveis
        embed = interaction.message.embeds[0]
        sessão = embed.title
        nome = embed.description
        channel = await client.fetch_channel(1047641289451130880) 
        mestres = []
        members = await get_members(client)
        if not isinstance(channel, discord.abc.Messageable):
           return
        if not members:
            return
        
        #Desabilita o botão vermelho e habilita o verde
        for child in self.children: 
            child.disabled = False # type: ignore
            child.label = "Posso participar!" # type: ignore
            child.emoji = None # type: ignore
        button.disabled = True 
        button.label = "Presença não confirmada :(" 
        await interaction.response.edit_message(view=self) 
        
        #responde a interação
        await interaction.user.send("Presença não confirmada :(")
        
        # manda para o mestre e pra mim a (in)disponibilidade
        for member in members: 
            if discord.utils.get(member.roles, name="Mestres"):
                await member.send(f"{interaction.user.mention} não tem disponibilidade para:", embed = embed)
                mestres.append(member)
            if member.id == 286540943056830474:
                await member.send(f"{interaction.user.mention} não tem disponibilidade para:", embed = embed)
        
        #edita a mensagem original no canal de marcações de sessão
        async for msg in channel.history(limit=None): 
            if not (len(msg.embeds) == 0):
                #pegando variáveis
                embed = msg.embeds[0]
                confirmados_old = embed.fields[3].value
                      
                #checa se o nome da sessão está na mensagem
                if embed.description == None:
                    return
                if (nome == embed.description) and (sessão in embed.title):
                    if confirmados_old: #Caso alguém já tenha confirmado
                        confirmados = confirmados_old.split(";") 
                        if not embed.fields[3].value:
                            return
                        if embed.fields[3].value.find(interaction.user.mention) != -1:
                            #Refaz a lista de confirmados
                            confirmados_new = [m for m in confirmados if m.strip() != interaction.user.mention] #nova lista de confirmados, sem o cara que desconfirmou
                            confirmados = ""
                            confirmados = ";".join(confirmados_new) #faz a string separando por ";"
                            if confirmados == ";":
                                confirmados = ""
                            
                            #faz o novo embed com nova lista de confirmados
                            players_total = embed.fields[2].value
                            list = confirmados
                            n_players = 0
                            if not (players_total == None or list == None):
                                players_total = len(players_total.split(","))
                                n_players = len(list.split(";")) - 1
                            embed.set_field_at(3, name=f"Confirmados: ({n_players}/{players_total})", value=confirmados, inline= False)                        
                    
                    # (NÃO TIRA MAIS) Tirando "Sessão confirmada, se tiver no título"    
                    title = embed.title
                    if not title:
                        return
                    
                    '''if title.find("Sessão confirmada!")!=-1:
                        aux = title.split("\n")
                        title = aux[0]
                        embed.title = title
                        for mestre in mestres:
                            await mestre.send(f"{title} foi cancelada pois um player desconfirmou ;-;, {mestre.mention}")
                        if not client.user: #validação do bot
                            return
                        await msg.remove_reaction(member=client.user, emoji="✅")'''

                    #Field dos desconfirmados
                    try:
                        desconfirmados = embed.fields[4].value
                        if not (interaction.user.mention in desconfirmados): #Se o player não estiver na lista
                            desconfirmados = embed.fields[4].value + interaction.user.mention + ";"
                            embed.set_field_at(4, name=embed.fields[4].name, value=desconfirmados, inline= False)
                            await msg.edit(content = "", embed = embed)
                            
                    except: #Se não tiver esse field no embed
                        embed.add_field(name=f"Não pode(m):", value=f"{interaction.user.mention};", inline= False)
                        await msg.edit(content = "", embed = embed)  
                        #manda no Avisos que a sessão vai ter que ser remarcada, mas só se este for o primeiro desconfirmado
                        channel = await client.fetch_channel(1085684537067053167)
                        if not isinstance(channel, discord.abc.Messageable):
                            return
                        guild = await get_server(client)
                        if not guild:
                            return
                        jogadores = discord.utils.get(guild.roles, id=1047640423012761711)
                        if not jogadores:
                            print("jogadores deu None")
                            return
                        #NÃO MANDA MAIS NO CANAL
                        #await channel.send(f"A {sessão} não foi confirmada, porque um ou mais players não podem comparecer. Tentaremos marcar novamente!{jogadores.mention}")

                    #(NÃO CANCELA A SESSÃO DIRETO)edita a msg 
                    #embed.color= colors().dark_red
                    #await msg.add_reaction("❌")
                    
                    
                    #(NÃO EDITA MAIS)edita o evento
                    '''sessões_marcadas = await client.guilds[0].fetch_scheduled_events()
                    sessões_marcadas.sort(key=lambda event: event.start_time)
                    for event in sessões_marcadas:
                        if event.name.find(sessão) !=-1:
                            if event.name.find("(Sessão confirmada! ✅)") !=-1:
                                await event.edit(name = sessão, channel= event.channel)'''
        
        embed = interaction.message.embeds[0]
        embed.color = colors().dark_red
        discord_timestamp = discord.utils.format_dt(datetime.utcnow(), style="D")
        await interaction.message.edit(content = f"Presença não confirmada em {discord_timestamp}!", embed = embed)  


#comandos: ----------------------------------------------------------------------------------
#comandos: ----------------------------------------------------------------------------------
#comandos: ----------------------------------------------------------------------------------


'''/sessão''' #Marca a sessão, mandando dm pra todos
@client.hybrid_command()
@app_commands.rename(members_or_role='players')
@app_commands.describe( 
    numero_da_sessão='Número da sessão, como 0, 0.1, 1, 2, etc',
    tipo_de_sessão = 'Emoji referente ao tipo de sessão(copie e cole do catálogo). Ex.(Sessão principal):🎮',
    nome = 'Nome da sessão. Ex.: A morte de Freeza',
    data = 'Data que a sessão ocorrerá. Ex.: 28/02',
    horário = 'Horário da sessão. Ex.: 18:00',
    members_or_role = 'Players que jogarão a sessão, como menções. Ex.: @Pendragon(pode usar @cargo também)'
)
async def sessão(ctx: commands.Context, numero_da_sessão: str,tipo_de_sessão: str, nome:str, data : str,horário: str,data_in_game: str, members_or_role: commands.Greedy[Union[discord.Member, discord.Role]]):
    #Fazendo a lista com os member objects de cada um mencionado, sendo role ou pessoa em si
    members = []
    for member_or_role in members_or_role:
        if isinstance(member_or_role, discord.Role):
            members.extend(member_or_role.members)
        elif isinstance(member_or_role, discord.Member):
            members.append(member_or_role)
    #Transformando todos os players em uma string pra colocar no embed
    players = ""
    for player in members:
        players += player.mention + ", "
    players = players[:-2] + "."
    n_players = len(members)
    
    #Data
    aux = data.split("/")
    data_new = aux[1] + "/" + aux[0] +"/2023 "+horário+":00" #data
    data_object = brasil.localize(datetime.utcnow().strptime(data_new, '%m/%d/%Y %H:%M:%S'))
    discord_timestamp_horas = discord.utils.format_dt(data_object, style="t")
    discord_timestamp_data = discord.utils.format_dt(data_object, style="d")
    #criando o embed
    embed = discord.Embed(title=f"Sessão {numero_da_sessão}({tipo_de_sessão})", description=f'"||{nome}||\n Data in-game:{data_in_game}"', color = colors().teal)
    embed.add_field(name="Data:",value=discord_timestamp_data, inline=False)
    embed.add_field(name="Horário:",value=discord_timestamp_horas, inline=False)
    embed.add_field(name="Players: ",value=players, inline=False)
    embed.add_field(name = f"Confirmados: (0/{n_players})", value = "", inline=False)
    
    #mandando msg no canal
    message = await ctx.reply(f"{players}", embed = embed)
    await message.edit(content=None,embed=embed) #Tira as menções da mensagem
    
    #mensagem para cada player na sessão, com botões
    for player in members:
        try:
            embed.remove_field(index=3) #Tira o campo "Confirmados"
            embed.set_footer(text = "tuuty")
            await player.send(f"{player.mention}",embed=embed, view= Session())
        except Exception as e:
            await ctx.channel.send(f"{player} não recebeu notificação na Dm, \n {e}")
    
    #criando o evento
    guild = await client.fetch_guild(guild_id)
    if not embed.title:
        return
    sessão = embed.title
    await guild.create_scheduled_event(name= sessão, start_time=data_object, channel=client.get_channel(1086301770545889320), description=(f"'||{nome}||' \nPlayers: {players}"))

    #Avisando o mestre
    mestres = await get_mestres(client)
    if not mestres:
        print("Mestres de None")
        return
    embed.color = colors().orange
    for mestre in mestres:
        await mestre.send("A seguinte sessão foi marcada:", embed = embed)
    ptr = await client.fetch_user(286540943056830474)
    await ptr.send("A seguinte sessão foi marcada:", embed = embed)
        

    
'''/Confirmar [Título da sessão]'''
@client.tree.command()
async def confirmar(interaction: discord.Interaction, title: str):
    '''Confirma uma sessão.'''
    await interaction.response.send_message("Confirmando sessão...", delete_after=5)
    #Pegando variáveis
    sessões_channel = await client.fetch_channel(1047641289451130880)
    avisos_channel = await client.fetch_channel(1085684537067053167)
    guild = await get_server(client)
    if not isinstance(sessões_channel, discord.abc.Messageable) or not isinstance(avisos_channel, discord.abc.Messageable):
        print("Um dos canais não mensageável")
        return
    if not guild:
        return
    
    #Busca uma mensagem que contenha o título escrito
    async for message in sessões_channel.history(limit = None):
        if message.embeds:
            embed = message.embeds[0]
            if not embed.title:
                print("Embed title não rolou")
                continue
            embed_sessão = embed
            if embed.title.find(title) != -1:
                #Edita a msg com "Confirmada"
                new_embed = embed
                new_embed.title = title+"\nSessão confirmada!✅"
                new_embed.color = colors().green
                await message.edit(embed=new_embed)
                await message.add_reaction("✅")
                if not client.user:
                    return
                await message.remove_reaction("❌", member = client.user)
                
                #Avisa os players da confirmação(na dm e no canal de avisos)
                try:
                    if not embed.fields[2].value:
                        return
                    jogadores = embed.fields[2].value
                    mentions_list = []
                    for mention in embed.fields[2].value.split(","):
                        mention = mention.strip(" ")
                        mention = mention.strip("<@")
                        mention = mention.strip(">")
                        mention = mention.strip(".")
                        mentions_list.append(mention)
                    members = []
                    for mention in mentions_list:
                        mention = mention.replace(" ", "")
                        mention = mention.replace("<@","")
                        mention = mention.replace(">","")
                        mention = mention.replace(".","")
                        member = int(mention)
                        if member:
                            members.append(member)
                    if not embed.title:
                        return
                    embed.title = embed.title.replace("\nSessão confirmada!✅", "")
                    embed.color = colors().green
                    for member in members: 
                        member = client.get_user(int(member))
                        if not member:
                            return
                        message = await member.send(f"{embed.title} foi confirmada!✅ {member.mention}", embed=embed)
                        await message.add_reaction("✅")
                    #Avisa o mestre
                    mestre = client.get_user(252150507345281024)
                    if not mestre:
                        print("Mestre não recebeu confirmação de sessão!")
                        return
                    await mestre.send(f"{embed.title} foi confirmada!✅ {mestre.mention}", embed=embed)
                    #Mensagem de aviso que a sessão foi confirmada
                    embed_sessão.color = colors().green
                    jogadores = jogadores.strip(".")
                    await avisos_channel.send(f"{title} foi confirmada {jogadores}!", embed = embed_sessão)    
                    
                except Exception as e:
                    print(f"Embed não foi adquirido: {e}")
                break
    #Atualizando lista de eventos e editando nome do evento pra Confirmado
    sessões_marcadas = await client.guilds[0].fetch_scheduled_events()
    sessões_marcadas.sort(key=lambda event: event.start_time)
    
    for event in sessões_marcadas:
        if not event.channel:
            return
        if event.name.find(title) !=-1:
            await event.edit(name = (title + "(Sessão confirmada! ✅)"), channel= event.channel)
                
    
    

'''/Cancelar [Título da sessão]'''
@client.tree.command()
async def cancelar(interaction: discord.Interaction, title: str):
    '''Cancela uma sessão.'''
    await interaction.response.send_message("Cancelando sessão...D:", delete_after=5)
    #Pegando variáveis
    guild = await get_server(client)
    sessões_channel = await client.fetch_channel(1047641289451130880)
    avisos_channel = await client.fetch_channel(1085684537067053167)
    guild = await get_server(client)
    if not isinstance(sessões_channel, discord.abc.Messageable) or not isinstance(avisos_channel, discord.abc.Messageable):
        print("Um dos canais não mensageável")
        return
    if not guild:
        return
    
    #Busca uma mensagem que contenha o título escrito
    async for message in sessões_channel.history(limit = None):
        if message.embeds:
            embed = message.embeds[0]
            if not embed.title or not embed.description:
                print("Título ou description da embed não rolou")
                continue
            embed_sessão = embed
            if embed.title.find(title) != -1:
                #Edita a msg com "Confirmada"
                new_embed = embed
                aux = embed.title
                new_embed.title = "Sessão cancelada❌"
                new_embed.description = embed.description + "\n" + aux
                new_embed.color = colors().dark_red
                embed_sessão = new_embed
                await message.edit(embed=new_embed)
                await message.add_reaction("❌")
                if not client.user:
                    return
                await message.remove_reaction("✅", member=client.user)
                
                #Avisa os players da desconfirmação(na dm e no canal de avisos)
                try:
                    if not embed.fields[2].value:
                        print("Sessão não contém field de players")
                        return
                    jogadores = embed.fields[2].value
                    mentions_list = []
                    for mention in embed.fields[2].value.split(","):
                        mention = mention.strip(" ")
                        mention = mention.strip("<@")
                        mention = mention.strip(">")
                        mention = mention.strip(".")
                        mentions_list.append(mention)
                    members = []
                    for mention in mentions_list:
                        mention = mention.replace(" ", "")
                        mention = mention.replace("<@","")
                        mention = mention.replace(">","")
                        mention = mention.replace(".","")
                        member = int(mention)
                        if member:
                            members.append(member)
                    if not embed.title:
                        return
                    embed.title = embed.title.strip("\nSessão confirmada!✅")
                    embed.title = embed.title.replace("\nSessão confirmada!✅", "")
                    embed.color = colors().dark_red
                    for member in members: 
                        member = client.get_user(int(member))
                        if not member:
                            return
                        message = await member.send(f"{embed.title} foi cancelada❌ {member.mention}", embed=embed)
                        await message.add_reaction("❌")
                        if not member.dm_channel:
                            print("Dm do membro deu None")
                            continue
                    #Avisa o mestre
                    mestre = client.get_user(252150507345281024)
                    if not mestre:
                        print("Mestre não recebeu confirmação de sessão!")
                        return
                    await mestre.send(f"{embed.title} foi cancelada❌ {mestre.mention}", embed=embed)
                    #Mensagem de aviso que a sessão foi confirmada
                    embed_sessão.color = colors().dark_red
                    jogadores = jogadores.strip(".")
                    await avisos_channel.send(f"{title} foi cancelada❌ {jogadores}!", embed = embed_sessão)    
                    #Edita a mensagem de chamada pra sessão na dm de cada um
                    for member in members:
                        async for message in member.dm_channel.history(limit = None):
                            if message.embeds:
                                embed = message.embeds[0]
                                if not embed.title or not embed.description:
                                    print("Título ou description da embed não rolou")
                                    continue
                                embed_sessão = embed
                                if embed.title.find(title) != -1:
                                    #Edita a msg com "Confirmada"
                                    new_embed = embed
                                    new_embed.title = "Sessão cancelada❌"
                                    new_embed.description = embed.description + "\n" + title
                                    new_embed.color = colors().dark_red
                                    await message.edit(embed=new_embed)
                                    await message.add_reaction("❌")
                except Exception as e:
                    print(f"Embed não foi adquirido: {e}")
                break
    #Atualizando lista de eventos e editando nome do evento pra Confirmado
    sessões_marcadas = await client.guilds[0].fetch_scheduled_events()
    sessões_marcadas.sort(key=lambda event: event.start_time)
    
    

    for event in sessões_marcadas:
        if not event.channel:
            return
        if event.name.find(title) != -1:
            await event.delete()
                



'''/Desconfirmar
    edita a mensagem(deixa a cor neutra, tira todas as reações, tira toda a segunda parte do título(confirmada ou cancelada))
@client.tree.command()
async def desconfirmar(interaction: discord.Interaction):
    ''Edita a mensagem, remove todas as reações e deixa a cor neutra''
    channel = await client.fetch_channel(1047641289451130880)
    if not isinstance(channel, discord.abc.Messageable):
        return
    await interaction.response.send_message("Desconfirmando sessão...", delete_after=5)
    
    async for message in channel.history(limit=None):
        if message.embeds:
            embed = message.embeds[0]
            if not embed.title:
                return
            
            # Check if the title contains "confirmada" or "cancelada"
            if "confirmada" in embed.title.lower() or "cancelada" in embed.title.lower():
                # Remove all reactions from the message
                await message.clear_reactions()
                
                # Reset the embed color to neutral
                embed.color = discord.Color.default()
                
                # Remove the second part of the title
                embed.title = embed.title.split("(")[0].strip()
                
                # Edit the message with the updated embed
                await message.edit(embed=embed)
                break


'''



'''/Concluídas'''            
@client.tree.command()  
async def concluidas(interaction: discord.Interaction):
    '''Checa no canal de marcar sessões, quais sessões foram concluídas, e edita as mensagens'''
    channel = await client.fetch_channel(1047641289451130880)
    if not isinstance(channel,discord.abc.Messageable):
        return
    await interaction.response.send_message("Concluindo sessões finalizadas...", delete_after=5)
    async for message in channel.history(limit = None):
        if message.embeds:
            embed = message.embeds[0]
            if not embed.title :
                return
            if not embed.fields[0].value:
                return
            if embed.title.find("Sessão confirmada!")!=-1:
                date = embed.fields[0].value.replace("<t:","") 
                date = date.replace(":d>","")   
                date_object = datetime.fromtimestamp(int(date))
                if date_object < datetime.now()+timedelta(days=1):
                    
                    aux = embed.title.split(")")
                    aux = aux[0]+ ")"
                    embed.title = aux+"\nSessão concluída!☑️"
                    embed.color = colors().blue
                    if not client.user:
                        return
                    await message.remove_reaction( member= client.user, emoji= "✅")
                    await message.add_reaction("☑️")
                    await message.edit(embed= embed)
        
        

'''/teste''' #Teste
@client.tree.command()
async def teste(interaction):
    """TESTE"""
    channel = await client.fetch_channel(1065721164657336370)
    if not isinstance(channel, discord.abc.Messageable):
        return
    await channel.send("Teste")
    stage_channel = await client.fetch_channel(1086301770545889320)
    if stage_channel and (isinstance(stage_channel,discord.StageChannel) or isinstance(stage_channel, discord.VoiceChannel)):
        try:
            await stage_channel.connect()
            print("Conectado no stage channel")
        except discord.errors.ClientException:
            print("Não conectado ao stage")
        connected_members = stage_channel.voice_states.keys()
        flag = 0
        while flag == 0:
            await asyncio.sleep(1800)
            if len(connected_members) > 1:
                await client.voice_clients[0].disconnect(force= True)
                flag = 1
    
    
    
client.run(TOKEN)

    
'''Dump do chat gpt:
    
async def str_to_members(guild, members_string):
    member_ids = [int(member_id) for member_id in members_string.split() if member_id.isdigit()]
    members = [guild.get_member(member_id) for member_id in member_ids]
    return [member for member in members if member is not None]


async def concluir_sessao(session_message):
    if session_message.embeds:
        embed = session_message.embeds[0]
        if embed.title.find("Sessão confirmada!") != -1:
            embed.title = embed.title.replace("Sessão confirmada!", "Sessão concluída!☑️")
            embed.color = discord.Color.blue()
            await session_message.clear_reactions()
            await session_message.add_reaction("☑️")
            await session_message.edit(embed=embed)


from datetime import datetime
from pytz import timezone

def get_time(timezone_name):
    tz = timezone(timezone_name)
    return datetime.now(tz)

def find_carta_aventura(cards, name):
    for card in cards:
        if card['name'] == name:
            return card
    return None


async def move_members_to_stage(guild, stage_channel):
    for voice_channel in guild.voice_channels:
        if voice_channel != stage_channel:
            for member in voice_channel.members:
                await member.move_to(stage_channel)


async def send_dm_to_players(players, message_content):
    for player in players:
        try:
            await player.send(message_content)
        except discord.Forbidden:
            print(f"Failed to send DM to {player.name}")


async def create_diario_page(diario_channel, template_content):
    await diario_channel.send(template_content)


async def edit_concluded_event(event_message):
    if event_message.embeds:
        embed = event_message.embeds[0]
        embed.description = embed.description.replace("Evento ativo", "Evento concluído")
        await event_message.clear_reactions()
        await event_message.edit(embed=embed)


async def send_reminders(players, session_date):
    current_date = datetime.now()
    days_since_session = (current_date - session_date).days
    if days_since_session % 3 == 0:
        for player in players:
            try:
                await player.send("Lembrete: Você ainda não respondeu à sessão. Por favor, confirme sua presença ou desconfirme se não puder comparecer.")
            except discord.Forbidden:
                print(f"Failed to send reminder to {player.name}")


async def auto_cancel_session(session_message, scheduled_date):
    current_date = datetime.now()
    if current_date >= scheduled_date:
        embed = session_message.embeds[0]
        embed.title = embed.title.replace("Sessão confirmada", "Sessão cancelada")
        embed.color = discord.Color.red()
        await session_message.clear_reactions()
        await session_message.edit(embed=embed)


async def move_members_to_stage_on_start(guild, stage_channel):
    for voice_channel in guild.voice_channels:
        if voice_channel != stage_channel:
            for member in voice_channel.members:
                await member.move_to(stage_channel)


async def send_dm_to_players_on_start(players, message_content):
    for player in players:
        try:
            await player.send(message_content)
        except discord.Forbidden:
            print(f"Failed to send DM to {player.name}")


async def create_session_log_entry(session_data):
    diary_channel = await client.fetch_channel(YOUR_DIARY_CHANNEL_ID)
    if not isinstance(diary_channel, discord.TextChannel):
        return

    session_info = f"Session Date: {session_data['date']}\n" \
                   f"Duration: {session_data['duration']}\n" \
                   f"Participants: {', '.join(session_data['players'])}\n" \
                   f"Summary: {session_data['summary']}"
    
    await diary_channel.send(session_info)


async def update_event_description(event_message, session_name):
    embed = event_message.embeds[0]
    embed.description = session_name
    await event_message.edit(embed=embed)


async def update_session_status(session_message):
    current_date = datetime.now()
    embed = session_message.embeds[0]
    if embed.timestamp.date() < current_date.date():
        embed.title = embed.title.replace("Sessão confirmada", "Sessão concluída")
        # Optionally, you can add a button to the message for additional functionality
        embed.add_field(name="Status", value="Concluída")
        await session_message.clear_reactions()
        await session_message.edit(embed=embed)


async def delete_messages_with_content(channel, content):
    async for message in channel.history(limit=None):
        if content.lower() in message.content.lower():
            await message.delete()



@client.command()
async def calculator(ctx, operation: str, *numbers: float):
    if operation == "add":
        result = sum(numbers)
        await ctx.send(f"The result of adding {', '.join(map(str, numbers))} is {result}.")
    elif operation == "multiply":
        result = 1
        for num in numbers:
            result *= num
        await ctx.send(f"The result of multiplying {', '.join(map(str, numbers))} is {result}.")
    elif operation == "divide":
        result = numbers[0]
        for num in numbers[1:]:
            if num == 0:
                await ctx.send("Error: Division by zero is not allowed.")
                return
            result /= num
        await ctx.send(f"The result of dividing {', '.join(map(str, numbers))} is {result}.")
    else:
        await ctx.send("Invalid operation. Available operations: add, multiply, divide.")



from dateutil.parser import parse

@client.command()
async def purge_after_date(ctx, date_string: str):
    target_date = parse(date_string)
    async for message in ctx.channel.history(limit=None, after=target_date):
        await message.delete()



from datetime import datetime, timedelta

def calculate_next_session_date(interval):
    current_date = datetime.now().date()
    next_date = current_date + timedelta(days=interval)
    return next_date.strftime("%Y-%m-%d")



@client.command()
async def initiative(ctx, *players):
    players = list(players)
    players.sort()  # Sort players alphabetically
    # Calculate initiative order based on the number of cards each player has
    initiative_order = sorted(players, key=lambda p: int(p.split("(")[-1].rstrip(")")), reverse=True)
    await ctx.send(f"The initiative order is: {', '.join(initiative_order)}.")

    
    
    
    
    
    
    
    '''
