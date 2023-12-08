from nextcord import slash_command
from nextcord.ext import commands
import nextcord
from gtts import gTTS
import json

with open('config.json') as f:
  data = json.load(f)

bot_admin = data["BOT_ADMINISTRATOR"]

class TTS(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
  @slash_command(
    name="speak",
    description="uses gTTS to speak",
    guild_ids=[data["GUILD"]])
  async def speak(self, interaction, speech):
    role = nextcord.utils.get(interaction.guild.roles, id=bot_admin)
    if role in interaction.user.roles:
        user = interaction.user
        if user.voice != None:
          try:
            vc = await user.voice.channel.connect()
          except:
            vc = interaction.guild.voice_client
          sound = gTTS(text=speech, lang="en", slow=False)
          sound.save("tts-audio.mp3")

          if vc.is_playing():
            vc.stop()

          source = await nextcord.FFmpegOpusAudio.from_probe("tts-audio.mp3", method="fallback")
          await interaction.response.send_message(
            content = "Playing!",
            ephemeral = True
          )
          vc.play(source)
        else:
          await interaction.response.send_message(
            content = "You're not in a vc!",
            ephemeral = True
          )

def setup(bot):
  bot.add_cog(TTS(bot))