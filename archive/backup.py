from typing import Optional
import discord
import os
import sys
import random
from discord import app_commands
from discord.ext import commands
import asyncio
from datetime import datetime
from pytz import timezone
from mine import MineView

TOKEN = "MTA3ODcyNDM4NDkyMDk2NTEzMA.GZXmUj.0e1YU_6MmTUVpQ0EiQutiOH966rnnU048LIq0E"
MY_GUILD = discord.Object(id=1047320746453643344)
guild_id = int(1047320746453643344)
intents = discord.Intents.all()
intents.members = True
cog_files = ["misc", "mine"]

class MyClient(commands.Bot):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents, command_prefix="?")   

    async def setup_hook(self):
        # This copies the global commands over to your guild.
        for cog_file in cog_files:
            await self.load_extension(cog_file)
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)
client = MyClient(intents=intents)

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
deck = [
  'Antes você do que eu: Ao receber um ataque, jogue esta carta, e um personagem adjacente a você receberá o ataque em seu lugar.',

'Watashi Ga Kita: A ajuda chega à cena vinda de alguma fonte determinada pelo mestre.',

'Ao estilo russo: Jogue essa carta após se recuperar de um teste de morte. Você não sofre lesões, mas ainda está inconsciente.',

'Tankei foi tudo: Nega o dano total de um ataque.',

'Ás: Em vez de rolar um teste de característica, considere uma ampliação automática.',

'Exceder poder: Dobra o dano de um ataque(precisa ser um poder), sem gastar EQ, mas faz um teste de Vigor-2, ou sofre um nível de Fadiga.',

'Boa fama: Ganhe +1 de carisma permanente após fazer uma boa ação. Esse ponto se aplica apenas aqueles que ouviram falar de você, ou o conhecem.',

'Contatos: Seu personagem encontra um velho amigo/conhecido, que pode lhe ajudar no momento, mas claro, ele pode pedir um favor em troca.',

'Voz da razão: Todos os personagens param de lutar, para escutar o herói falar por pelo menos 30 segundos. Só se pode fazer ações defensivas nesse período, e criaturas que não compreendem o herói, não são afetadas por essa carta.',

'Monólogo vilanesco: O vilão perde seu próximo turno falando seu plano diabólico.',

'Corridão: A distância da viagem é reduzida pela metade, ou o personagem dobra sua movimentação durante 1d6 turnos.',

'Saldão: Seu herói consegue um item genérico de sua escolha(como sucateiro).',

'Entregando o jogo: Sucesso automático em persuasão, intimidação ou outra forma de conseguir informação.',

'Epifania: Tenha um d6 em qualquer perícia que não tinha antes até o final da sessão(se a sessão for dividida em dois, este permanece)',

'Esforço extra: Adicione +1d6 em qualquer rolagem para cada bene que seu personagem possua nesta sessão.',

'Fica a dica: O mestre responde algo, ou dá alguma dica ou informação importante para o personagem.',

'Uma alma por outra: Evita a morte, captura ou outra situação ruim para você ou um aliado, mas isso leva a um novo problema, determinado pelo mestre',

'Herói popular: Após salvar um grupo de pessoas, a comunidade local adota você e seu grupo como heróis locais e sempre oferecerá ajuda.',

'Hoje não: Ao jogar essa carta, um ataque de alguém é considerado automaticamente como uma falha crítica.',

'Hora da revolta: +2 em ações contra um personagem até o fim do dia.',

'Hora do sangue: Nenhum personagem pode absorver dano(poderes não contam) até que um coringa seja sacado nesse combate.',

'Inimigo: Jogue no começo da sessão. Um personagem da escolha do mestre vira inimigo jurado do seu personagem. Você não pode absorver danos contra ele. A partir de agora, compre duas cartas de aventura(pode usar 2 por sessão) até que o vilão seja derrotado.',

'Check point: Recupere todos seus EQ imediatamente',

'Inspiração: Todos da sua equipe recebem +2 para rolagens de características até o fim da rodada.',

'Interesse amoroso: Jogue em um extra. Isso encoraja um interesse romântico, esse personagem pode ajudar, mas também pode causar problemas com frequência, pela sua inocência ou incompetência.',

'Fúria: Após receber um Ferimento, jogue essa carta e cause +2 de dano em seus ataques, para cada Ferimento que receber, até o fim da cena.',

'Levantar a moral: Recupera todos seus aliados do estado Abalado, Vulnerável, Distraído e estados de complicações menores, depois de um discurso, se o discurso for muito bom, recupera um Ferimento.',

'Sorte grande: Tire mais duas cartas do Baralho e escolha uma.',

'Touché: Jogue após serem surpreendidos, isso anula a surpresa e todos compram cartas de iniciativa normalmente.',

'Fortuna: Ao lotear algo ou alguém, jogue essa carta e encontre tudo que pode ser encontrado.',

'Mal funcionamento: Causa um mau funcionamento ou quebra em algum equipamento(invento também conta), consertar é uma rolagem de reparo-4 e com 10 minutos.',

'Multidão enfurecida: Durante um combate, uma multidão armada(2 por personagem da party) entra no combate e ajuda os heróis.',

'Na hora certa: Gaste um bene e escolha uma carta no baralho de aventura, você pode jogar uma carta extra nesta sessão.',

'OOHHH!: Um inimigo determinado pelo mestre tem seu tamanho e Força aumentado em 2, e todos os aliados compram 1 carta de aventura. Players podem usar 2 cartas essa sessão',

'Paz: Melhora a atitude de um grupo, por conhecer alguém no meio, mostrar respeito ou apenas persuadi-los a não serem ofensivos. Não funciona em vilões maiorais',

'Reanimar: Levanta todos os aliados extras imediatamente sem Ferimentos.',

'Reforços: Reforços inimigos chegam(quantos e como fica a critério do mestre) e todos os aliados compram uma carta extra e podem jogar mais uma nesta sessão.',

'Save point: Depois de 30 minutos ininterruptos, jogue essa carta e considere como se o personagem tivesse tido uma noite completa, restaurando todo seu EQ e suas Fadigas',

'Revelação: Durante uma pesquisa, seu herói descobre tudo que há para ser descoberto, ou absorve uma informação importante sobre o assunto.',

'Segundo vento: Cura automaticamente todos os Ferimentos e Fadigas do personagem',

'Selvageria: Ganha uma vantagem qualquer de sua escolha, sem ter que obedecer requisitos pelo resto da sessão.',

'Assassino nato: Durante 1d4 turnos, você age como se tivesse tirado um coringa.',

'Surto de adrenalina: Ganha um turno extra quando decidir usar.',

'Trabalho em equipe: Seu herói e quaisquer personagens adjacentes fazem um ataque em conjunto, com +4 cada.',

'Vestido para matar: Adicione +4 em seu carisma durante essa sessão, pois seu personagem está vestido muito bem ou está a caráter na ocasião.',

'Vira casaca: Convence um inimigo(menor) a fazer alguma coisa para lhe ajudar.',

'Você não disse isso: Durante um combate, diga algo intenso e amedrontador, que nunca deveria ser dito. Todos, sem exceção, ficam Abalados.(menos você)',

'Agrupar em equipe: Todos a 5 quadros, de você(aliados), recebem +2 em Aparar e Resistência até que um coringa seja sacado no combate.',

'Relíquia: Ao saquear alguma área, ou em qualquer ocasião, seu herói encontra um item importantíssimo, com um passado misterioso e algum poder ou maldição atrelado.',

'Homenagem: Depois da morte de algum personagem, seu herói fala algumas palavras importantes, todos compram cartas novas e jogam 2 nesta sessão.',

'Espanto: Depois de falar alguma coisa, todos os inimigos em um raio de 10m perdem suas ações.',

'Ladrão: Roube um bene de qualquer Carta Selvagem.',

'Jeito difícil: Transforme todos os seus benes em XP nessa sessão(pode ser no começo)',

'Karma: Depois de fazer uma boa ação(o mestre decide se vale) recupere os benes de todos nesta sessão.',

'Comando: O bônus de ações de suporte são dobrados até o fim do combate.',

'Que barulho é esse?: Todos os players recebem uma carta extra, e podem jogar duas cartas essa sessão, mas em algum momento, alguma ameaça surgirá.',

'Reciclar: Escolha uma carta da pilha de descarte, para usá-la como carta extra(2 cartas na  sessão).',

'Ferro quente e whiskey: Recupera todos os Ferimentos de um personagem, mas o deixa com uma cicatriz horrível, que o deixa com -2 de Carisma por um mês no jogo.',

'Máfia: Uma gangue da máfia entra no combate, se eles são aliados ou não, o mestre diz.',

'Plus-ultra: O personagem pode usar QUALQUER poder do livro uma vez nesse combate, desde que faça sentido com sua individualidade',

'Apunhalada: Um aliado te trai, se aliando com seus inimigos ou contando seus segredos. Todos compram uma carta de aventura e recuperam seus benes.',

'Pacto escuro: Jogue depois de presenciar um evento estranho, ou conhecer alguma força da natureza ou sobrenatural. Você recebe a desvantagem “Má sorte”, mas tira e usa 2 cartas de aventura por sessão.',

'Intuição inesperada: Seu personagem consegue afetar(ataque ou outra ação contra) uma criatura com um ataque, independentemente das invulnerabilidades dela ou situação.'

] 
dealt_cards = []
descartadas = []
player_cards = {}
'''
usar atribuição para dicionário:
player_cards[player] = cartas
usar exec(f"{}")
'''
#funções: ----------------------------------------------------------------------------------
#funções: ----------------------------------------------------------------------------------
#funções: ----------------------------------------------------------------------------------

