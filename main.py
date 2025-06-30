import interactions
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")

bot = interactions.Client(intents=interactions.Intents.ALL)

@interactions.listen()
async def on_startup():
    print("Bot started!")

@interactions.listen(interactions.events.VoiceUserJoin)
async def on_voice_user_join(event):
    print(f"{event.user} joined {event.channel}")

@interactions.listen(interactions.events.VoiceUserLeave)
async def on_voice_user_leave(event):
    print(f"{event.user} left {event.channel}")


bot.start(TOKEN)
