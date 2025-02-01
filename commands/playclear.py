import discord
from discord import app_commands

queue = []  # Globalna kolejka

def setup(bot):
    @bot.tree.command(name="playclear", description="Czyści kolejkę odtwarzania")
    async def playclear(interaction: discord.Interaction):
        global queue
        queue.clear()
        await interaction.response.send_message("Kolejka została wyczyszczona.")
