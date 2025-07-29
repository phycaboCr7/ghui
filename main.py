import os
import discord
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-pro")
intents = discord.Intents.default()
intents.messages = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("!ask"):
        prompt = message.content[5:].strip()
        if prompt:
            try:
                response = model.generate_content(prompt)
                await message.channel.send(response.text)
            except Exception as e:
                await message.channel.send("Error: " + str(e))
        else:
            await message.channel.send("Please provide a prompt after !ask")

client.run(TOKEN)