import interactions
import time
from interactions import User
from typing import Optional

class VoiceSession:
    def __init__(self, channel: interactions.models.discord.channel.VoiceChannel, start_time: float = time.time(), end_time: float = time.time()):
        self.start_time = start_time
        self.end_time = end_time
        self.channel = channel

    def duration(self) -> float:
        return self.end_time - self.start_time

    def update(self):
        self.end_time = time.time()

    def to_dict(self):
        return {
            'start_time': self.start_time,
            'end_time': self.end_time,
            'channel': str(self.channel),
        }

    @staticmethod
    def from_dict(data):
        # channel is not restored as object, just as name
        return VoiceSession(channel=data.get('channel', 'Unknown'), start_time=data['start_time'], end_time=data['end_time'])

class UserData:
    def __init__(self, username: str):
        self.username = username
        self.voice_sessions = []

        self.active_session: Optional[VoiceSession] = None

    def add_voice_session(self, session: VoiceSession):
        self.voice_sessions.append(session)

    def start_voice_session(self, channel: interactions.models.discord.channel.VoiceChannel):
        self.active_session = VoiceSession(channel)
        self.voice_sessions.append(self.active_session)

    def end_voice_session(self):
        if self.active_session:
            self.active_session.update()
            self.active_session = None

    def total_voice_time(self) -> float:
        return sum(session.duration() for session in self.voice_sessions)

    @property
    def num_sessions(self):
        return len(self.voice_sessions)

    def to_dict(self):
        return {
            'username': self.username,
            'voice_sessions': [s.to_dict() for s in self.voice_sessions],
        }

    @staticmethod
    def from_dict(data):
        user = UserData(data['username'])
        user.voice_sessions = [VoiceSession.from_dict(s) for s in data.get('voice_sessions', [])]
        return user

    def __str__(self):
        return f"User: {self.username}, Voice Time: {self.total_voice_time()} seconds"
