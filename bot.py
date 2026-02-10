import discord
from discord.ext import commands
import asyncio
import random
import os

intents = discord.Intents.default()
intents.members = True
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents)

# --- [คลังเสียงสุ่ม] ---
NA_KHOM_RANDOM = [
    "https://www.myinstants.com/media/sounds/khm-ayaa.mp3",
    "https://www.myinstants.com/media/sounds/nakhom1.mp3",
    "https://www.myinstants.com/media/sounds/nakhom2_8H96i8e.mp3"
]

Siren_Sound = [
    "https://www.myinstants.com/media/sounds/999-social-credit-siren-82729.mp3",
    "https://www.myinstants.com/media/sounds/siren-dog-made-with-Voicemod.mp3"
]

# --- [ตั้งค่ารายคน] ---
USER_SOUNDS = {
    1242809444631449683: "https://www.myinstants.com/media/sounds/harry-maguireeeeeeeee-53526.mp3",
    1383745754996281405: "Random_Siren"
}

@bot.event
async def on_voice_state_update(member, before, after):
    if member.id == bot.user.id: return
    if before.channel is None and after.channel is not None:
        selected_sound = None
        
        if member.id in USER_SOUNDS:
            if USER_SOUNDS[member.id] == "Random_Siren":
                selected_sound = random.choice(Siren_Sound)
            else:
                selected_sound = USER_SOUNDS[member.id]
        else:
            selected_sound = random.choice(NA_KHOM_RANDOM)

        try:
            vc = await after.channel.connect()
            # บน Render ใช้ executable="ffmpeg" หรือไม่ต้องใส่ก็ได้ถ้าตั้ง Build Command ถูก
            vc.play(discord.FFmpegPCMAudio(selected_sound, options='-filter:a "volume=0.5"'))
            
            counter = 0
            while vc.is_playing() and counter < 7:
                await asyncio.sleep(1)
                counter += 1
            
            if vc.is_playing(): vc.stop()
            await vc.disconnect()
        except Exception as e:
            print(f"Error: {e}")
            if member.guild.voice_client: await member.guild.voice_client.disconnect()

# ดึง Token จาก Environment ของ Render เท่านั้น
token = os.getenv("DISCORD_TOKEN")
bot.run(token)