async def get_server(): #Retorna o objeto GUILD
    await client.wait_until_ready()
    server = client.get_guild(guild_id)
    return server

async def get_members(): #Retorna membros do objeto GUILD
    await client.wait_until_ready()
    server = await get_server()
    if not server:
        return
    members = server.members
    return members

async def embedar_e_mandar(interaction : discord.Interaction,card, cor, user): #pega uma string "carta" e divide ela nos ":", criando um embed com titulo e descrição, e recebe a cor, no formato color().COR
    parts = card.split(":")
    title = parts[0]
    description = parts[1]
    embedvar = discord.Embed(title=title, description= description, color=cor)
    embedvar.set_footer(text = "Carta de aventura")
    channel = interaction.channel
    if not isinstance (channel, discord.abc.Messageable):
        return # or send an error
    try:
        await user.send(embed = embedvar, view = Descartar())
    except Exception as e:
        try:            
            await channel.send(f"Não foi possível enviar uma carta para {user.mention}, \n{e}")
        except:
            channel = client.get_channel(1065721164657336370)
            if not isinstance (channel, discord.abc.Messageable):
                return # or send an error
            ptr = await client.fetch_user(286540943056830474)
            await channel.send(f"Não foi possível enviar uma carta para {user.mention}, {ptr.mention}, \n{e}")
            
    return 

