import discord
from discord import app_commands
import asyncio

# Używamy tej samej listy co w `przenies.py`
from commands.przenies import moving_users

def setup(bot):
    @bot.tree.command(name="zatrzymaj", description="Zatrzymuje przenoszenie użytkownika po kanałach.")
    @app_commands.describe(member="Użytkownik, którego przenoszenie ma zostać zatrzymane")
    async def zatrzymaj(interaction: discord.Interaction, member: discord.Member):
        if member.id not in moving_users:
            await interaction.response.send_message(f"{member.mention} nie jest przenoszony!")
            return

        # Zatrzymanie procesu przenoszenia
        moving_users[member.id].set()
        del moving_users[member.id]
        await interaction.response.send_message(f"Zatrzymano przenoszenie {member.mention}!")
