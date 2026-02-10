import discord
from discord.ext import commands
import asyncio
import random
import os

intents = discord.Intents.default()
intents.members = True
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents)

# --- [คลังเสียงน้าค้อมสุ่ม (สำหรับคนทั่วไป)] ---
NA_KHOM_RANDOM = [
    "https://www.myinstants.com/media/sounds/khm-ayaa.mp3",
    "https://www.myinstants.com/media/sounds/nakhom1.mp3",
    "https://www.myinstants.com/media/sounds/nakhom2_8H96i8e.mp3",
    "https://www.myinstants.com/media/sounds/nakhom-3.mp3",
    "https://www.myinstants.com/media/sounds/nakhom-5.mp3"
]

# --- [เพิ่มลิสต์เสียง Siren ตามภาพที่คุณส่งมา] ---
Siren_Sound = [
    "https://tuna.voicemod.net/sound/24c6bb11-f129-43e6-906e-ba0294d3d77b",
    r"/workspaces/SoundDiscord/siren-dog-made-with-Voicemod.mp3" # แก้ลิงก์ให้เป็น .mp3 เพื่อให้เล่นได้
]

# --- [ตั้งค่าเสียงเฉพาะคน] ---
USER_SOUNDS = {
    1242809444631449683: "https://www.myinstants.com/media/sounds/harry-maguireeeeeeeee-53526.mp3",
    1383745754996281405: "Random_Siren" # ตั้งค่าให้ใช้การสุ่มจากกลุ่ม Siren
}

@bot.event
async def on_voice_state_update(member, before, after):
    if member.id == bot.user.id: return
    
    if before.channel is None and after.channel is not None:
        selected_sound = None
        
        # เช็คเงื่อนไขเสียง
        if member.id in USER_SOUNDS:
            if USER_SOUNDS[member.id] == "Random_Siren":
                selected_sound = random.choice(Siren_Sound)
            else:
                selected_sound = USER_SOUNDS[member.id]
        else:
            # คนทั่วไปสุ่มน้าค้อม
            selected_sound = random.choice(NA_KHOM_RANDOM)

        try:
            vc = await after.channel.connect()
            vc.play(discord.FFmpegPCMAudio(selected_sound, options='-filter:a "volume=0.5"'))
            
            # จำกัดเวลาไม่เกิน 7 วินาที
            counter = 0
            while vc.is_playing() and counter < 7:
                await asyncio.sleep(1)
                counter += 1
            
            if vc.is_playing():
                vc.stop()
                
            await vc.disconnect()
        except Exception as e:
            print(f"Error: {e}")
            if member.guild.voice_client:
                await member.guild.voice_client.disconnect()

bot.run(os.getenv("MTQ2NjQxNzAxMTM5MDQxNDkxMw.Gn6yZ6.W_LYTxpoItyx_oXXijB06O9tm3L0u4IxoJ2pE0"))