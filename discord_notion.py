from http import client
import json
import requests
import secrets
from typing import Optional
import discord
from discord import app_commands
from discord.ext import commands, tasks
from datetime import datetime, timedelta
import asyncio
from my_secrets.Secrets import NOTION_API_TOKEN, NOTION_TOKEN_V2 , OST_DATABASE_ID   #type: ignore



headers = {
    "Accept": "application/json",
    "Authorization": f"Bearer {NOTION_API_TOKEN}",
    "Notion-Version": "2022-06-28",  # Check the latest API version
    'content-type': 'application/json',
}



OST_DATABASE_FILE = "pages.json"

#Funções: --------------------------------------------------------------------------------
#Funções: --------------------------------------------------------------------------------
#Funções: --------------------------------------------------------------------------------
#Funções:
def salvar_json(file_name, content):
    with open(file_name, "w", encoding="utf8") as file:
        json.dump(content, file, ensure_ascii=False, indent=4)
    
        
def abrir_json(file_name):
    with open(file_name, "r") as file:
        return json.load(file)

async def update_page(page_id,payload,headers):
    url = f"https://api.notion.com/v1/pages/{page_id}"
    response = requests.patch(url=url, json=payload, headers=headers)
    return response


async def get_database_pages(DATABASE_ID):
    NOTION_DATABASE_URL = f"https://api.notion.com/v1/databases/{DATABASE_ID}"
    params = {}
    all_pages_data = []
    while True: #Loop de fetch de todas as páginas da Database
        
        response = requests.post(NOTION_DATABASE_URL+"/query", headers=headers, json=params )
        #print("Status do request:" + str(response.status_code)+"\n")
        
        if response.status_code == 200:
            database_data = response.json()
            database_pages = database_data['results']
            j = 0
            
            for page in database_pages:
                j+=1
                page_id = page['id']  # Use the unique ID as the key
                page_data = page 
                all_pages_data.append(page_data)
                    
            #print(f"Páginas totais do pedido: {j}")
            if database_data.get("has_more", True):
                start_cursor = database_data["next_cursor"]
                params["start_cursor"] = start_cursor
            else:
                #print("Terminou de pegar as páginas da database")
                break
            
        else:
            print("Erro no request notion:" + str(response.content))
            break
    return all_pages_data

#Classe:--------------------------------------------------------------------------------
#Classe:--------------------------------------------------------------------------------
#Classe:--------------------------------------------------------------------------------
class discord_notion(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    '''/comando'''
    @app_commands.command()
    async def commando(self, interaction : discord.Interaction):
        await interaction.response.send_message("Olá")
    
    @commands.Cog.listener()
    async def on_ready(self):
        self.check_notion_database_for_ost.start()
    
    @tasks.loop(seconds=5)
    async def check_notion_database_for_ost(self):
        #print("Loop\n")
        
        pages = await get_database_pages(OST_DATABASE_ID)
        NOTION_DATABASE_URL = f"https://api.notion.com/v1/databases/{OST_DATABASE_ID}"
        for page in pages:
            properties = page.get('properties', {})
            page_id = page['id']
            # Check if the "Play" checkbox is checked
            if properties.get('Play', {}).get('checkbox', False):
                print("Tocando OST no bot!")
                
                #tocar música no bot
                #Tirar o play selecionado
                global headers
                properties = {
                    'Play': {'type': 'checkbox', 'checkbox': False},
                }
                payload = {
                    "properties": properties,
                }
                # Uncheck the "Play" checkbox after playing
                response = await update_page(page_id,payload,headers)
                if response.status_code != 200:
                    print(response.content)
                voice_channel =await  self.client.fetch_channel(1047320748529811500)
                await voice_channel.connect()
                music_channel = await self.client.fetch_channel(1053116705704001646)
                await music_channel.send("/play https://www.youtube.com/watch?v=YoBe-OpHRmc")
        
        



#Setup: --------------------------------------------------------------------------------
async def setup(client): # Must have a setup function
    await client.add_cog(discord_notion(client)) # Add the class to the cog.