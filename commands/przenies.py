import discord
from discord import app_commands
from random import choice
import asyncio

# Wspólna lista przenoszonych użytkowników
moving_users = {}

def setup(bot):
    async def move_user_randomly(guild, user, stop_event):
        while not stop_event.is_set():
            voice_channels = [vc for vc in guild.voice_channels if len(vc.members) < vc.user_limit or vc.user_limit == 0]
            if not voice_channels:
                break

            target_channel = choice(voice_channels)
            try:
                await user.move_to(target_channel)
            except discord.Forbidden:
                break
            except discord.HTTPException:
                break

            await asyncio.sleep(0.5)

    @bot.tree.command(name="przenies", description="Przenosi wybranego użytkownika po losowych kanałach głosowych.")
    @app_commands.describe(member="Użytkownik, który ma być przenoszony")
    async def przenies(interaction: discord.Interaction, member: discord.Member):
        if not member.voice or not member.voice.channel:
            await interaction.response.send_message(f"{member.mention} nie znajduje się na kanale głosowym!")
            return

        if member.id in moving_users:
            await interaction.response.send_message(f"{member.mention} już jest przenoszony!")
            return

        stop_event = asyncio.Event()
        moving_users[member.id] = stop_event
        await interaction.response.send_message(f"Rozpoczynam przenoszenie {member.mention}!")
        asyncio.create_task(move_user_randomly(interaction.guild, member, stop_event))
