import discord
from discord import app_commands
from discord.ext import commands
from typing import Union
from utility import is_owner, get_members, get_server, owner, is_mestre, guild_id #type: ignore
import asyncio
import youtube_dl



YTDL_OPTIONS = {
    'format': 'bestaudio/best',
    'outtmpl': 'downloads/%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'  # bind to ipv4 since ipv6 addresses cause issues sometimes
}

FFMPEG_OPTIONS = {
    'options': '-vn'
}

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: youtube_dl.YoutubeDL(YTDL_OPTIONS).extract_info(url, download=not stream))

        if data and ('entries' in data):
            # take first item from a playlist
            data = data['entries'][0]

            filename = data['url'] if stream else youtube_dl.YoutubeDL(YTDL_OPTIONS).prepare_filename(data)
            return cls(discord.FFmpegPCMAudio(filename, **FFMPEG_OPTIONS), data=data)#type: ignore


class MusicControls(discord.ui.View):
    def __init__(self, client):
        super().__init__(timeout=None)
        self.client = client
        global guild_id
        self.guild_id = guild_id

    @discord.ui.button(label="Pause", style=discord.ButtonStyle.primary, custom_id="pause")
    async def pause_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild = interaction.guild
        if not guild:
            print("Guild deu None")
            return
        vc = guild.voice_client
        if not isinstance(vc, discord.VoiceClient):
            print("vc not VoiceClient")
            return
        if not vc:
            if isinstance(interaction.channel, discord.abc.Messageable):
                await interaction.channel.send("Bot não conectado ao voice")
            return
        vc.pause()
        await interaction.response.send_message("Music paused.")

    @discord.ui.button(label="Resume", style=discord.ButtonStyle.primary, custom_id="resume")
    async def resume_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild = interaction.guild
        if not guild:
            print("Guild deu None")
            return
        vc = guild.voice_client
        if not isinstance(vc, discord.VoiceClient):
            print("vc not VoiceClient")
            return
        if not vc:
            if isinstance(interaction.channel, discord.abc.Messageable):
                await interaction.channel.send("Bot não conectado ao voice")
            return
        vc.resume()
        await interaction.response.send_message("Music resumed.")

    @discord.ui.button(label="Loop", style=discord.ButtonStyle.primary, custom_id="loop")
    async def loop_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.client.get_cog("Music").loop_status[self.guild_id] = not self.client.get_cog("Music").loop_status.get(guild_id, False)
        status = "enabled" if self.client.get_cog("Music").loop_status[self.guild_id] else "disabled"
        await interaction.response.send_message(f"Loop has been {status}.")

    @discord.ui.button(label="Next Song", style=discord.ButtonStyle.primary, custom_id="next_song")
    async def next_song_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild = interaction.guild
        if not guild:
            print("Guild deu None")
            return
        vc = guild.voice_client
        if not isinstance(vc, discord.VoiceClient):
            print("vc not VoiceClient")
            return
        if not vc:
            if isinstance(interaction.channel, discord.abc.Messageable):
                await interaction.channel.send("Bot não conectado ao voice")
            return
        vc.stop()  # this will trigger the after callback and start the next song
        await interaction.response.send_message("Playing next song.")

class Music(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.music_queues = {}  # {guild_id: [song1, song2, ...]}
        self.loop_status = {}  # {guild_id: False}
        self.last_song = {}  # {guild_id: last_played_song}
        global guild_id
        self.guild_id = guild_id
    
    @commands.hybrid_command()
    async def play(self, ctx: commands.Context, url):
        if guild_id not in self.music_queues:
            self.music_queues[guild_id] = []
        self.music_queues[guild_id].append(url)
        if not ctx.guild:
            print("Guild deu None")
            return
        member = ctx.guild.get_member(ctx.author.id)
        if not member:
            print("Member deu None")
            return
        if not member.voice:
            print("Voice deu None")
            await ctx.send("You are not connected to a voice channel.")
            return
        if not member.voice.channel:
            print("Channel deu None")
            return
        
        
        if ctx.voice_client is None or not isinstance(ctx.voice_client, discord.VoiceClient): #Bot não está conectado, nem tocando música
            vc = await member.voice.channel.connect()
            await self.start_playing(ctx, vc)
        
        
        elif not ctx.voice_client.is_playing(): #bot não está tocando música, mas está conectado
            try:
                vc = await member.voice.channel.connect()
            except:
                vc = ctx.voice_client
            await self.start_playing(ctx, vc)
        
            

    async def start_playing(self, ctx, vc):
        if self.music_queues[guild_id]:
            url = self.music_queues[guild_id].pop(0)
            self.last_song[guild_id] = url
            if not ctx.guild:
                print("Guild deu None")
                return
            member = ctx.guild.get_member(ctx.author.id)
            if not member:
                print("Member deu None")
                return
            if not member.voice:
                print("Voice deu None")
                return
            if not member.voice.channel:
                print("Voice channel deu None")
                return
            
            try: 
                voice_channel = member.voice.channel
                #print("Conectando a canal com música")
                #vc = await voice_channel.connect()
                ydl_opts = YTDL_OPTIONS
                with youtube_dl.YoutubeDL(ydl_opts) as ydl :
                    info = ydl.extract_info(url, download=False)
                    if not info:
                        print("Info None")
                        return
                    url2 = info['formats'][0]['url']
                    vc.play(discord.FFmpegPCMAudio(url2))
                    await ctx.channel.send('**Now playing:** ', view = MusicControls(self.client))
            except Exception as e:
                print(e)
            if self.music_queues[guild_id]:
                ctx.voice_client.after = lambda e: self.start_playing(ctx, vc)
        
        elif self.loop_status.get(guild_id, False):
            self.music_queues[guild_id].append(self.last_song[guild_id])
            await self.start_playing(ctx, vc)

    @commands.hybrid_command()
    async def loop(self, ctx: commands.Context):
        self.loop_status[guild_id] = not self.loop_status.get(guild_id, False)
        status = "enabled" if self.loop_status[guild_id] else "disabled"
        await ctx.send(f"Loop has been {status}.")






async def setup(client): # Must have a setup function
    client.add_view(MusicControls(client))
    await client.add_cog(Music(client)) # Add the class to the cog.