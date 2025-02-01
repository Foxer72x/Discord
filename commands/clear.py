import discord
from discord import app_commands

def setup(bot):

    @bot.tree.command(name="clear", description="Usuwa określoną liczbę wiadomości z kanału.")
    async def clear(interaction: discord.Interaction, ilość: int):
        """
        Komenda usuwająca określoną liczbę wiadomości z kanału tekstowego, z wyjątkiem komendy.
        """
        # Sprawdzenie, czy użytkownik ma odpowiednie uprawnienia
        if not interaction.user.guild_permissions.manage_messages:
            await interaction.response.send_message("Nie masz uprawnień do usuwania wiadomości.", ephemeral=True)
            return

        # Sprawdzenie, czy liczba wiadomości jest poprawna
        if ilość < 1 or ilość > 100:
            await interaction.response.send_message("Podaj liczbę wiadomości do usunięcia w zakresie od 1 do 100.", ephemeral=True)
            return

        # Uzyskanie kanału tekstowego, na którym komenda została wywołana
        channel = interaction.channel

        try:
            # Usuwanie wiadomości (z wyjątkiem komendy)
            messages = []
            async for message in channel.history(limit=ilość + 1):
                if message.author != bot.user:  # Pomijanie wiadomości bota
                    messages.append(message)
            
            # Usuwanie zebranych wiadomości
            for message in messages:
                await message.delete()

            # Wysyłanie komunikatu w postaci embeda po wyczyszczeniu czatu
            embed = discord.Embed(
                title="Czat został wyczyszczony!",
                description=f"Czat został wyczyszczony przez {interaction.user.mention}.",
                color=discord.Color.orange()  # Kolor przypominający kolor lisa
            )
            # Wysyłanie wiadomości z embedem
            await interaction.followup.send(embed=embed, ephemeral=True)
        except discord.errors.Forbidden:
            # Wysyłanie komunikatu o braku uprawnień
            await interaction.response.send_message("Nie mogę usunąć wiadomości, brak odpowiednich uprawnień.", ephemeral=True)
        except Exception as e:
            # Wysyłanie komunikatu o błędzie
            await interaction.response.send_message(f"Wystąpił błąd: {e}", ephemeral=True)
