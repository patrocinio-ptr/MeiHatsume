import discord
from discord.ext import commands
import random
import os

TOKEN = os.environ['TOKENV']
intents = discord.Intents.all()
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
    'Monólogo vilanesco: O vilão perde sua próxima ação falando seu plano diabólico.',
    'Corridão: A distância da viagem é reduzida pela metade, ou o personagem dobra sua movimentação neste turno.',
    'Saldão: Seu herói consegue um item genérico de sua escolha(como sucateiro).',
    'Entregando o jogo: Sucesso automático em persuasão, intimidação ou outra forma de conseguir informação.',
    'Epifania: Tenha um d6 em qualquer perícia que não tinha antes até o final da sessão(se a sessão for dividida em dois, este permanece)',
    'Esforço extra: Adicione +1d6 em qualquer rolagem.',
    'Fica a dica: O mestre responde algo, ou dá alguma dica ou informação importante para o personagem.',
    'Uma alma por outra: Evita a morte, captura ou outra situação ruim para você ou um aliado, mas isso leva a um novo problema, determinado pelo mestre',
    'Herói popular: Após salvar um grupo de pessoas, a comunidade local adota você e seu grupo como heróis locais e sempre oferecerá ajuda.',
    'Hoje não: Ao jogar essa carta, um ataque de alguém é considerado automaticamente como uma falha crítica.',
    'Hora da revolta: +2 em ações contra um personagem até o fim do dia.',
    'Hora do sangue: Nenhum personagem pode absorver dano(poderes não contam) até que um coringa seja sacado nesse combate.',
    'Inimigo: Jogue no começo da sessão. Um personagem da escolha do mestre vira inimigo jurado do seu personagem. Você não pode absorver danos contra ele. A partir de agora, compre duas cartas de aventura até que o vilão seja derrotado.',
    'Check point: Recupere todos seus EQ imediatamente',
    'Inspiração: Todos da sua equipe recebem +2 para rolagens de características até o fim da rodada.',
    'Interesse amoroso: Jogue em um extra. Isso encoraja um interesse romântico, esse personagem pode ajudar, mas também pode causar problemas com frequência, pela sua inocência.',
    'Fúria: Após receber um Ferimento, jogue essa carta e cause +2 de dano em seus ataques, para cada Ferimento que tenha recebido, até o fim da cena.',
    'Levantar a moral: Recupera todos seus aliados do estado Abalado, Vulnerável, Distraído e estados de complicações menores, depois de um discurso, se o discurso for muito bom, recupera um Ferimento.',
    'Sorte grande: Tire mais duas cartas do Baralho e escolha uma.',
    'Touché: Jogue após serem surpreendidos, isso anula a surpresa e todos compram cartas de iniciativa normalmente.',
    'Fortuna: Ao lotear algo ou alguém, jogue essa carta e encontre tudo que pode ser encontrado.',
    'Mal funcionamento: Causa um mau funcionamento ou quebra em algum equipamento(invento mecânico também conta), consertar é uma rolagem de reparo-4 e com 10 minutos.',
    'Multidão enfurecida: Durante um combate, uma multidão armada(2 por personagem da party) entra no combate e ajuda os heróis.',
    'Na hora certa: Gaste um bene e escolha uma carta no baralho de aventura, você pode jogar uma carta extra nesta sessão.',
    'OOHHH!: Um inimigo determinado pelo mestre tem seu tamanho e Força aumentado em 2, e todos os aliados compram 1 carta de aventura.',
    'Paz: Melhora a atitude de um grupo, por conhecer alguém no meio, mostrar respeito ou apenas persuadi-los a não serem ofensivos. Não funciona em vilões de verdade',
    'Reanimar: Levanta todos os aliados extras imediatamente sem Ferimentos.',
    'Reforços: Reforços inimigos chegam(quantos e como fica a critério do mestre) e todos os aliados compram uma carta extra.',
    'Save point: Depois de 30 minutos ininterruptos, jogue essa carta e considere como se o personagem tivesse tido uma noite completa, restaurando todo seu EQ e suas Fadigas',
    'Revelação: Durante uma pesquisa, seu herói descobre tudo que há para ser descoberto, ou absorve uma informação importante sobre o assunto.',
    'Segundo vento: Cura automaticamente todos os Ferimentos e Fadigas do personagem',
    'Selvageria: Ganha uma vantagem qualquer de sua escolha, sem ter que obedecer requisitos pelo resto da sessão.',
    'Assassino nato: Durante 1d6 turnos, você age como se tivesse tirado um coringa.',
    'Surto de adrenalina: Ganha um turno extra quando decidir usar.',
    'Trabalho em equipe: Seu herói e quaisquer personagens adjacentes fazem um ataque em conjunto, com +4 cada.',
    'Vestido para matar: Adicione +4 em seu carisma durante essa sessão, pois seu personagem está vestido muito bem ou está a caráter na ocasião.',
    'Vira casaca: Convence um inimigo(menor) a fazer alguma coisa para lhe ajudar.',
    'Você não disse isso: Durante um combate, diga algo intenso e amedrontador, que nunca deveria ser dito. Todos, sem exceção, ficam Abalados.(menos você)',
    'Agrupar em equipe: Todos a 5 quadros, de você(aliados), recebem +2 em Aparar e Resistência até que um coringa seja sacado.',
    'Relíquia: Ao saquear alguma área, ou em qualquer ocasião, seu herói encontra um item importantíssimo, com um passado misterioso e algum poder ou maldição atrelado.',
    'Homenagem: Depois da morte de algum personagem, seu herói fala algumas palavras importantes, todos compram cartas novas.',
    'Espanto: Depois de falar alguma coisa, todos os inimigos em um raio de 10m perdem suas ações.',
    'Ladrão: Roube um bene de qualquer Carta Selvagem.',
    'Jeito difícil: Transforme todos os seus benes em XP',
    'Karma: Depois de fazer uma boa ação(o mestre decide se vale) recupere os benes de todos nesta sessão.',
    'Comando: O bônus de ações de suporte são dobrados até o fim do combate.',
    'Que barulho é esse?: Todos os players recebem uma carta extra, e podem jogar duas cartas essa sessão, mas em algum momento, alguma ameaça surgirá.',
    'Reciclar: Escolha uma carta da pilha de descarte, para usá-la como carta extra.',
    'Ferro quente e whiskey: Recupera todos os Ferimentos de um personagem, mas o deixa com uma cicatriz horrível, que o deixa com -2 de Carisma por um mês no jogo.',
    'Máfia: Uma gangue da máfia entra no combate, se eles são aliados ou não, o mestre diz.',
    'Plus-ultra: O personagem pode usar QUALQUER poder do livro uma vez nesse combate, desde que faça sentido com sua individualidade',
    'Apunhalada: Um aliado te trai, se aliando com seus inimigos ou contando seus segredos. Todos compram uma carta de aventura e recuperam seus benes.',
    'Pacto escuro: Jogue depois de presenciar um evento estranho, ou conhecer alguma força da natureza ou sobrenatural. Você recebe a desvantagem “Má sorte”, mas tira e usa 2 cartas de aventura por sessão.',
    'Intuição inesperada: Seu personagem consegue afetar uma criatura com um ataque, independentemente das invulnerabilidades dela ou situação.'
]   

