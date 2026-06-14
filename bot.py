import discord
from discord.ext import commands
import os
import threading
from flask import Flask

# --- KONFIGURÁCIÓ ---
TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_ID = 1511071871465029632 # Ellenőrizd, hogy ez a jó csatorna ID!

# --- FLASK WEBSZERVER ---
app = Flask('')

@app.route('/')
def home():
    return "Bot is alive!"

def run_flask():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

# Szerver indítása külön szálon
threading.Thread(target=run_flask).start()

# --- BOT BEÁLLÍTÁS ---
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# --- GOMB LOGIKA ---
class ActivityView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None) # Timeout=None: a gomb örökre aktív marad

    @discord.ui.button(label="I'm Active", style=discord.ButtonStyle.green, custom_id="persistent_active_button")
    async def active_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)
        # Itt rögzítheted az aktivitást (pl. egy listába vagy adatbázisba)
        await interaction.followup.send("Aktivitásod rögzítve.", ephemeral=True)

    @discord.ui.button(label="View Report", style=discord.ButtonStyle.blurple, custom_id="persistent_report_button")
    async def report_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)
        await interaction.followup.send("Jelentés előkészítve.", ephemeral=True)

@bot.event
async def on_ready():
    # Gombok regisztrálása
    bot.add_view(ActivityView())
    print(f'{bot.user} online!')
    
    # Automatikus üzenet küldése (opcionális, ha tesztelni akarod)
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        await channel.send("2-hetes Aktivitás Ellenőrzés\nKérlek, nyomd meg a gombot:", view=ActivityView())

# --- INDÍTÁS ---
bot.run(TOKEN)
