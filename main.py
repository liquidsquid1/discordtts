# Imports

from nextcord.ext import commands
import nextcord
import asyncio
import json
import os

bot = commands.Bot(command_prefix="tts>", intents = nextcord.Intents.all()) # Create instance of a NextCord bot

# Load JSON
with open('config.json') as f:
    data = json.load(f)

# Store JSON values
guild = data["GUILD"]
log_channel = data["LOG_CHANNEL"]
bot_admin = data["TTS_ROLE"]

@bot.event
async def on_ready():
    print("Waiting for ASYNCIO")
    await asyncio.sleep(1)
    if bot.user:
        print(f"> logged in as {bot.user}")
        await bot.get_channel(log_channel).send(f"Bot is online as {bot.user}")
        await bot.change_presence(
            activity = nextcord.Activity(
                type = nextcord.ActivityType.playing,
                name="TTS"
            ))

for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")

@bot.command()
async def reload(ctx):
    role = nextcord.utils.get(ctx.guild.roles, id=bot_admin)
    if role in ctx.author.roles:
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                bot.reload_extension(f"cogs.{filename[:-3]}")
        await ctx.send("Reloaded cogs!")

if __name__ == "__main__":
    bot.run(data["TOKEN"])