# List to keep track of which cards have been dealt
dealt_cards = []

# Create a new Discord bot
bot = commands.Bot(command_prefix='!',intents=intents)

#funções: ----------------------------------------------------------------------------------
async def embedar(carta, color): #pega uma string "carta" e divide ela nos ":", criando um embed com titulo e descrição, e recebe a cor, no formato color().COR
    parts = carta.split(":")
    title = parts[0]
    desc = parts[1]
    embedvar = discord.Embed(title = title, description = desc, color = color)
    return embedvar
#comandos: ----------------------------------------------------------------------------------
#comandos: ----------------------------------------------------------------------------------
#comandos: ----------------------------------------------------------------------------------

# Define the command for dealing a card to a specific user
@bot.command()
async def deal(ctx, user: discord.Member):
    # Check if the deck is empty
    if len(deck) == 0:
        await ctx.send("Baralho acabou, digite !retornar para retornar as cartas.")
        return

    # Deal a random card from the deck to the target user
    card = random.choice(deck)

    # Add the dealt card to the list of dealt cards
    dealt_cards.append(card)

    # Remove the dealt card from the deck
    deck.remove(card)
  
    # Separate title from descriprion and embed it
    parts = card.split(":")
    title = parts[0]
    description = parts[1]
    embedvar = discord.Embed(title=title, description= description, color=discord.Color.blue())
 
  # Send a message to the target user with the dealt card
    await user.send(embed = embedvar)

    # Send a message to the channel indicating that the target user has been dealt a card
    await ctx.send(f"{user.mention} recebeu uma carta.")