async def deal_dm(interaction: discord.Interaction, user: discord.Member, cor):# Tira uma carta do baralho e mamnda para embedar_e_mandar()
    """Dá uma carta de aventura para um Player."""
    # Check if the deck is empty
    channel = interaction.channel
    if not isinstance (channel, discord.abc.Messageable):
                    return # or send an error
    if len(deck) == 0:
        await channel.send(f"As cartas acabaram, digite /retornar para voltar o baralho, {user.mention} ficou sem carta.")
        return 0
    # Deal a random card from the deck to the target user
    card = random.choice(deck)
    # Add the dealt card to the list of dealt cards
    dealt_cards.append(card)
    # Remove the dealt card from the deck
    deck.remove(card)
  
    # Separate title from descriprion and embed it
    await embedar_e_mandar(interaction, card,cor, user)
    return 1

async def deal_mestre(interaction : discord.Interaction, num_players: int):#Deal dm, mas para quem tiver o cargo "Mestre"
    members = await get_members()
    if not members:
        print("Server deu None")
        return
    for member in members:
        if discord.utils.get(member.roles, name="Mestres"):
            i = 0
            while i< num_players: 
                print("deal mestre")
                await deal_dm(interaction, member, colors().red)
                i+= 1
            if not isinstance(interaction.channel, discord.abc.Messageable):
                return
            await interaction.channel.send("Mestre recebeu a carta!")

async def is_owner(interaction : discord.Interaction):#Retorna True se o interaction.user for dono do server
    if interaction.user.id == 286540943056830474:
        return True
    else:
        return False

