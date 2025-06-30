import interactions
import time
from interactions import User
from typing import Optional

class VoiceSession:
    def __init__(self, channel: interactions.models.discord.channel.VoiceChannel, start_time: float, end_time: float = time.time()):
        self.start_time = start_time
        self.end_time = end_time
        self.channel = channel

    def duration(self) -> float:
        return self.end_time - self.start_time

    def update(self):
        self.end_time = time.time()

class UserData:
    def __init__(self, username: str):
        self.username = username
        self.voice_sessions = []

        self.active_session: Optional[VoiceSession] = None

    def add_voice_session(self, session: VoiceSession):
        self.voice_sessions.append(session)

    def start_voice_session(self, channel: interactions.models.discord.channel.VoiceChannel):
        self.active_session = VoiceSession(channel, time.time())
        self.voice_sessions.append(self.active_session)

    def end_voice_session(self):
        if self.active_session:
            self.active_session.update()
            self.active_session = None

    def total_voice_time(self) -> float:
        return sum(session.duration() for session in self.voice_sessions)

    def __str__(self):
        return f"User: {self.username}, Voice Time: {self.total_voice_time()} seconds"
