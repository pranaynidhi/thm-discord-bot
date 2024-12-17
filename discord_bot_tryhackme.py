import discord
from discord.ext import commands
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()
DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
API_ENDPOINT = os.getenv('API_ENDPOINT')

# Initialize bot with a command prefix
intents = discord.Intents.all()  # Enable all intents
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Bot is ready and logged in as {bot.user}')

# Command to fetch user rank
@bot.command()
async def rank(ctx, username: str):
    """Fetch and display the TryHackMe rank of a user."""
    try:
        response = requests.get(f'{API_ENDPOINT}/api/rank/{username}')
        if response.status_code == 200:
            data = response.json()
            badges = data.get('badges', [])
            embed = discord.Embed(title=f"TryHackMe Rank for {username}", color=0x00ff00)
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"Could not fetch data for user {username}. Ensure the username is correct.")
    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}")

# Command to show new rooms
@bot.command()
async def newrooms(ctx):
    """Display the recently added TryHackMe rooms."""
    try:
        response = requests.get(f'{API_ENDPOINT}/api/new-rooms')
        if response.status_code == 200:
            data = response.json()
            embed = discord.Embed(title="New Rooms on TryHackMe", color=0x00ff00)
            for room in data:
                embed.add_field(name=room['title'], value=f"Code: {room['code']}, Creator: {room['creator']}", inline=False)
            await ctx.send(embed=embed)
        else:
            await ctx.send("Failed to fetch new rooms.")
    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}")

# Command to recommend rooms
@bot.command()
async def recommend(ctx):
    """Display recommended rooms."""
    try:
        response = requests.get(f'{API_ENDPOINT}/recommend/last-room?type=json')
        if response.status_code == 200:
            data = response.json()
            embed = discord.Embed(title="Recommended Rooms", color=0x00ff00)
            for room in data:
                embed.add_field(name=room['roomCode'], value=f"Last Action: {room['lastAction']}", inline=False)
            await ctx.send(embed=embed)
        else:
            await ctx.send("Failed to fetch recommended rooms.")
    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}")

# Command to fetch leaderboard
@bot.command()
async def leaderboard(ctx, room_code: str):
    """Display the leaderboard for a specific room."""
    try:
        response = requests.get(f'{API_ENDPOINT}/api/room/scoreboard?code={room_code}&limit=10')
        if response.status_code == 200:
            data = response.json()
            embed = discord.Embed(title=f"Leaderboard for Room: {room_code}", color=0x00ff00)
            for user in data:
                embed.add_field(name=user['username'], value=f"Rank: {user['rank']}, Score: {user['score']}", inline=False)
            await ctx.send(embed=embed)
        else:
            await ctx.send("Failed to fetch leaderboard data.")
    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}")

# Command to fetch room details
@bot.command()
async def roomdetails(ctx, room_code: str):
    """Display details of a specific room."""
    try:
        response = requests.get(f'{API_ENDPOINT}/api/room/details?codes={room_code}')
        if response.status_code == 200:
            data = response.json()
            room = data.get(room_code, {})
            embed = discord.Embed(title=f"Details for Room: {room.get('title', 'Unknown')}", color=0x00ff00)
            embed.add_field(name="Description", value=room.get('description', 'No description available.'), inline=False)
            embed.add_field(name="Difficulty", value=room.get('difficulty', 'Unknown'), inline=False)
            embed.add_field(name="Users", value=room.get('users', 0), inline=False)
            await ctx.send(embed=embed)
        else:
            await ctx.send("Failed to fetch room details.")
    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}")

# Run the bot
bot.run(DISCORD_BOT_TOKEN)
