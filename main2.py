import random
import discord
from discord.ext import commands
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import requests
from datetime import datetime, timedelta
import asyncio, os
from dotenv import load_dotenv
load_dotenv()


intents = discord.Intents.default()
intents.voice_states = True

bot = commands.Bot(command_prefix='/', intents=intents)

SPOTIFY_CLIENT_ID = os.getenv("s_id")
SPOTIFY_CLIENT_SECRET = os.getenv("s_s")
TOKEN = os.getenv("moj_token")

spotify_client_credentials_manager = SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET)
spotify = spotipy.Spotify(client_credentials_manager=spotify_client_credentials_manager)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.command()
async def join(ctx, channel_id):
    channel = discord.utils.get(ctx.guild.voice_channels, id=int(1099957202871136316))
    voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)

    if voice_client and voice_client.is_connected():
        await voice_client.move_to(channel)
    else:
        voice_client = await channel.connect()

@bot.command()
async def play(ctx, duration: float):
    voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if not voice_client or not voice_client.is_connected():
        await ctx.send("I'm not connected to a voice channel.")
        return
    if duration == 1:
        trajanje = 0.1
        točke = 5
    elif duration == 2:
        trajanje = 1
        točke = 2
    elif duration == 3:
        trajanje = 5
        točke = 1
    # Get the playlist tracks
    playlist_tracks = spotify.playlist_tracks("https://open.spotify.com/playlist/5ABHKGoOzxkaa28ttQV9sE?si=8547bbaf974c4994")

    # Extract the titles of the songs
    song_titles = [track['track']['name'] for track in playlist_tracks['items']]

    # Choose a random song
    random_title = random.choice(song_titles)

    # Search for the chosen song on Spotify
    search_results = spotify.search(random_title, type='track', limit=1)

    # Get the audio file URL of the first search result
    audio_url = search_results['tracks']['items'][0]['preview_url']

    response = requests.get(audio_url)
    with open("downloaded_song.mp3", 'wb') as file:
        file.write(response.content)

    # Play the downloaded audio file
    voice_client.play(discord.PCMVolumeTransformer(discord.FFmpegPCMAudio("downloaded_song.mp3")), after=lambda e: asyncio.run_coroutine_threadsafe(voice_client.disconnect()))
    await asyncio.sleep(trajanje)
    voice_client.stop()


@bot.command()
async def leave(ctx):
    voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice_client and voice_client.is_connected():
        await voice_client.disconnect()
    else:
        await ctx.send("I'm not connected to a voice channel.")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if bot.user.mentioned_in(message):
        await bot.process_commands(message)

bot.run(TOKEN)
