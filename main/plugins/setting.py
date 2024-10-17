import re

from pyrogram import Client, enums, types
from pyrogram.types import (
    Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
)
from main.helpers import Database
from main.helpers.decorators import Bot


@Bot(r"^[\/]bot", regex=True, is_admin=True)
async def bot_handler(client: Client, msg: Message, db: Database = None):
    if re.search(r"^[\/]bot(\s|\n)*$", msg.text):
        return await msg.reply("*Cara penggunaan command*\n\nEX : `/bot <on|off>`\nContoh : `/bot on`", quote=True, parse_mode=enums.ParseMode.MARKDOWN)

    x = re.search(r"^[\/]bot\s*(on|off|<on>|<off>)$", msg.text)
    if x:
        status = x.group(1)
        my_db = db if db else Database(msg.from_user.id, client.me.id)
        db_bot = my_db.get_data_bot(client.me.id)
        if status == 'on' or status == '<on>':
            if db_bot.bot_status:
                return await msg.reply(
                    text='❌<i>Terjadi kesalahan, bot saat ini dalam kondisi aktif</i>', quote=True,
                    parse_mode=enums.ParseMode.HTML
                )
            else:
                await my_db.bot_handler(status)
                return await msg.reply(
                    text='Saat ini status bot telah <b>AKTIF</b> ✅', quote=True,
                    parse_mode=enums.ParseMode.HTML
                )
        else:
            if not db_bot.bot_status:
                return await msg.reply(
                    text='❌<i>Terjadi kesalahan, bot saat ini dalam kondisi tidak aktif</i>', quote=True,
                    parse_mode=enums.ParseMode.HTML
                )
            else:
                await my_db.bot_handler(status)
                return await msg.reply(
                    text='Saat ini status bot telah <b>TIDAK AKTIF</b> ❌', quote=True,
                    parse_mode=enums.ParseMode.HTML
                )
    else:
        return await msg.reply("*Cara penggunaan command*\n\nEX : `/bot <on|off>`\nContoh : `/bot on`", quote=True, parse_mode=enums.ParseMode.MARKDOWN)


@Bot(["setting", "settings"])
async def setting_handler(client: Client, msg:types.Message, db: Database = None):
    member = db.get_data_pelanggan()
    if member.status != 'admin' and member.status != 'owner':
        return
    db = db.get_data_bot(client.me.id)
    pesan = "<b>💌 Menfess User\n\n✅ = AKTIF\n❌ = TIDAK AKTIF</b>\n"
    pesan += "______________________________\n\n"
    photo = ["TIDAK AKTIF", "❌"] if not db.kirimchannel.photo else ["AKTIF", "✅"]
    video = ["TIDAK AKTIF", "❌"] if not db.kirimchannel.video else ["AKTIF", "✅"]
    voice = ["TIDAK AKTIF", "❌"] if not db.kirimchannel.voice else ["AKTIF", "✅"]
    status_bot = "TIDAK AKTIF" if not db.bot_status else "AKTIF"
    pesan += f"📸 Foto = <b>{photo[0]}</b>\n"
    pesan += f"🎥 Video = <b>{video[0]}</b>\n"
    pesan += f"🎤 Voice = <b>{voice[0]}</b>\n\n"
    pesan += f'🔰Status bot: <b> {status_bot}</b>'
    markup = InlineKeyboardMarkup([
        [InlineKeyboardButton('📸', callback_data='no'), InlineKeyboardButton(photo[1], callback_data='photo')],
        [InlineKeyboardButton('🎥', callback_data='no'), InlineKeyboardButton(video[1], callback_data='video')],
        [InlineKeyboardButton('🎤', callback_data='no'), InlineKeyboardButton(voice[1], callback_data='voice')],
        [InlineKeyboardButton(status_bot, callback_data='status_bot')]
    ])
    await msg.reply(
        pesan, quote=True, parse_mode=enums.ParseMode.HTML, reply_markup=markup
                    )