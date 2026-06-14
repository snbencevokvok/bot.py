import discord
from discord.ext import commands
import os
import threading
from flask import Flask

# --- KONFIGURÁCIÓ ---
TOKEN = os.getenv('DISCORD_TOKEN')
MEMBER_ROLE_ID = 1481671590189072455

# --- FLASK WEBSZERVER (az ébren tartáshoz) ---
app = Flask('')

@app.route('/')
def home():
    return "Bot is alive!"

def run_flask():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

# Szerver elindítása külön szálon
t = threading.Thread(target=run_flask)
t.start()

# --- BOT BEÁLLÍTÁS ---
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)
active_members = set()

# --- GOMB LOGIKA ---
class ActivityView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="I'm Active", style=discord.ButtonStyle.green, custom_id="persistent_active_button")
    async def active_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Defer: jelzi a Discordnak, hogy a bot dolgozik, nem fagyott le
        await interaction.response.defer(ephemeral=True)
        active_members.add(interaction.user.id)
        await interaction.followup.send("Aktivitásod rögzítve.", ephemeral=True)

    @discord.ui.button(label="View Report", style=discord.ButtonStyle.blurple, custom_id="persistent_report_button")
    async def report_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)
        # Ide írhatod a jelentés lekérdezésének logikáját
        await interaction.followup.send("Jelentés előkészítve.", ephemeral=True)

@bot.event
async def on_ready():
    bot.add_view(ActivityView())
    print(f'{bot.user} online!')

bot.run(TOKEN)