#Eventos:----------------------------------------------------------------------------------
#Eventos:----------------------------------------------------------------------------------
#Eventos:----------------------------------------------------------------------------------

@client.event
async def on_ready():
    print(f'Logged in as {client.user} (ID: {client.user})')
    print('------')
    print(discord.__version__)
    await client.change_presence(activity=discord.Game(name="BNHA"))
    client.add_view(MineView())
    client.add_view(Session())
    client.add_view(Descartar())
    channel = client.get_channel(1065721164657336370)
    if not isinstance(channel, discord.abc.Messageable):
        return
    ptr = await client.fetch_user(286540943056830474)
    await channel.send(f"Bot on {ptr.mention}", delete_after=5)
    
    
whitelist = [1047320746453643344]
@client.event #whitelist bot
async def on_guild_join(guild):
    if guild.id not in whitelist:
        channel = guild.text_channels[0]
        await channel.send("Saindo do server porque não está na whitelist.")
        await guild.leave()
        print(f"Left {guild.name} because it's not on the whitelist.")


@client.event
async def on_scheduled_event_create(event):
    data = event.start_time
    await asyncio.sleep((data - datetime.now()).total_seconds())
    channel = await client.fetch_channel(1047320748529811499)
    if not isinstance(channel, discord.abc.Messageable):
        return
    await channel.send("Sessão começando! @here")
#Context menus: ----------------------------------------------------------------------------------
#Context menus: ----------------------------------------------------------------------------------
#Context menus: ----------------------------------------------------------------------------------
'''Context menu /deal'''
@client.tree.context_menu(name='Cartear com aventura') #Context menu para dar cartas a um player específico
async def deal_menu(interaction: discord.Interaction, user: discord.Member):
    '''Dar carta de aventura'''
    await deal_dm(interaction,user, colors().blue)
    await interaction.response.send_message(f"{user.mention} recebeu uma carta!", delete_after=1)


'''buttons'''
class Descartar(discord.ui.View):#Botão de descartar carta 
    """Descarta a carta da mensagem"""
    @discord.ui.button(label="Descartar", style=discord.ButtonStyle.primary)
    async def button_callback(self,  interaction, button):
        embed = interaction.message.embeds
        title = embed[0].title
        descartadas.append(title)
        await interaction.message.delete() 
        channel = client.get_channel(1065721164657336370)
        if not isinstance(channel, discord.abc.Messageable):
            return
        await channel.send(f"{interaction.user.mention} descartou uma carta!")
        

