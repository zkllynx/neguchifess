from typing import Union

import config
from main.guchi import Guchi
from pyrogram import filters, Client
from pyrogram.types import Message
from pyrogram import enums

from main.helpers import Helper, Database


def Bot(command: Union[str, list], regex: bool = False, prefixes: Union[list, str] = "/", flt=filters.private,
        is_authorized: bool = True, is_admin: bool = False):
    def wrapper(func, custom_filter=flt):
        cmd = filters.command(command, prefixes) if not regex else filters.regex(command)

        @Guchi.on_message(cmd & custom_filter)
        async def wrapped_func(client: Client, msg: Message):
            database = None
            if is_authorized:
                uid = msg.from_user.id
                helper = Helper(client, msg)
                database = Database(uid, client.me.id)
                is_new = False
                # cek apakah user sudah bergabung digrup chat
                if not await helper.cek_langganan_channel(uid):
                    await helper.pesan_langganan()  # jika belum akan menampilkan pesan bergabung
                    return msg.stop_propagation()

                # Pesan jika bot sedang dalam kondisi tidak aktif
                if not database.get_data_bot(client.me.id).bot_status:
                    status = [
                        'non member', 'member', 'banned'
                    ]
                    member = database.get_data_pelanggan()
                    if member.status in status:
                        await client.send_message(uid, "<i>Saat ini bot sedang dinonaktifkan</i>", enums.ParseMode.HTML)
                        return msg.stop_propagation()
            if is_admin:
                uid = msg.from_user.id
                if uid != config.id_admin:
                    return msg.stop_propagation()
            await func(client, msg, database)

        return wrapped_func

    return wrapper
