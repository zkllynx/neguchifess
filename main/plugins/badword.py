import os
from pyrogram import Client, types
from main.helpers import Database
from main.helpers.decorators import Bot
from config import kata_terlarang


async def badwords_handler(c: Client, m: types.Message):
    global kata_terlarang
    cmd = m.text.split()
    if len(cmd) < 2:
        return await m.reply_text(f"Sertakan badwords nya")
    words = " ".join(cmd[1:])
    if not "|" in words:
        return await m.reply_text(f"Format Badwords salah, setiap kata dipisah dengan |")
    if len(words.split("|")) < 1:
        return await m.reply_text(f"Minimal Badwords 2")
    words = "|".join(words.split("|"))
    os.environ['KATA_TERLARANG'] = words
    kata_terlarang = words
    await m.reply_text(f"Badwords berhasil diubah ke {kata_terlarang}")


@Bot("setbadwords", is_admin=True)
async def on_set_badwords_handler(client: Client, msg: types.Message, db: Database = None):
    return await badwords_handler(client, msg)


@Bot("badwords", is_admin=True)
async def on_set_badwords_handler(client: Client, msg: types.Message, db: Database = None):
    badlist = kata_terlarang.split("|")
    allbad = "\n".join(badlist)
    return await msg.reply_text(f"Total badwords: {len(badlist)}\n{allbad}")
