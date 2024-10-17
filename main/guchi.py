import traceback

import config, sys, os, requests
from main import dbclone, set_main_bot
from main.database.clone_db import Owner

from main.helpers import Database
from pyrogram import Client
from pyrogram.types import BotCommand, BotCommandScopeAllPrivateChats

data = []


class Guchi(Client):
    id_bot = 0
    db_url: str = config.db_url
    channel_log: int = config.channel_log
    channel_1: int = config.channel_1
    channel_2: int = config.channel_2
    channel_tf: int = config.channel_tf
    hashtag: str = config.hastag
    owner: Owner = None
    owner_id: int = 0

    def __init__(self, owner_id: int = 0, token: str = config.bot_token, memory=True, owner: Owner = None):
        name = "menfess" if owner_id == 0 else f"Bot-{owner_id}"
        self.owner = owner
        self.owner_id = owner_id
        if owner:
            self.channel_1 = owner.channel_1
            self.channel_2 = owner.channel_2
            self.channel_tf = owner.channel_tf
            self.channel_log = owner.channel_log
            self.hashtag = owner.hashtag.replace(' ', '|').lower()
        super().__init__(
            name=name,
            api_id=config.api_id,
            api_hash=config.api_hash,
            plugins={
                "root": "menfess.plugins"
            },
            bot_token=token,
            in_memory=memory,
        )

    async def start(self) -> tuple[bool, Client]:
        await super().start()
        bot_me = await self.get_me()
        self.username = bot_me.username
        self.id_bot = bot_me.id
        if self.owner:
            self.owner.username = bot_me.username
            await dbclone.update(self.owner_id, username=bot_me.username)
        if not self.owner:
            set_main_bot(self.id_bot)
        db = Database(bot_me.id, self.id_bot)
        if not await db.cek_user_didatabase():
            print(f'[!] Menambahkan data bot ke database...')
            await db.tambah_databot()
        print("[!] Database telah ready")
        print(f"[!] Link Database Kamu : {self.db_url}")
        print("================")
        print(f"Bot Name: {bot_me.first_name}")

        if self.channel_1:
            try:
                await self.export_chat_invite_link(self.channel_1)
            except Exception:
                print(f'Harap periksa kembali ID [ {self.channel_1} ] pada channel 1')
                print(f'Pastikan bot telah dimasukan kedalam channel dan menjadi admin')
                print('-> Bot terpaksa dihentikan')
                return False, f'Harap periksa kembali ID [ {self.channel_1} ] pada channel 1'
        if self.channel_2:
            try:
                await self.export_chat_invite_link(self.channel_1)
            except:
                print(f'Harap periksa kembali ID [ {self.channel_2} ] pada channel 2')
                print(f'Pastikan bot telah dimasukan kedalam channel dan menjadi admin')
                print('-> Bot terpaksa dihentikan')
                return False, f'Harap periksa kembali ID [ {self.channel_2} ] pada channel 2'
        if self.channel_log:
            try:
                await self.export_chat_invite_link(self.channel_log)
            except:
                print(f'Harap periksa kembali ID [ {self.channel_log} ] pada channel log')
                print(f'Pastikan bot telah dimasukan kedalam channel dan menjadi admin')
                print('-> Bot terpaksa dihentikan')
                return False, f'Harap periksa kembali ID [ {self.channel_log} ] pada channel log'

        data.append(self.id_bot)
        await self.set_bot_commands([
            BotCommand('status', '🍃 check status'), BotCommand('topup', '💸 Top up'),
            BotCommand('talent')
        ], BotCommandScopeAllPrivateChats())

        print('BOT TELAH AKTIF')
        return True, self

    async def stop(self):
        await super().stop()
        print('BOT BERHASIL DIHENTIKAN')

    async def kirim_pesan(self, x: str):
        db = Database(config.id_admin, bot_id=self.id_bot).get_pelanggan()
        pesan = f'<b>TOTAL USER ( {db.total_pelanggan} ) PENGGUNA 📊</b>\n'
        pesan += f'➜ <i>Total user yang mengirim menfess hari ini adalah {x}/{db.total_pelanggan} user</i>\n'
        pesan += f'➜ <i>Berhasil direset menjadi 0 menfess</i>'
        url = f'https://api.telegram.org/bot{self.bot_token}'
        a = requests.get(f'{url}/sendMessage?chat_id={self.channel_log}&text={pesan}&parse_mode=HTML').json()
        requests.post(
            f'{url}/pinChatMessage?chat_id={self.channel_log}&message_id={a["result"]["message_id"]}&parse_mode=HTML')
        requests.post(
            f'{url}/deleteMessage?chat_id={self.channel_log}&message_id={a["result"]["message_id"] + 1}&parse_mode=HTML')
