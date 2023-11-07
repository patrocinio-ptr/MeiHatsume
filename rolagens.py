import discord
from discord import app_commands
from discord.ext import commands
import random
from typing import Union
import os
import sys
from utility import is_owner, get_members, get_server, owner, is_mestre #type: ignore
import asyncio


suits = {
    "Clubs": "♣️",
    "Diamonds": "♦️",
    "Hearts": "♥️",
    "Spades": "♠️"
}
ranks = ["Ás", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "**CURINGA MUAHAHAHAHAH**"]
deck = [f"{rank} de {suits[suit]}" for suit in suits for rank in ranks]


#Classe:--------------------------------------------------------------------------------
#Classe:--------------------------------------------------------------------------------
#Classe:--------------------------------------------------------------------------------
class Rolagens(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    #Eventos: --------------------------------------------------
    #Eventos: --------------------------------------------------
    #Eventos: --------------------------------------------------
    
    @commands.Cog.listener()
    async def on_message(self, message):
        """Rola dados com soma e explosão caso contenham '!'"""
        channel = message.channel
        if message.author == self.client.user: #ignora se vier do bot
            return
        if not isinstance(channel, discord.abc.Messageable):
            return
        if isinstance(message.channel, discord.DMChannel):
            await self.client.process_commands(message)
        if  message.content.startswith("."):
            #Definindo variáveis
            rolled = []
            roll = message.content[1:] #tira o "." da mensagem
            dice = roll.split('+') # Separa a soma de dados
            result = 0
            display = ""
            
            for die in dice: #Faz iterações para o número de dados que foram separados por +
                die = die.strip() #Tira espaços da string
                
                if 'd' in die: #Checa se tem "d" na string, senão retorna
                    num, size = die.split('d') #Separa em número de dados, e tamanho do dado
                    said = die.split('d')
                    if num == '': #se não tiver numerador, vira 1
                        num = 1
                    else:
                        num = int(num) #se tiver, transforma em int
                    if '!' in size: #se tiver "!" depois do tamanho, explode o dado
                        size = int(size[:-1]) #pega o tamanho em int, tirando o "!"
                        if size == 1:
                            await channel.send("Não use dados de 1 lado!")
                            return
                        total = 0
                        for i in range(num): #Faz isso para todos no numerador do dado
                            roll = random.randint(1, size)
                            while roll == size:
                                rolled.append(f"**{roll}**")
                                total += roll
                                roll = random.randint(1, size)
                            if roll == 1:
                                rolled.append(f"**{roll}**")
                            else:
                                rolled.append(roll)
                            total += roll
                    else: #Se não estourar
                        size = int(size)
                        total = 0
                        for i in range(num):
                            roll = random.randint(1, size)
                            total += roll
                            if (roll == 1) or (roll == 6):
                                rolled.append(f"**{roll}**")
                            else:
                                rolled.append(roll)
                    result += total
                    display += f"{rolled} " + said[0]+"d"+said[1] + " + "

                    rolled = [] 
                elif 'D' in die:    #sure crit     
                    die = die.strip() #Tira espaços da string
                    if 'D' in die: #Checa se tem "d" na string, senão retorna
                        num, size = die.split('D') #Separa em número de dados, e tamanho do dado
                        said = die.split("D")
                        if num == '': #se não tiver numerador, vira 1
                            num = 1
                        else:
                            num = int(num) #se tiver, transforma em int
                        if '!' in size: #se tiver "!" depois do tamanho, explode o dado
                            size = int(size[:-1]) #pega o tamanho em int, tirando o "!"
                            if size == 1:
                                await channel.send("Não use dados de 1 lado!")
                                return
                            total = 0
                            for i in range(num): #Faz isso para todos no numerador do dado
                                roll = size
                                while roll == size:
                                    rolled.append(f"**{roll}**")
                                    total += roll
                                    roll = random.randint(1, size)
                                if roll == 1:
                                    rolled.append(f"**{roll}**")
                                else:
                                    rolled.append(roll)
                                total += roll
                        else: #Se não estourar
                            size = int(size)
                            total = 0
                            for i in range(num):
                                roll = size
                                total += roll
                                if (roll == 1) or (roll == size):
                                    rolled.append(f"**{roll}**")
                                else:
                                    rolled.append(roll)
                        result += total
                        display += f"{rolled} " + said[0]+"d"+said[1] + " + "

                        rolled = [] 
                else:
                    n = int(die)
                    result+= n
                    display += f"{n}" + " + "
            display = display[:-2].replace("'","")   

            await message.reply(f"` {result} ` ⟵ {display}, {message.author.mention}")
            await message.delete()  
    
    
    #Comandos: --------------------------------------------------
    #Comandos: --------------------------------------------------
    #Comandos: --------------------------------------------------

    '''/deck''' #da uma carta do baralho normal
    @app_commands.command()
    async def deck(self, interaction: discord.Interaction):
        '''Tira uma ou mais cartas de um baralho'''
        global deck
        if len(deck) == 0:
            # If the deck is empty, reshuffle the cards
            deck = [f"{rank} de {suits[suit]}" for suit in suits for rank in ranks]
        # Draw a random card from the deck
        card = random.choice(deck)
        # Remove the card from the deck
        deck.remove(card)
        # Send the card to the channel
        await interaction.response.send_message(f"{interaction.user.mention} recebeu {card}!")
        
    '''/deck_dm''' #da uma carta do baralho normal
    @app_commands.command()
    async def deck_dm(self, interaction: discord.Interaction):
        '''Tira uma ou mais cartas de um baralho'''
        global deck
        if len(deck) == 0:
            deck = [f"{rank} de {suits[suit]}" for suit in suits for rank in ranks]
        card = random.choice(deck)
        deck.remove(card)
        await interaction.user.send(f"{interaction.user.mention} recebeu {card}!")
        await interaction.response.send_message("Mandando carta na DM!", delete_after=1)

    
    '''/deck_shuffle'''#embaralha o deck de cartas normais
    @app_commands.command()
    async def deck_shuffle(self, interaction: discord.Interaction):
        '''Embaralha o deck normal'''
        deck = [f"{rank} de {suits[suit]}" for suit in suits for rank in ranks]
        await interaction.response.send_message(f"{interaction.user.mention} Deck embaralhado!")
    

    '''/rolar [rolagem] [resultado]   
    @app_commands.command()
    @app_commands.check(is_mestre or is_owner)
    async def rolar(self, interaction:discord.Interaction, rolagem: str, resultado: int = 0 ):
        await interaction.response.send_message("Rolando", delete_after=0.1)
        rolagem = rolagem.replace("!","")
        estoura = 1
        exc = ""
        parts = rolagem.split("d")
        rolls = int(parts[0])
    
        die = int(parts[1])
        if resultado == 0:
            resultado = random.randint(1, rolls*4)
        if resultado%die == 0:
            if rolls == 1 and resultado == die:
                estoura = 0
                resultado = die
            else:
                estoura = 1
                resultado +=random.randint(1,die)
            
        if not isinstance(interaction.channel, discord.abc.Messageable):
            return
        dice_rolls = []
        total = 0
        flag = 1
        counter = 0
        while flag == 1:
            
            for i in range(rolls):    
                dice_roll = random.randint(1, die)
                total += dice_roll
                dice_rolls.append(str(dice_roll))
                while ((dice_roll == die)):  # Check for exploding dice
                    if estoura ==1:
                        dice_roll = random.randint(1, die)
                        total += dice_roll
                        dice_rolls.append(str(dice_roll))
                    else:
                        break
            if total != resultado :  # Stop rolling if the desired result can't be achieved
                flag=1
                dice_rolls = []
                total = 0
            else:
                flag = 0    
            counter+=1
            if counter >10000:
                dice_rolls = []
                total = 0
                aux = resultado
                while aux > die:
                    dice_roll = die
                    total += dice_roll
                    dice_rolls.append(str(dice_roll))
                    aux -= die
                for i in range(rolls-1):
                    dice_roll = random.randint(1,(die-1))
                    total += dice_roll
                    dice_rolls.append(str(dice_roll))
                    
                dice_roll = aux
                total += dice_roll
                dice_rolls.append(str(dice_roll))
                flag = 0
            
        rolagem_str = ",".join(dice_rolls)
        rolagem_str = rolagem_str.replace(str(die), f"**{die}**")
        rolagem_str = rolagem_str.replace("1,", f"**1**,")
        rolagem_str = rolagem_str.replace("1]", f"**1**]")
        
        if  estoura == 1:
            exc = "!"
        await interaction.channel.send(f"`{total}` <-- [{rolagem_str}] {rolls}d{die}{exc}, {interaction.user.mention}")
        '''
    '''/rolar2 [rolagem] [resultado]''' #Segundo comando de rolagem rigged, esse aqui aceita dois termos, mas não aceita rolagens mirabulantes, como 1d6! dando 36, mas funciona para rolagens compostas como 1d6! + 1d8! dar uma falha crítica    
    @app_commands.command()
    async def rolar(self, interaction:discord.Interaction, rolagem: str, resultado: int  ):
        await interaction.response.send_message("Rolando", delete_after=0.1)
        channel = interaction.channel
        if not isinstance(channel, discord.abc.Messageable):
            return
        total_da_rolagem = 0
        rolled = []
        conjuntos = rolagem.split('+') # Separa a soma de dados
        total_da_rolagem = 0
        display = ""
        flag = 1
        counter = 0
        while flag == 1:
            counter += 1
            for die in conjuntos: #Faz iterações para o número de dados que foram separados por +
                die = die.strip() #Tira espaços da string
                
                if 'd' in die: #Checa se tem "d" na string, senão retorna
                    num_of_dice, size = die.split('d') #Separa em número de dados, e tamanho do dado
                    said = die.split('d')#anota para usar na string do display
                    if num_of_dice == '': #se não tiver numerador, vira 1
                        num_of_dice = 1
                    else:
                        num_of_dice= int(num_of_dice) #se tiver, transforma em int
                    
                    #se tiver "!" depois do tamanho, explode o dado   
                    if '!' in size: 
                        total = 0
                        size = int(size[:-1]) #pega o tamanho em int, tirando o "!"
                        if size == 1:
                            await channel.send("Não use dados de 1 lado!")
                            return
                        
                        for i in range(num_of_dice): #Faz isso para todos no numerador do dado
                            roll = random.randint(1, size)
                            while roll == size:
                                rolled.append(f"**{roll}**")
                                total += roll
                                roll = random.randint(1, size)
                            
                            if roll == 1:
                                rolled.append(f"**{roll}**")
                            else:
                                rolled.append(roll)
                                
                            total += roll
                    #Se não estourar
                    else: 
                        total = 0
                        size = int(size)
                        
                        for i in range(num_of_dice):
                            roll = random.randint(1, size)
                            total += roll
                            
                            if (roll == 1) or (roll == 6):
                                rolled.append(f"**{roll}**")
                            else:
                                rolled.append(roll)
                                
                    total_da_rolagem += total #acrescenta ao total da rolagem
                    display += f"{rolled} " + said[0]+"d"+said[1] + " + " #anota a rolagem desse(s) dados no display
                    rolled = [] #zera para o próximo dado
            if resultado != total_da_rolagem:
                flag = 1
                total_da_rolagem = 0
                display = ""
                if counter>=100000:
                    await channel.send("Rolagem improvável")
                    return
                    
            else:
                flag = 0
            
        
        
        display = display[:-2].replace("'","")   

        await channel.send(f"`{total_da_rolagem }` <-- {display}, {interaction.user.mention}")



async def setup(client): # Must have a setup function
    await client.add_cog(Rolagens(client)) # Add the class to the cog.