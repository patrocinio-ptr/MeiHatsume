import discord
import random
from discord import app_commands
from discord.ext import commands
from utility import guild_id, MY_GUILD, colors, update_events, get_members, get_server #type:ignore
from typing import Union

deck = [
'Inimigo: Jogue no começo da sessão. Um personagem da escolha do mestre vira inimigo jurado do seu personagem. Você não pode absorver danos contra ele. A partir de agora, compre duas cartas de aventura(pode usar 2 por sessão) até que o vilão seja derrotado.',

'Pacto escuro: Jogue depois de presenciar um evento estranho, ou conhecer alguma força da natureza ou sobrenatural. Você recebe a desvantagem “Má sorte”, mas tira e usa 1 carta extra de aventura por sessão.',

'Sorte grande: Tire mais duas cartas do Baralho e escolha uma.',

'Na hora certa: Gaste um bene e escolha uma carta no baralho de aventura, você pode jogar uma carta extra nesta sessão.',

'Jeito difícil: Transforme todos os seus benes em XP nessa sessão(tem que  ser no começo, e pode ser usada apenas uma vez por estágio, se tirá-la novamente, pegue outra carta)',

'Relíquia: Ao saquear alguma área, ou em qualquer ocasião, seu herói encontra um item importantíssimo, com um passado misterioso e algum poder ou maldição atrelado.',

'Fica a dica: O mestre responde algo, ou dá alguma dica ou informação importante para o personagem, durante a sessão, o ajudando quando precisar.',

'Watashi Ga Kita: A ajuda chega à cena vinda de alguma fonte determinada pelo mestre.',

'Contatos: Seu personagem encontra um velho amigo/conhecido, que pode lhe ajudar no momento, mas claro, ele pode pedir um favor em troca.',

'Vira casaca: Convence um inimigo(menor) a fazer alguma coisa para lhe ajudar.',

'Segundo vento: Cura automaticamente todos os Ferimentos, Fadigas e condições do personagem',

'Uma alma por outra: Evita a morte, captura ou outra situação ruim para você ou um aliado, mas isso leva a um novo problema, determinado pelo mestre.',

'Exceder poder: Dobra o dano de um ataque(precisa ser um poder), sem gastar EQ, mas faz um teste de Vigor-2, ou sofre um nível de Fadiga.',

'Esforço extra: Adicione +1d6 em qualquer rolagem para cada bene que seu personagem possua(incluindo os gastos) nesta sessão.',

'Fúria: Jogue essa carta e ganhe +2 em tudo, até o fim da cena, ou um Coringa aparecer.',

'Hoje não: Ao jogar essa carta, um ataque de alguém é considerado automaticamente como uma falha crítica.',

'Tankei foi tudo: Nega o dano total de um ataque.',

'Ás: Em vez de rolar um teste, considere uma ampliação automática.',

'Agrupar em equipe: Todos a 5 quadros, de você(aliados), recebem +2 em Aparar e em Resistência até que um coringa seja sacado no combate.',

'Hora do sangue: Nenhum personagem pode absorver dano(poderes não contam) até que um coringa seja sacado nesse combate.',

'Assassino nato: Durante 1d4 turnos, você age como se tivesse tirado um coringa.',

'Levantar a moral: Recupera todos seus aliados do estado Abalado, Vulnerável, Distraído e estados de complicações menores, depois de um discurso, se o discurso for muito bom, recupera um Ferimento ou Fadiga.',

'Inspiração: Todos da sua equipe recebem +2 para rolagens de características até o fim da rodada.',

'Antes você do que eu: Ao receber um ataque, jogue esta carta, e um personagem adjacente a você receberá o ataque em seu lugar.',

'Surto de adrenalina: Ganha um turno extra quando decidir usar., e age imediatamente(pode interromper ação de outros)',

'Boa fama: Ganhe +1 de carisma permanente após fazer uma boa ação.',

'Plus-ultra: O personagem pode usar QUALQUER poder do livro uma vez nesse combate, desde que faça sentido com sua individualidade',

'Voz da razão: Todos os personagens param de lutar, para escutar o herói falar por pelo menos 30 segundos. Só se pode fazer ações defensivas nesse período, e criaturas que não compreendem o herói, não são afetadas por essa carta.',

'Espanto: Depois de falar alguma coisa, todos os inimigos em um raio de 10m perdem suas ações.',

'Monólogo vilanesco: O vilão perde seu próximo turno falando seu plano diabólico.',

'Reciclar: Escolha uma carta da pilha de descarte, para usá-la como carta extra(2 cartas na  sessão).',

'Trabalho em equipe: Seu herói e quaisquer personagens adjacentes fazem um ataque em conjunto, com +4 cada.',

'Corridão: A distância da viagem é reduzida pela metade, ou o personagem dobra sua movimentação durante 1d6 turnos.',

'Saldão: Seu herói consegue um item genérico de sua escolha(como sucateiro, mas sem limite de tamanho).',

'Ao estilo russo: Jogue essa carta após se recuperar de um teste de morte. Você não sofre lesões, mas ainda está inconsciente.',

'Entregando o jogo: Sucesso automático em persuasão, intimidação ou outra forma de conseguir informação.',

'Epifania: Tenha um d6 em qualquer perícia que não tinha antes até o final da sessão(se a sessão for dividida em dois, este permanece)',

'Herói popular: Após salvar um grupo de pessoas, a comunidade local adota você e seu grupo como heróis locais e sempre oferecerá ajuda.',

'Hora da revolta: +2 em ações contra um personagem até o fim do dia.',

'Check point: Recupere todos seus EQ imediatamente',

'Interesse amoroso: Jogue em um extra. Isso encoraja um interesse romântico, esse personagem pode ajudar, mas também pode causar problemas com frequência, pela sua inocência ou incompetência.',

'Touché: Jogue após serem surpreendidos, isso anula a surpresa e todos compram cartas de iniciativa normalmente.',

'Fortuna: Ao lotear algo ou alguém, jogue essa carta e encontre tudo que pode ser encontrado.',

'Mal funcionamento: Causa um mau funcionamento ou quebra em algum equipamento(invento também conta), consertar é uma rolagem de reparo-4 e com 10 minutos.',

'Multidão enfurecida: Durante um combate, uma multidão armada(2 por personagem da party) entra no combate e ajuda os heróis.',

'OOHHH!: Um inimigo determinado pelo mestre tem seu tamanho e Força aumentado em 2, e todos os aliados compram 1 carta de aventura. Players podem usar 2 cartas essa sessão',

'Paz: Melhora a atitude de um grupo, por conhecer alguém no meio, mostrar respeito ou apenas persuadi-los a não serem ofensivos. Não funciona em vilões maiorais',

'Reanimar: Levanta todos os aliados extras imediatamente sem Ferimentos.',

'Reforços: Reforços inimigos chegam(quantos e como fica a critério do mestre) e todos os aliados compram uma carta extra e podem jogar mais uma nesta sessão.',

'Save point: Depois de 30 minutos ininterruptos, jogue essa carta e considere como se o personagem tivesse tido uma noite completa, restaurando todo seu EQ e suas Fadigas',

'Revelação: Durante uma pesquisa, seu herói descobre tudo que há para ser descoberto, ou absorve uma informação importante sobre o assunto.',

'Selvageria: Ganha uma vantagem qualquer de sua escolha, sem ter que obedecer requisitos pelo resto da sessão.',

'Vestido para matar: Adicione +4 em seu carisma durante essa sessão, pois seu personagem está vestido muito bem ou está a caráter na ocasião.',

'Você não disse isso: Durante um combate, diga algo intenso e amedrontador, que nunca deveria ser dito. Todos, sem exceção, ficam Abalados.(menos você)',

'Homenagem: Depois da morte de algum personagem, seu herói fala algumas palavras importantes, todos compram cartas novas e jogam 2 nesta sessão.',

'Ladrão: Roube 2 benes de qualquer Carta Selvagem.',

'Karma: Depois de fazer uma boa ação(o mestre decide se vale) recupere os benes de todos nesta sessão.',

'Comando: O bônus de ações de suporte são dobrados até o fim do combate.',

'Que barulho é esse?: Todos os players recebem uma carta extra, e podem jogar duas cartas essa sessão, mas em algum momento, alguma ameaça surgirá.',

'Ferro quente e whiskey: Recupera todos os Ferimentos de um personagem, mas o deixa com uma cicatriz horrível, que o deixa com -2 de Carisma por um mês no jogo.',

'Máfia: Uma gangue da máfia entra no combate, se eles são aliados ou não, o mestre diz.',

'Apunhalada: Um aliado te trai, se aliando com seus inimigos ou contando seus segredos. Todos compram uma carta de aventura e recuperam seus benes.',

'Intuição inesperada: Seu personagem consegue afetar(ataque ou outra ação contra) uma criatura com um ataque, independentemente das invulnerabilidades dela ou situação.',

'Visão do Futuro: Durante um momento crucial, seu personagem recebe uma visão do futuro que pode ajudá-lo a evitar um desastre iminente ou a tomar uma decisão estratégica.',

'Chuva de Ouro: Um dia de fortuna encobre a sua equipe, concedendo a cada personagem uma recompensa valiosa, como itens mágicos, ouro, ou conhecimento.',

'Segredo Obscuro: Um segredo profundo sobre um dos personagens é revelado, levando a conflitos internos e externos. No entanto, a revelação também pode fornecer insights valiosos ou vantagens.',

'Roleta da Profissão: Ao final da sessão, o personagem ganha +1 em uma perícia aleatória(ou determinada pelo mestre, se assim ele decidir)',

'Está chovendo sorte?:  Ao jogar esta carta no começo da sessão, todos os personagens da equipe ganham 1 bene extra.',

'Brutalidade Brutal:  Ao jogar esta carta, seus inimigos não podem gastar benes durante a cena atual, ou até um coringa ser sacado',] 
dealt_cards = []
descartadas = []
player_cards = {
}
'''
usar atribuição para dicionário:
player_cards[player] = cartas
usar exec(f"{}")
descartar tira a carta desse dict
'''

        
#Classe:--------------------------------------------------------------------------------
#Classe:--------------------------------------------------------------------------------
#Classe:--------------------------------------------------------------------------------
class Baralho_de_aventura(commands.Cog):
    def __init__(self, client: commands.Bot) :
        self.client = client
        self.ctx_menu = app_commands.ContextMenu(name='Cartear com aventura',callback=self.deal_menu)
        self.client.tree.add_command(self.ctx_menu) # add the context menu to the tree
    
    
    #Eventos: ----------------------------------------------------------------
    #Eventos: ----------------------------------------------------------------
    #Eventos: ----------------------------------------------------------------
    @commands.Cog.listener() #Manda cartas de aventura para todos que estão na sessão, assim que ela começar
    async def on_scheduled_event_update(self, event, new_event):
        if (event.status == discord.EventStatus.scheduled) and (new_event.status == discord.EventStatus.active):
            parts = event.description.split("Players:")
            players = parts[1]
            players = players.split(",")
            new_players = []
            for player in players:#Refazendo a lista de menções em player ids
                player = player.replace(" ", "").replace(".", "")
                new_players.append(player)
            
            players = [discord.utils.get(self.client.get_all_members(), id=int(m[2:-1])) for m in new_players]
            for player in players: #mandando cartas para os players
                if not player:
                    return
                await player.send(f"Sua carta de aventura para a {new_event.name} é:")
                await self.deal_dm(interaction= None, user= player, cor=colors().blue)
            for i in range(len(players)/2):
                await self.deal_mestre(None, 1)
        

    #Context menus: ----------------------------------------------------------------
    #Context menus: ----------------------------------------------------------------
    #Context menus: ----------------------------------------------------------------
    
    '''Context menu /deal''' #Context menu para dar cartas a um player específico
    async def deal_menu(self,interaction: discord.Interaction, user: discord.Member):
        '''Dar carta de aventura'''
        await self.deal_dm(interaction,user, colors().blue)
        await interaction.response.send_message(f"{user.mention} recebeu uma carta!", delete_after=1)

    #Funções:------------------------------------------------------------------------
    #Funções:------------------------------------------------------------------------
    #Funções:------------------------------------------------------------------------
    async def embedar_e_mandar(self, interaction:Union[discord.Interaction, None],card, cor, user): #pega uma string "carta" e divide ela nos ":", criando um embed com titulo e descrição, e recebe a cor, no formato color().COR
        parts = card.split(":")
        title = parts[0]
        description = parts[1]
        embedvar = discord.Embed(title=title, description= description, color=cor)
        embedvar.set_footer(text = "Carta de aventura")
        if interaction != None:
            channel = interaction.channel
            if not isinstance (channel, discord.abc.Messageable):
                return # or send an error
        else:
            channel = await self.client.fetch_channel(1065721164657336370)
            if not isinstance (channel, discord.abc.Messageable):
                return # or send an error
        try:
            await user.send(embed = embedvar, view = Descartar())
            print(f"Player: {user.name} recebeu carta: {title}:{description}")
            try:
                player_cards[user].append(title)
            except:
                player_cards[user] = []
                player_cards[user].append(title)
            
        except Exception as e: #mensagens de erro
            try:            
                print(f"Não foi possível enviar uma carta para {user.name}, \n{e}")
                await channel.send(f"Não foi possível enviar uma carta para {user.mention}, \n{e}")
            except:
                channel = self.client.get_channel(1065721164657336370)
                if not isinstance (channel, discord.abc.Messageable):
                    return # or send an error
                ptr = await self.client.fetch_user(286540943056830474)
                await channel.send(f"Não foi possível enviar uma carta para {user.mention}, {ptr.mention}, \n{e}")
                
        return 

    async def deal_dm(self, interaction:Union[discord.Interaction, None], user: discord.Member, cor):# Tira uma carta do baralho e mamnda para embedar_e_mandar()
        """Dá uma carta de aventura para um Player."""
        # Check if the deck is empty
        if interaction != None:
            channel = interaction.channel
            if not isinstance (channel, discord.abc.Messageable):
                return # or send an error
        else:
            channel = await self.client.fetch_channel(1065721164657336370)
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
        await self.embedar_e_mandar(interaction, card,cor, user)
        return 1

    async def deal_mestre(self, interaction :Union[discord.Interaction, None], num_players: int):#Deal dm, mas para quem tiver o cargo "Mestre"
        if interaction != None:
            channel = interaction.channel
            if not isinstance(channel, discord.abc.Messageable):
                    return
        else:
            channel = await self.client.fetch_channel(1065721164657336370)
            if not isinstance(channel, discord.abc.Messageable):
                    return
        members = await get_members(self.client)
        if not members:
            print("Server deu None")
            return
        for member in members:
            if discord.utils.get(member.roles, name="Mestres"):
                i = 0
                while i< num_players: 
                    print("deal mestre")
                    await self.deal_dm(interaction, member, colors().red)
                    i+= 1
                
                await channel.send("Mestre recebeu a carta!")

    async def is_owner(self, interaction : discord.Interaction):#Retorna True se o interaction.user for dono do server
        if interaction.user.id == 286540943056830474:
            return True
        else:
            return False

    async def find_card(self, interaction : discord.Interaction, nome : str):
        '''Pesquisa no baralho as cartas que contenham os termos pesquisados.'''
        whole_deck = deck + dealt_cards
        result = []
        for term in whole_deck: # busca no deck alguma carta que contenha os elementos de "term"
            if nome.lower() in (term.lower()) :
                result.append(term)
        return result
                
                
    #Comandos: ---------------------------------------------------------------------
    #Comandos: ---------------------------------------------------------------------
    #Comandos: ---------------------------------------------------------------------
    
    
    '''/deal [player]''' #Manda uma carta na DM do Player
    @app_commands.command()
    @app_commands.rename(user='player')
    @app_commands.describe( #options 
        user='Player para receber a carta na DM'
    )
    async def deal(self, interaction: discord.Interaction, user: discord.Member, carta: str = "", quantidade: int = 1):
        """Dá uma carta de aventura para um Player."""
        channel = interaction.channel
        await interaction.response.send_message("Mandando carta",delete_after=1)
        if not isinstance(channel, discord.abc.Messageable):
            return
        if not carta:
            for i in range(quantidade):
                flag = await self.deal_dm(interaction,user, colors().blue)
                if flag == 1:
                    await channel.send(f"{user.mention} recebeu uma carta!",delete_after=1)
            else:
                return
        else:
            await channel.send("Mandando carta...;)")
            card = await self.find_card(interaction, carta)
            try:
                card[1]
                await channel.send(f"Mais de uma carta encontrada. {interaction.user.mention}")
                return
            except:
                if not card:
                    await channel.send(f"Nenhuma carta encontrada. {interaction.user.mention}")
                else:                
                    await self.embedar_e_mandar(card =card[0], interaction = interaction, cor =colors().blue, user=user)
                

    '''/deal_all'''#Dá uma carta para cada player que está online no voice do rpg, e tem o role "Jogadores"
    @app_commands.command()
    async def deal_all(self, interaction: discord.Interaction):
        """Distribui uma carta de aventura para todos os Players no voice, e para o Mestre"""
        voice_channel = self.client.get_channel(1047320748529811500)
        if not isinstance(voice_channel, discord.VoiceChannel):
            return
        players = [member for member in voice_channel.members]
        flag = 0
        for player in players:
            if discord.utils.get(player.roles, name="Jogadores") is not None:
                await self.deal_dm(interaction, player, colors().blue)
                flag = 1
                await self.deal_mestre(interaction, 1)
        if flag == 0:
            await interaction.response.send_message("Nenhum player conectado no canal de voz")
        else:
            await interaction.response.send_message("Todos os players(e mestre) receberam cartas.", delete_after=1)
        print("Mãos de baralho: \n")
        for player in player_cards:
            print(f"Player:{player.user} tem cartas : {player_cards[player]}")
        

    '''/shuffle''' #Embaralha as cartas que estão no baralho
    @app_commands.command()
    async def shuffle(self, interaction : discord.Interaction):
        '''Embaralha as cartas que estão no baralho'''
        random.shuffle(deck)
        await interaction.response.send_message("Baralho embaralhado")


    '''/retornar''' #Retorna as cartas para o baralho
    @app_commands.command()
    async def retornar(self, interaction : discord.Interaction):
        '''Retornar todas as cartas para o Baralho e embaralha.'''
        await interaction.response.send_message("Baralho sendo retornado e embaralhado")
        members = await get_members(self.client)
        if not members: 
            return
        for member in members:
            try:
                async for message in member.history(limit = None):
                    if message.author == self.client.user:
                        try:
                            footer = message.embeds[0].footer.text
                            if not footer:
                                return
                            if (footer.find("Carta de aventura") != -1):
                                await message.delete()
                                print("Mensagem deletada")
                        except Exception as e:
                            print(f"Mensagem não era carta de aventura {e}")
            except Exception as e:
                print(f"Não foi possível deletar as cartas de: {member} /n {e}")
        
        # Add all dealt cards back to the deck
        deck.extend(dealt_cards)

        # Clear the list of dealt cards
        dealt_cards.clear()
        descartadas.clear()
        random.shuffle(deck)
        player_cards.clear()
        if not isinstance(interaction.channel, discord.abc.Messageable):
            return
        await interaction.channel.send("Baralho retornado e embaralhado.")
    
    
    '''/mão [Player]'''#Mostra as cartas que estão na mão de [Player]
    @app_commands.command()
    async def mão(self, interaction, player: discord.Member): 
        try:
            if player_cards[player] != None:
                await interaction.response.send_message(f"O player {player.name} está com a(s) carta(s) {player_cards[player]}")
            else:
                await interaction.response.send_message(f"O player {player.mention} não possui cartas")
        except:
            await interaction.response.send_message(f"O player {player.mention} não possui cartas")
        print("Mãos de baralho: \n")
        for player in player_cards:
            print(f"Player:{player.name} tem cartas : {player_cards[player]}")
    
    
    '''/descartes''' #Responde com uma lista com os nomes das cartas que foram descartadas 
    @app_commands.command()
    async def descartes(self, interaction: discord.Interaction):
        '''Mostra a pilha de cartas descartadas.'''
        cartas = []
        for card in descartadas:
            name = card
            cartas.append(name)
        array_string = "-"
        array_string = "- "+"\n- ".join(cartas)
        embedvar = discord.Embed(title = "Pilha de descartes", description = array_string)
        await interaction.response.send_message(embed = embedvar)

    '''/carta [Nome da carta para pesquisar]''' #Pesquisa no baralho uma carta com um nome [nome] e manda embeds de todas as cartas que contém aqueles termos em suas palavras
    @app_commands.command()
    @app_commands.describe( #options 
        nome='Nome da carta'
    )
    async def carta(self, interaction : discord.Interaction, nome : str):
        '''Pesquisa no baralho as cartas que contenham os termos pesquisados.'''
        await interaction.response.send_message("Buscando cartas com os termos desejados..." , delete_after=5)
        channel = interaction.channel
        if not isinstance(channel, discord.abc.Messageable):
            return
        cartas = []
        cartas = await self.find_card(interaction, nome)
        if cartas == None:
            await channel.send("Nenhuma carta foi encontrada com esse termo, tente novamente com um termo diferente.")
            return
        for carta in cartas: 
            parts = carta.split(":")
            title = parts[0]
            desc = parts[1]
            embedvar = discord.Embed(title = title, description = desc, color = colors().green)
            await channel.send(embed = embedvar)
        await channel.send("Todas as cartas encontradas foram mostradas.")



#Botões: ---------------------------------------------------------------------------------
#Botões: ---------------------------------------------------------------------------------
#Botões: ---------------------------------------------------------------------------------
class Descartar(discord.ui.View):#Botão de descartar carta 
    """Descarta a carta da mensagem"""
    def __init__(self)-> None:
            super().__init__(timeout = None)
    
    @discord.ui.button(label="Descartar", style=discord.ButtonStyle.primary, custom_id= "Descartar")
    async def button_callback(self,  interaction, button):
        embed = interaction.message.embeds
        title = embed[0].title
        descartadas.append(title)
        try:
            player_cards[interaction.user].remove(title)#tira a carta da mão do brother
        except:
            print(f"O {interaction.user.mention} descartou uma carta que não estava na sua mão, provavelmente porque o bot reiniciou e zerou as mãos")
        await interaction.message.delete() 

        channel = interaction.client.get_channel(1065721164657336370)
        if not isinstance(channel, discord.abc.Messageable):
            return
        await channel.send(f"{interaction.user.mention} descartou uma carta!")
            

#Setup: ----------------------------------------------------------------------------------
async def setup(client): # Must have a setup function
    await client.add_cog(Baralho_de_aventura(client)) # Add the class to the cog.