# Define the command for dealing a card to all players with the "Player" role
@bot.command()
async def dealall(ctx):
    # Check if the deck is empty
    if len(deck) == 0:
        await ctx.send("Baralho acabou, digite !retornar para retornar as cartas.")
        return

    # Get all members with the "Player" role
    voice_channel = bot.get_channel(1047320748529811500)
    players = [member for member in voice_channel.members]

    # Deal a random card to each player
    for player in players:
        # Deal a random card from the deck
        card = random.choice(deck)

        # Add the dealt card to the list of dealt cards
        dealt_cards.append(card)

        # Remove the dealt card from the deck
        deck.remove(card)
        # Separate title from descriprion and embed it
        parts = card.split(":")
        title = parts[0]
        description = parts[1]
        embedvar = discord.Embed(title=title, description= description, color=discord.Color.blue())
       
        # Send a message to the player with the dealt card
        await player.send(embed = embedvar)

    # Send a message to the channel indicating that all players have been dealt a card
    await ctx.send("Todos os players receberam cartas")


@bot.command()
async def dealmestre(ctx, Jogadores):
    # Check if the deck is empty
    if len(deck) == 0:
        await ctx.send("Baralho acabou, digite !retornar para retornar as cartas.")
        return
    mestres = [member for member in ctx.guild.members if discord.utils.get(member.roles, name="Mestre") is not None]
       # Deal a random card from the deck to the target user
    for mestre in mestres:
        while int(Jogadores) > 0:
        # Deal a random card from the deck
          card = random.choice(deck)
  
          # Add the dealt card to the list of dealt cards
          dealt_cards.append(card)
  
          # Remove the dealt card from the deck
          deck.remove(card)
          # Separate title from descriprion and embed it
          parts = card.split(":")
          title = parts[0]
          description = parts[1]
          embedvar = discord.Embed(title=title, description= description, color=discord.Color.red())
         
          # Send a message to the player with the dealt card
          await mestre.send(embed = embedvar)
          Jogadores = int(Jogadores) -1


@bot.command()
async def retornar(ctx):
    # Add all dealt cards back to the deck
    deck.extend(dealt_cards)

    # Clear the list of dealt cards
    dealt_cards.clear()

    # Shuffle the deck
    random.shuffle(deck)

    # Send a message to the channel indicating the deck has been shuffled
    await ctx.send("Cartas retornadas e baralho embaralhado.")


@bot.command()
async def descartes(ctx):
    cartas = []
    for card in dealt_cards:
      parts = card.split(":")
      name = parts[0]
      print(name)
      array_string = "-"
      cartas.append(name)
    array_string = "-"+"\n- ".join(cartas)
    embedvar = discord.Embed(title = "Pilha de descartes", description = array_string)
    await ctx.send(embed = embedvar)


@bot.command()
async def dealtudo(ctx):
    while True:
      if len(deck) == 0:
          await ctx.send("Baralho acabou, digite !retornar para retornar as cartas.")
          return 0
  
      # Get all members with the "Player" role
      voice_channel = bot.get_channel(1047320748529811500)
      players = [member for member in voice_channel.members]
  
      # Deal a random card to each player
      for player in players:
          # Deal a random card from the deck
          card = random.choice(deck)
  
          # Add the dealt card to the list of dealt cards
          dealt_cards.append(card)
  
          # Remove the dealt card from the deck
          deck.remove(card)
          parts = card.split(":")
          title= parts[0]
          desc = parts[1]
          embedvar = discord.Embed(title = title, description = desc, color = colors().blue)
          # Send a message to the player with the dealt card
          await player.send(embed = embedvar)
  
      # Send a message to the channel indicating that all players have been dealt a card
    await ctx.send("Todas as cartas foram esvaziadas.")


@bot.command()
async def shuffle(ctx):
    random.shuffle(deck)
    await ctx.send("Baralho embaralhado")


@bot.command()
async def carta(ctx, name : str):
    whole_deck = deck + dealt_cards
    result = []
    for term in whole_deck:
      if name.lower() in (term.lower()) :
        result = term
        parts = result.split(":")
        title = parts[0]
        desc = parts[1]
        embedvar = discord.Embed(title = title, description = desc, color = colors().green)
        await ctx.send(embed = embedvar)


  
bot.run(TOKEN)

# Modificar o código com :
# Deal all: Checar players no canal de voz, e checar se eles tem Player role
# Descartar apenas cartas que os players mandarem: !descartar, colocando em uma pilha separada, que é descartes = []
#
#
#