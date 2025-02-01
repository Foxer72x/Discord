import discord
from discord import app_commands
import psutil
from datetime import datetime, timedelta

def setup(bot):
    start_time = datetime.utcnow()

    @bot.tree.command(name="info", description="Wyświetla informacje o bocie.")
    async def info(interaction: discord.Interaction):
        uptime = datetime.utcnow() - start_time
        memory = psutil.virtual_memory()
        cpu = psutil.cpu_percent(interval=1)

        embed = discord.Embed(
            title="Informacje o bocie",
            description="Statystyki i informacje",
            color=discord.Color.green()
        )
        embed.add_field(name="Czas działania", value=str(timedelta(seconds=int(uptime.total_seconds()))))
        embed.add_field(name="Zużycie RAM", value=f"{memory.used / (1024**2):.2f} MB")
        embed.add_field(name="Użycie CPU", value=f"{cpu:.2f}%")
        await interaction.response.send_message(embed=embed)
