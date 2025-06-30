import interactions
from interactions import Task, IntervalTrigger
from typing import Optional, Union
from interactions import slash_command, SlashContext, SlashCommandOption, OptionType, User, Member

import os
from dotenv import load_dotenv
import time

from src.user_data import UserData, VoiceSession

from src.database_io import Database

load_dotenv()
TOKEN = os.getenv("TOKEN")

bot = interactions.Client(intents=interactions.Intents.DEFAULT)

database: Database = Database.load()

@interactions.listen()
async def on_startup():
    print("Bot started!")
    update_voice_sessions.start()

@Task.create(IntervalTrigger(minutes=1))
async def update_voice_sessions():
    for user_data in database.users:
        if user_data.active_session:
            user_data.active_session.update()

@interactions.listen(interactions.events.VoiceUserJoin)
async def on_voice_user_join(event: interactions.events.VoiceUserJoin):
    print(f"{event.author} joined {event.channel}")
    database.start_voice_session(event.author.username, event.channel)
    database.write()

@interactions.listen(interactions.events.VoiceUserLeave)
async def on_voice_user_leave(event: interactions.events.VoiceUserLeave):
    print(f"{event.author} left {event.channel}")
    database.end_voice_session(event.author.username)
    database.write()

@slash_command(
    name="vc-stats",
    description="Voice channel statistics",
    options=[
        SlashCommandOption(
            name="user",
            description="Optional user",
            type=OptionType.USER,
            required=False
        )
    ]
)
async def vc_stats(ctx: SlashContext, user: Optional[Union[User, Member]] = None):
    user = user or ctx.author
    user_data = database.get_user(user.username)
    total_seconds = int(user_data.total_voice_time())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    num_sessions = len(user_data.voice_sessions)
    msg = (
        f"**Voice Stats for {user.username}:**\n"
        f"Total Time: **{hours}h {minutes}m {seconds}s**\n"
        f"Sessions: **{num_sessions}**"
    )
    await ctx.send(msg)

bot.start(TOKEN)
