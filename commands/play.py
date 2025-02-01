import discord
from discord import app_commands
from yt_dlp import YoutubeDL
import asyncio

# Kolejka odtwarzania
queue = []

# Funkcja pobierająca URL audio z YouTube
def get_audio_url(url):
    """
    Funkcja pobiera URL do pliku audio z YouTube za pomocą yt_dlp.
    """
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': False,  # Włącz logi yt-dlp
        'noplaylist': True,
        'geo-bypass': True,
        'no-check-certificate': True,
        'logtostderr': True,  # Logi do stderr
        'verbose': True  # Włączenie bardziej szczegółowych logów
    }
    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return info['url']
    except Exception as e:
        raise RuntimeError(f"Błąd podczas pobierania audio: {e}")

# Ustawienia bota
def setup(bot):

    async def play_next(voice_client):
        """
        Odtwarza kolejny utwór z kolejki.
        """
        if queue:
            next_url = queue.pop(0)
            ffmpeg_path = "D:/ffmpeg/bin/ffmpeg.exe"  # Zmień ścieżkę, jeśli potrzebne
            try:
                # Dodanie opcji debugowania oraz wyłączenie wideo
                source = discord.FFmpegPCMAudio(
                    next_url, 
                    executable=ffmpeg_path, 
                    options="-vn -loglevel debug"
                )
                voice_client.play(
                    source,
                    after=lambda e: asyncio.run_coroutine_threadsafe(play_next_safe(voice_client), bot.loop)
                )
            except Exception as e:
                print(f"Błąd podczas odtwarzania: {e}")

    async def play_next_safe(voice_client):
        """
        Bezpieczne wywołanie kolejnego utworu w pętli asynchronicznej.
        """
        try:
            await play_next(voice_client)
        except Exception as e:
            print(f"Błąd w play_next_safe: {e}")

    @bot.tree.command(name="play", description="Odtwórz dźwięk z YouTube z podanego linku")
    async def play(interaction: discord.Interaction, url: str):
        voice_client = interaction.guild.voice_client

        # Jeśli bot nie jest na kanale głosowym, połącz go
        if not voice_client:
            if interaction.user.voice and interaction.user.voice.channel:
                channel = interaction.user.voice.channel
                voice_client = await channel.connect()
            else:
                await interaction.response.send_message("Musisz być na kanale głosowym, aby użyć tej komendy!")
                return

        await interaction.response.defer()  # Opóźnienie odpowiedzi, aby uniknąć timeoutu

        try:
            # Pobierz URL do audio i dodaj do kolejki
            audio_url = get_audio_url(url)
            queue.append(audio_url)
            print(f"URL dodany do kolejki: {audio_url}")
            
            # Rozpocznij odtwarzanie, jeśli bot nie gra
            if not voice_client.is_playing():
                await play_next(voice_client)

            await interaction.followup.send(f"Dodano do kolejki: {url}")
        except RuntimeError as e:
            await interaction.followup.send(f"Błąd przy pobieraniu audio: {e}")
        except Exception as e:
            await interaction.followup.send(f"Wystąpił nieoczekiwany błąd: {e}")