class Session(discord.ui.View): # Server Mine
    """Botões para o /sessão"""
    def __init__(self)-> None:
        super().__init__(timeout = None)
   
    @discord.ui.button(label="Posso participar!",custom_id = "Confirmado", style=discord.ButtonStyle.green) 
    async def button_callback1(self, interaction, button):
        #Pega as variáveis
        embed = interaction.message.embeds[0]
        nome = embed.description
        sessão = embed.title
        channel = await client.fetch_channel(1047641289451130880) 
        if not isinstance(channel, discord.abc.Messageable):
           return
        members = await get_members()
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
            if member.id == 286540943056830474:
                await member.send(f"{interaction.user.mention} confirmou disponibilidade para: ", embed = embed)
                
        
        #procura no canal mensagens que tenham o mesmo título de sessão
        async for msg in channel.history(limit=None): 
            if not (len(msg.embeds) == 0):
                #pega os embeds da mensagem
                embeds = msg.embeds
                #procura nome da sessão no embed da mensagem
                if nome in embeds[0].description:
                    #pega o embed da mensagem
                    embed = embeds[0] 
                    confirmados = embed.fields[3].value
                    #checa se o membro foi mencionado na aba de confirmados
                    if not (interaction.user.mention in confirmados):
                        confirmados = embed.fields[3].value + interaction.user.mention + ";"
                        embed.set_field_at(3, name=embed.fields[3].name, value=confirmados)
                        await msg.edit(content = "", embed = embed)
                    
                    #tira o nome do fi da lista de desconfirmados, caso ele esteja la
                    try:
                        desconfirmados = embed.fields[4].value
                        if desconfirmados:
                            if (interaction.user.mention in desconfirmados):
                                desconfirmados = desconfirmados.strip(interaction.user.mention + ";")
                                embed.set_field_at(4, name=embed.fields[3].name, value=desconfirmados)
                                if desconfirmados == "":
                                    embed.remove_field(index=4)
                                    if client.user:
                                        await msg.remove_reaction(member = client.user,emoji="❌")
                                await msg.edit(content = "", embed = embed)
                    except Exception as e:
                        print(e)
                    
                        
                    players = embed.fields[2].value
                    mem = embed.fields[3].value
                    #checa se todos os players podem, e da verdinho na mensagem
                    if not (players == None or mem == None):
                        players_total = len(players.split(","))
                        n_players = len(mem.split(";")[:-1])
                        embed.set_field_at(3, name=f"Confirmados: ({n_players}/{players_total})", value=embed.fields[3].value)
                        await msg.edit(content = "", embed = embed)
                        porcent:float = n_players/players_total
                        if porcent >= 1:
                            embed.color = colors().green
                            embed.title = (sessão + "\nSessão confirmada!:white_check_mark:")
                            await msg.edit(content = "", embed = embed)
                            await msg.add_reaction("✅")
                    
                
        
    @discord.ui.button(label="Não posso participar :(",custom_id = "Não confirmado", style=discord.ButtonStyle.red) 
    async def button_callback2(self, interaction, button):
        #pega variáveis
        embed = interaction.message.embeds[0]
        nome = embed.description
        channel = await client.fetch_channel(1047641289451130880) 
        if not isinstance(channel, discord.abc.Messageable):
           return
        members = await get_members()
        if not members:
            return
        
        #Habilita o botão vermelho e desabilita o verde
        for child in self.children: 
            child.disabled = False # type: ignore
            child.label = "Posso participar!" # type: ignore
            child.emoji = None # type: ignore
        button.disabled = True 
        button.label = "Presença não confirmada :(" 
        await interaction.response.edit_message(view=self) 
        
        #responde a interação
        await interaction.user.send("Presença não confirmada :(")
        
        # manda para o mestre a disponibilidade
        for member in members: 
            if discord.utils.get(member.roles, name="Mestres"):
                await member.send(f"{interaction.user.mention} não tem disponibilidade para:", embed = embed)
            if member.id == 286540943056830474:
                await member.send(f"{interaction.user.mention} confirmou disponibilidade para: ", embed = embed)
        
        #edita a mensagem original
        async for msg in channel.history(limit=None): 
            if not (len(msg.embeds) == 0):
                embed = msg.embeds[0]
                confirmados_old = embed.fields[3].value
                if not confirmados_old:
                    return
                confirmados = confirmados_old.split(";")[:-1]
                
                #checa se o nome da sessão está na mensagem
                if nome == embed.description:
                    if interaction.user.mention in embed.fields[3].value:
                        confirmados_new = [m for m in confirmados if m.strip() != interaction.user.mention] #nova lista de confirmados
                        confirmados = ""
                        confirmados = ";".join(confirmados_new)+";" #faz a string separando por ";"
                        if confirmados == ";":
                            confirmados = ""
                        
                        #faz o novo embed com confirmados
                        embed.set_field_at(3, name=embed.fields[3].name, value=confirmados)
                        players_total = embed.fields[2].value
                        list = embed.fields[3].value
                        n_players = 0
                        if not (players_total == None or list == None):
                            players_total = len(players_total.split(","))
                            n_players = len(list.split(";")[:-1])
                        embed.set_field_at(3, name=f"Confirmados: ({n_players}/{players_total})", value=confirmados)                        
                        title = embed.title
                        if not title:
                            return
                        if title.find("Sessão confirmada!")!=-1:
                            aux = title.split("\n")
                            title = aux[0]
                            embed.title = title
                            embed.color = colors().dark_orange
                            if not client.user:
                                return
                            await msg.remove_reaction(member=client.user, emoji="✅")

                        try:
                            desconfirmados = embed.fields[4].value
                            if not (interaction.user.mention in desconfirmados):
                                desconfirmados = embed.fields[4].value + interaction.user.mention + ";"
                                embed.set_field_at(4, name=embed.fields[3].name, value=desconfirmados)
                                await msg.edit(content = "", embed = embed)
                                
                        except:
                            embed.add_field(name=f"Não pode(m):", value=f"{interaction.user.mention};", inline= False)
                    
                        #edita a msg
                        embed.color= colors().dark_red
                        await msg.add_reaction("❌")
                        await msg.edit(content = "", embed = embed)       
        
