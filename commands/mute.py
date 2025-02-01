import discord
from discord import app_commands
import asyncio

def setup(bot):
    muted_users = {}

    async def monitor_mute(guild, user, stop_event):
        while not stop_event.is_set():
            member = guild.get_member(user.id)
            if member and not member.voice.mute:
                try:
                    await member.edit(mute=True)
                except discord.Forbidden:
                    pass
            await asyncio.sleep(1)

    @bot.tree.command(name="mute", description="Włącza wyciszenie użytkownika.")
    @app_commands.describe(user="Osoba, którą chcesz wyciszyć")
    async def mute(interaction: discord.Interaction, user: discord.Member):
        if user.id in muted_users:
            await interaction.response.send_message(f"{user.mention} jest już wyciszony!")
            return

        await user.edit(mute=True)
        stop_event = asyncio.Event()
        muted_users[user.id] = stop_event
        asyncio.create_task(monitor_mute(interaction.guild, user, stop_event))
        await interaction.response.send_message(f"Wyciszono {user.mention}.")
