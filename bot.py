import discord
from discord.ext import tasks, commands
import asyncio
import os

# --- KONFIGURÁCIÓ ---
# A TOKEN-t a Railway-ben fogjuk beállítani a 'Variables' alatt
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
        active_members.add(interaction.user.id)
        await interaction.response.send_message("Aktív státuszod rögzítve.", ephemeral=True)

    @discord.ui.button(label="View Report", style=discord.ButtonStyle.blurple, custom_id="persistent_report_button")
    async def report_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        member_role = interaction.guild.get_role(MEMBER_ROLE_ID)
        
        active = []
        inactive = []

        for member in member_role.members:
            if member.id in active_members:
                active.append(member.display_name)
            else:
                inactive.append(member.display_name)

        report = (
            f"**Aktivitási Jelentés**\n\n"
            f"✅ **Aktív ({len(active)}):** {', '.join(active) if active else 'Senki'}\n\n"
            f"❌ **Inaktív ({len(inactive)}):** {', '.join(inactive) if inactive else 'Senki'}"
        )
        await interaction.response.send_message(report, ephemeral=True)

# --- AUTOMATA FELADAT ---
@tasks.loop(hours=336)
async def activity_check():
    guild = bot.get_guild(GUILD_ID)
    if not guild: return
    channel = guild.get_channel(CHANNEL_ID)
    if not channel: return
    
    active_members.clear()
    await channel.send(
        "**2-hetes Aktivitás Ellenőrzés**\n\n"
        "Kérlek, nyomd meg az 'I'm Active' gombot a következő 14 napban. "
        "Ha nem teszed, automatikusan Visitor rangra kerülsz.",
        view=ActivityView()
    )

    await asyncio.sleep(14 * 24 * 60 * 60) 

    member_role = guild.get_role(MEMBER_ROLE_ID)
    visitor_role = guild.get_role(VISITOR_ROLE_ID)

    if member_role:
        for member in member_role.members:
            if member.id not in active_members:
                await member.remove_roles(member_role)
                await member.add_roles(visitor_role)
                try:
                    await member.send("Nem igazoltad az aktivitásod, így átkerültél Visitor rangra.")
                except:
                    pass

@bot.event
async def on_ready():
    print(f"Bot bejelentkezett: {bot.user}")
    bot.add_view(ActivityView()) 
    if not activity_check.is_running():
        activity_check.start()

bot.run(TOKEN)
