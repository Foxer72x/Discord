import discord

def setup(bot):
    @bot.tree.command(name="join", description="Bot dołącza do kanału głosowego")
    async def join(interaction: discord.Interaction):
        if interaction.user.voice:
            channel = interaction.user.voice.channel
            await channel.connect()
            await interaction.response.send_message(f"Dołączono do kanału {channel.name}")
        else:
            await interaction.response.send_message("Musisz być na kanale głosowym, aby bot mógł dołączyć!")
