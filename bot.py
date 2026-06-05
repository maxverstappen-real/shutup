import os
import random
import discord
from discord import app_commands
from discord.ext import commands

# 1. Set up permissions
intents = discord.Intents.default()
intents.message_content = True

# We use commands.Bot here because it allows the bot to register Slash Commands
bot = commands.Bot(command_prefix="!", intents=intents)

# Exact filenames from your iOS Files app
IMAGE_COMMON = 'IMAGE_COMMON.JPEG'
IMAGE_RARE = 'IMAGE_RARE.png'

# The master switch: Starts as False (OFF) so it doesn't spam instantly
auto_reply_active = False

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    try:
        # This registers the slash commands (/shutup and /talk) to Discord
        synced = await bot.tree.sync()
        print(f"Successfully synced {len(synced)} slash command(s).")
    except Exception as e:
        print(f"Failed to sync slash commands: {e}")

# Command 1: /shutup
@bot.tree.command(name="shutup", description="Activate the automatic shut up replies")
async def shutup(interaction: discord.Interaction):
    global auto_reply_active
    auto_reply_active = True
    await interaction.response.send_message("🔴 Auto-reply activated! I am now monitoring chat.")

# Command 2: /talk
@bot.tree.command(name="talk", description="Deactivate the automatic shut up replies")
async def talk(interaction: discord.Interaction):
    global auto_reply_active
    auto_reply_active = False
    await interaction.response.send_message("🟢 Auto-reply deactivated! You are allowed to speak again.")

@bot.event
async def on_message(message):
    # Prevent the bot from replying to itself
    if message.author == bot.user:
        return

    # If the switch is turned OFF, ignore all incoming messages
    if not auto_reply_active:
        return

    # Roll a random decimal between 0.0 and 1.0
    roll = random.random()

    # 0.5% chance for the rare image
    if roll < 0.005:
        selected_image = IMAGE_RARE
    else:
        selected_image = IMAGE_COMMON

    try:
        with open(selected_image, 'rb') as f:
            picture = discord.File(f)
            await message.reply(content=f"shut up {message.author.mention}", file=picture)
    except FileNotFoundError:
        print(f"Error: Could not find '{selected_image}' in the folder.")

# Grab the token from JustRunMy.App settings
token = 'MTUxMjEzNzM1NDQ2OTU3Njc0NA.Geu8Aj.mlBtgJDs_ekCJsnUXd9e0Vxk9ySG-adFNt7A1c'
if token:
    bot.run(token)
