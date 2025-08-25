import discord
from discord.ext import commands
import requests
import os
from dotenv import load_dotenv

# 🔹 Charger les variables d'environnement
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
API_PASSWORD = os.getenv("API_PASSWORD")
API_URL = os.getenv("API_URL")
ADMIN_IDS = [int(x) for x in os.getenv("ADMIN_IDS").split(",")]

# 🔹 Bot configuration avec message_content intent
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# 🔹 Logs dans console et Discord
def log(ctx, text):
    print(text)
    # tu peux ajouter un channel spécifique pour logs si tu veux

# 🔹 Commande ping
@bot.command()
async def ping(ctx):
    await ctx.send("Pong 🏓")

# 🔹 Commande générer clé
@bot.command()
async def genkey(ctx):
    if ctx.author.id not in ADMIN_IDS:
        await ctx.send("❌ Tu n'as pas l'autorisation d'utiliser cette commande.")
        return
    try:
        response = requests.post(API_URL, json={"admin_password": API_PASSWORD})
        if response.status_code == 200:
            key = response.json().get("key")
            if key:
                await ctx.send(f"✅ Clé générée : **{key}**")
                log(ctx, f"Clé générée pour {ctx.author}: {key}")
            else:
                await ctx.send("❌ API OK mais aucune clé reçue.")
        else:
            await ctx.send(f"❌ Erreur API {response.status_code}: {response.text}")
    except Exception as e:
        await ctx.send(f"⚠️ Erreur API : {e}")

# 🔹 Lancement du bot
bot.run(TOKEN)