''' quando um evento for começar, starta ele
    quando começar evento, amndar mensagem em algum canal'''
                        
'''Evento que escuta mensagens dentro da dm do bot para comandos la dentro'''
#comandos: ----------------------------------------------------------------------------------
#comandos: ----------------------------------------------------------------------------------
#comandos: ----------------------------------------------------------------------------------

'''/deal''' #Manda uma carta na DM do Player
@client.tree.command()
@app_commands.rename(user='player')
@app_commands.describe( #options 
    user='Player para receber a carta na DM'
)
async def deal(interaction: discord.Interaction, user: discord.Member):
    """Dá uma carta de aventura para um Player."""
    flag = await deal_dm(interaction,user, colors().blue)
    if flag == 1:
        await interaction.response.send_message(f"{user.mention} recebeu uma carta!",delete_after=1)
    else:
        return



'''/deal_all'''#Dá uma carta para cada player que está online no voice do rpg, e tem o role "Jogadores"
@client.tree.command()
async def deal_all(interaction: discord.Interaction):
    """Distribui uma carta de aventura para todos os Players no voice, e para o Mestre"""
    voice_channel = client.get_channel(1047320748529811500)
    if not isinstance(voice_channel, discord.VoiceChannel):
        return
    players = [member for member in voice_channel.members]
    flag = 0
    num_players = 0
    for player in players:
        if discord.utils.get(player.roles, name="Jogadores") is not None:
            await deal_dm(interaction, player, colors().blue)
            flag = 1
            num_players+=1
    if flag == 0:
        await interaction.response.send_message("Nenhum player conectado no canal de voz")
    else:
        await interaction.response.send_message("Todos os players(e mestre) receberam cartas.", delete_after=1)
    await deal_mestre(interaction, num_players)



'''/shuffle''' #Embaralha as cartas que estão no baralho
@client.tree.command()
async def shuffle(interaction : discord.Interaction):
    '''Embaralha as cartas que estão no baralho'''
    random.shuffle(deck)
    await interaction.response.send_message("Baralho embaralhado")



'''/retornar''' #Retorna as cartas para o baralho
@client.tree.command()
async def retornar(interaction : discord.Interaction):
    '''Retornar todas as cartas para o Baralho e embaralha.'''
    members = await get_members()
    if not members: 
        return
    for member in members:
        try:
            async for message in member.history(limit = None):
                if message.author == client.user:
                    try:
                        footer = message.embeds[0]
                        if not(footer.find("Carta de aventura") == -1): #type: ignore
                            await message.delete()
                            print("Mensagem deletada")
                    except:
                        await message.delete()
                        print("Mensagem deletada")
        except Exception as e:
            print(f"Não foi possível deletar as cartas de: {member} /n {e}")
    
    # Add all dealt cards back to the deck
    deck.extend(dealt_cards)

    # Clear the list of dealt cards
    dealt_cards.clear()
    descartadas.clear()
    random.shuffle(deck)
    await interaction.response.send_message("Baralho retornado e embaralhado")



'''/carta [Nome da carta para pesquisar]''' #Pesquisa no baralho uma carta com um nome [nome] e manda embeds de todas as cartas que contém aqueles termos em suas palavras
@client.tree.command()
@app_commands.describe( #options 
    nome='Nome da carta'
)
async def carta(interaction : discord.Interaction, nome : str):
    '''Pesquisa no baralho as cartas que contenham os termos pesquisados.'''
    whole_deck = deck + dealt_cards
    result = []
    flag = 0
    channel = interaction.channel
    if not isinstance (channel, discord.abc.Messageable):
        return # or send an error
    await interaction.response.send_message("Buscando cartas com os termos desejados..." , delete_after=5)
    for term in whole_deck: # busca no deck alguma carta que contenha os elementos de "term"
      if nome.lower() in (term.lower()) :
        result = term
        parts = result.split(":")
        title = parts[0]
        desc = parts[1]
        embedvar = discord.Embed(title = title, description = desc, color = colors().green)
        await channel.send(embed = embedvar)
        flag = 1
    if flag == 0:
        await channel.send("Nenhuma carta foi encontrada com esse termo, tente novamente com um termo diferente.")
    else:
        await channel.send("Todas as cartas encontradas foram mostradas.")



