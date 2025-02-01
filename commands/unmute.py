import discord
from discord import app_commands

def setup(bot):
    muted_users = {}

    @bot.tree.command(name="unmute", description="Wyłącza wyciszenie użytkownika.")
    @app_commands.describe(user="Osoba, której chcesz wyłączyć wyciszenie")
    async def unmute(interaction: discord.Interaction, user: discord.Member):
        if user.id not in muted_users:
            await interaction.response.send_message(f"{user.mention} nie jest wyciszony!")
            return

        await user.edit(mute=False)
        muted_users[user.id].set()
        del muted_users[user.id]
        await interaction.response.send_message(f"Odciszono {user.mention}.")
