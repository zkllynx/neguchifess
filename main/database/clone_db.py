# (©)Codexbotz
# Recode by @npdkdev
# t.me/DkManSupport

from typing import Union
import threading
from pymongo import MongoClient
import config

client = MongoClient(config.db_url)
db = client["guchi_clone"]

INSERTION_LOCK = threading.RLock()


class User:
    user_id: int
    username: str

    def __init__(self, user_id, username):
        self.user_id = user_id
        self.username = username


class Owner:
    user_id: int
    username: str
    channel_1: int
    channel_2: int
    channel_tf: int
    channel_log: int
    token: str
    status: bool
    hashtag: str

    def __init__(self, user_id, username, channel_1, channel_2, channel_tf, channel_log, hashtag, token, status):
        self.user_id = user_id
        self.username = username
        self.channel_1 = channel_1
        self.channel_2 = channel_2
        self.channel_tf = channel_tf
        self.channel_log = channel_log
        self.hashtag = hashtag
        self.token = token
        self.status = status

    def __dict__(self):
        return {
            "user_id": self.user_id,
            "username": self.username,
            "channel_1": self.channel_1,
            "channel_2": self.channel_2,
            "channel_tf": self.channel_tf,
            "channel_log": self.channel_log,
            "hashtag": self.hashtag,
            "token": self.token,
            "status": self.status
        }


class Clone:
    col = db['clone']
    owner: int

    def __init__(self, user_id: int):
        self.owner = user_id

    async def get_clone(self) -> Union[None, Owner]:
        user = self.col.find_one({'user_id': self.owner})
        if user:
            return Owner(**user)
        else:
            return None

    async def update(self, user_id, **kwargs):
        self.col.update_one(
            {"user_id": user_id},
            {"$set": kwargs}
        )

    async def takedown(self):
        self.col.update_one(
            {"user_id": self.owner},
            {"$set": {
                "status": False
            }}
        )

    async def up(self):
        self.col.update_one(
            {"user_id": self.owner},
            {"$set": {
                "status": True
            }}
        )

    async def add_clone(self, owner: Owner) -> bool:
        with INSERTION_LOCK:
            user = self.col.find_one({'user_id': self.owner})
            if not user:
                self.col.insert_one(owner.__dict__())
                return True
            else:
                return False

    async def delete_clone(self) -> bool:
        with INSERTION_LOCK:
            user = self.col.find_one({'user_id': self.owner})
            if user:
                self.col.delete_one({'user_id': self.owner})
                return True
            else:
                return False

    async def full_clone(self) -> list[Owner]:
        get_clone = self.col.find()
        clone_own = []
        for clone in get_clone:
            clone_own.append(
                Owner(
                    clone['user_id'],
                    clone['username'],
                    clone['channel_1'],
                    clone['channel_2'],
                    clone['channel_tf'],
                    clone['channel_log'],
                    clone['hashtag'],
                    clone['token'],
                    clone['status']
                )
            )
        return clone_own

    async def query_clone(self):
        clone = self.col.find().sort('user_id')
        return [clone['user_id'] for clone in clone]