'''/descartes''' #Responde com uma lista com os nomes das cartas que foram descartadas 
@client.tree.command()
async def descartes(interaction: discord.Interaction):
    '''Mostra a pilha de cartas descartadas.'''
    cartas = []
    for card in descartadas:
      name = card
      cartas.append(name)
    array_string = "-"
    array_string = "-"+"\n- ".join(cartas)
    embedvar = discord.Embed(title = "Pilha de descartes", description = array_string)
    await interaction.response.send_message(embed = embedvar)



'''/dmpurgeall''' #Deleta todas as msgs da dm de todos os players
@client.tree.command()
@app_commands.check(is_owner)
async def dmpurgeall(interaction: discord.Interaction):
    """Deleta todas as mensagens do bot em todas as DMs"""
    server = client.guilds[0]
    members = server.members
    await interaction.response.send_message("DMs sendo purjadas!", delete_after= 1)
    print(f"Purjando dm dos membros")
    for member in members:
        try:
            async for message in member.history(limit = None):
                if message.author == client.user:
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
    if not isinstance (interaction.channel, discord.abc.Messageable):
        return
    await interaction.channel.send("Todas as DMs foram purjadas!:D")



'''/dmpurge [Player]'''#Deleta todas as msgs da dm de um player
@client.tree.command()
@app_commands.check(is_owner)
async def dmpurge(interaction: discord.Interaction, user : discord.Member):
    """Deleta todas as mensagens do bot na DM de um Player específico"""
    channel = interaction.channel
    if not isinstance (channel, discord.abc.Messageable):
            return # or send an error
    try:
            await interaction.response.send_message("Purjando")
            async for message in user.history(limit = None):
                if message.author == client.user:
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



'''/holocausto''' #Deleta todas as mensagens enviadas pelo bot em um canal
@client.tree.command()
@app_commands.check(is_owner)
async def holocausto(interaction: discord.Interaction, channel : discord.TextChannel):
    """Deleta todas as mensagens do bot de um canal de texto específico"""
    if not isinstance (channel, discord.abc.Messageable):
            return # or send an error
    await interaction.response.send_message("Purjando", delete_after=1)
    async for message in channel.history(limit = None):
        await message.delete()  
        ''' if message.author == client.user:
            await message.delete()'''
    await channel.send("Purjado", delete_after = 1)
    
     
           
'''/teste''' #Teste
@client.tree.command()
@app_commands.check(is_owner)
async def teste(interaction: discord.Interaction):
    """TESTE"""
    await interaction.response.send_message("Teste")



'''/restart''' #Teste
@client.tree.command()
@app_commands.check(is_owner)
async def restart(interaction: discord.Interaction):
    """Reiniciar bot"""
    await interaction.response.send_message("Reiniciando o bot...")
    os.execv(sys.executable, ['python'] + sys.argv)
    
    
    
'''/stop''' #Teste
@client.tree.command()
@app_commands.check(is_owner)
async def stop(interaction: discord.Interaction):
    """Desligar o bot"""
    await interaction.response.send_message("Desligando o bot...")
    await client.close()



'''/dmpurgeallall''' #Deleta todas as msgs da dm de todos os players(todas mesmo)
@client.tree.command()
@app_commands.check(is_owner)
async def dmpurgeallall(interaction: discord.Interaction):
    """Deleta todas as mensagens do bot em todas as DMs"""
    server = client.guilds[0]
    members = server.members
    await interaction.response.send_message("DMs sendo purjadas!", delete_after= 1)
    print(f"Purjando dm dos membros")
    for member in members:
        try:
            async for message in member.history(limit = None):
                if message.author == client.user:
                
                            await message.delete()
                            print("Mensagem deletada")
        except Exception as e:
            print(f"Não foi possível purjar: {member} /n {e}")
    if not isinstance (interaction.channel, discord.abc.Messageable):
        return
    await interaction.channel.send("Todas as DMs foram purjadas!:D")



