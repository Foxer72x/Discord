import discord
from discord.ext import commands
import os
from bot_token import TOKEN  # Token bota

intents = discord.Intents.default()
intents.messages = True  # Dodaj intencje potrzebne dla Twojego bota

bot = commands.Bot(command_prefix="!", intents=intents)

# Automatyczne ładowanie komend z folderu "commands"
def load_commands():
    commands_folder = "./commands"
    for filename in os.listdir(commands_folder):
        if filename.endswith(".py"):
            module_name = filename[:-3]  # Usunięcie rozszerzenia .py
            try:
                # Importowanie modułu z folderu "commands"
                module = __import__(f"commands.{module_name}", fromlist=[module_name])
                # Rejestracja komendy w bocie
                if hasattr(module, "setup"):
                    module.setup(bot)
                    print(f"Załadowano moduł: {module_name}")
            except Exception as e:
                print(f"Błąd podczas ładowania modułu {module_name}: {e}")

# Wydarzenie uruchamiane, gdy bot jest gotowy
@bot.event
async def on_ready():
    print(f"Bot jest online jako {bot.user}")
    # Synchronizacja komend aplikacji
    await bot.tree.sync()

# Załaduj wszystkie komendy
load_commands()

# Uruchomienie bota
bot.run(TOKEN)
