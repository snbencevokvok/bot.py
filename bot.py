import discord
from discord.ext import tasks, commands
import asyncio
import os

# --- KONFIGURÁCIÓ ---
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_ID = 1470064782471200987
CHANNEL_ID = 1511071871465029632
MEMBER_ROLE_ID = 1481671590189072455
VISITOR_ROLE_ID = 1481673410789642240

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.presences = True

bot = commands.Bot(command_prefix="!", intents=intents)
active_members = set()

# --- GOMB LOGIKA ---
class ActivityView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="I'm Active", style=discord.ButtonStyle.green, custom_id="persistent_active_button")
    async def active_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Jelzi a Discordnak, hogy megkaptuk az interakciót, ezzel elkerüljük a "Sikertelen interakció" hibát
        await interaction.response.defer(ephemeral=True)
        
        active_members.add(interaction.user.id)
        
        # Utólagos válasz
        await interaction.followup.send("Aktivitásod rögzítve.", ephemeral=True)

    @discord.ui.button(label="View Report", style=discord.ButtonStyle.blurple, custom_id="persistent_report_button")
    async def report_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Jelzi a Discordnak, hogy megkaptuk az interakciót
        await interaction.response.defer(ephemeral=True)
        
        member_role = interaction.guild.get_role(MEMBER_ROLE_ID)
        # Itt folytatódik a többi logikád...
        
        await interaction.followup.send("Jelentés előkészítve.", ephemeral=True)

@bot.event
async def on_ready():
    # Regisztráljuk a nézetet, hogy a gombok újraindulás után is működjenek
    bot.add_view(ActivityView())
    print(f'{bot.user} online és készen áll!')

bot.run(TOKEN)