'''/sessão'''
@client.hybrid_command()
@app_commands.rename(members='players')
@app_commands.describe( 
    numero_da_sessão='Número da sessão, como 0, 0.1, 1, 2, etc',
    tipo_de_sessão = 'Emoji referente ao tipo de sessão(copie e cole do catálogo). Ex.(Sessão principal):🎮',
    nome = 'Nome da sessão. Ex.: A morte de Freeza',
    data = 'Data que a sessão ocorrerá. Ex.: 28/02',
    horário = 'Horário da sessão. Ex.: 18:00',
    members = 'Players que jogarão a sessão, como menções. Ex.: @Pendragon'
)
async def sessão(ctx: commands.Context, numero_da_sessão: str,tipo_de_sessão: str, nome:str, data : str,horário: str, members: commands.Greedy[discord.Member]):
    #Pegando variáveis
    players = ""
    for player in members:
        players += player.mention + ", "
    players = players[:-2] + "."
    n_players = len(members)
    
    #criando o embed
    embed = discord.Embed(title=f"Sessão {numero_da_sessão}({tipo_de_sessão})", description=f'"||{nome}||"', color = colors().teal)
    embed.add_field(name="Data:",value=data, inline=False)
    embed.add_field(name="Horário:",value=horário, inline=False)
    embed.add_field(name="Players: ",value=players, inline=False)
    embed.add_field(name = f"Confirmados: (0/{n_players})", value = "", inline=False)
    
    #mandando msg no canal
    message = await ctx.reply(f"{players}", embed = embed)
    await message.edit(content=None,embed=embed)
    
    #mensagem para cada player na sessão, com botões
    for player in members:
        try:
            embed.remove_field(index=3) #Tira o campo "Confirmados"
            embed.set_footer(text = "tuuty")
            await player.send(f"{player.mention}",embed=embed, view= Session())
        except Exception as e:
            await ctx.channel.send(f"{player} não recebeu notificação na Dm, \n {e}")
    
    #criando o evento
    aux = data.split("/")
    data = aux[1] + "/" + aux[0] +"/2023 "+horário+":00"
    brasil = timezone('Brazil/east')
    data_object = brasil.localize(datetime.utcnow().strptime(data, '%m/%d/%Y %H:%M:%S'))
    guild = await client.fetch_guild(guild_id)
    
    if not embed.title:
        return
    sessão = embed.title
    await guild.create_scheduled_event(name= sessão, start_time=data_object, channel=client.get_channel(1047320748529811500), description=(f"'||{nome}||' \nPlayers: {players}"))


            
@client.hybrid_command()
async def roll(ctx, dice: str):
    """Rolls a dice in NdN format and explodes on critical rolls."""
    try:
        rolls, limit = map(int, dice.split('d'))
        if rolls > 10:
            await ctx.send('I can only roll up to 10 dice at a time.')
            return
    except Exception:
        await ctx.send('Format has to be in NdN!')
        return

    result = []
    crit = []
    total = 0

    for r in range(rolls):
        roll = limit
        if roll == limit:
            crit.append(roll)
            while roll == limit:
                roll = random.randint(1, limit)
                crit.append(roll)
        result.append(roll)
        total += roll

    if crit:
        crit_string = ' '.join(str(i) for i in crit)
        await ctx.send(f'Critical! You rolled {crit_string}! Roll again to add to your total.')
    else:
        await ctx.send(f'You rolled {result} for a total of {total}.')





client.run(TOKEN)   


"""Fazer: 
    -Comando /Server com botão persistente
    -Comando /Mapa
    -Retornar: deleta as cartas da dm de todos
    -tirar a msg de sessões dos dmpurges
    -/Sessao : tem o nome da sessao como titulo, a descricao sao os players, e manda na dm de cada um dizendo os detalhes da sessao, com um botao de confirmar e um de nao posso. ele tem botoes persistentes e salva o id das mensagens, quando clicado, ele edita a msg, colocando um check do lado do player que confirmou, e manda  pro mestre e pra mim. no dmpurge, impedir de deletar essas msgs(colocar no if (se conter tuuty no author da msg, n apaga))
    -;restart na dm
    -quando um evento começar, trocar canal Sessão = On verde
    """