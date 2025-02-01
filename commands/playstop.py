import discord

def setup(bot):
    @bot.tree.command(name="playstop", description="Zatrzymaj odtwarzanie dźwięku")
    async def playstop(interaction: discord.Interaction):
        voice_client = interaction.guild.voice_client

        if voice_client and voice_client.is_playing():
            voice_client.stop()
            await interaction.response.send_message("Zatrzymano odtwarzanie dźwięku.")
        else:
            await interaction.response.send_message("Bot nie odtwarza żadnego dźwięku.")
