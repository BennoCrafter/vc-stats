import interactions
from interactions.models.discord.channel import VoiceChannel
from src.user_data import UserData
import json
from pathlib import Path

database_path: Path = Path("database.json")

class Database:
    def __init__(self):
        self.users: list[UserData] = []

    def add_user(self, user: UserData):
        self.users.append(user)
        return user

    def remove_user(self, user: UserData):
        self.users.remove(user)

    def update_user(self, user: UserData):
        self.users[self.users.index(user)] = user

    def get_user(self, username: str) -> UserData:
        for user in self.users:
            if user.username == username:
                return user

        return self.add_user(UserData(username))

    def start_voice_session(self, username: str, channel: interactions.models.discord.channel.VoiceChannel):
        user = self.get_user(username)
        user.start_voice_session(channel)

    def end_voice_session(self, username: str):
        user = self.get_user(username)
        user.end_voice_session()

    @classmethod
    def load(cls) -> 'Database':
        db = cls()
        users = Database._load_users()
        for user in users:
            db.add_user(user)
        return db

    @staticmethod
    def _load_users() -> list[UserData]:
        try:
            with open(database_path, "r") as f:
                data = json.load(f)
                return [UserData(**user_dict) for user_dict in data]
        except FileNotFoundError:
            database_path.write_text("[]")
            return []

    def write(self):
        with open(database_path, "w") as f:
            json.dump([user.__dict__ for user in self.users], f, indent=2)
