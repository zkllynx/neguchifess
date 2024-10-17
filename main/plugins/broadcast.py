from pyrogram import Client, filters

from main.guchi import Guchi
from main.helpers import Database
from main.helpers.decorators import Bot
import asyncio
from pyrogram.types import (
    Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
)
from pyrogram.errors import (
    FloodWait, PeerIdInvalid, UserIsBlocked, InputUserDeactivated
)


@Bot("broadcast", is_admin=True)
async def on_broadcast_handler(client: Client, msg: Message, db: Database = None):
    if msg.reply_to_message != None:
        anu = msg.reply_to_message
        anu = await anu.copy(msg.chat.id, reply_to_message_id=anu.id)
        markup = InlineKeyboardMarkup([
            [InlineKeyboardButton('Ya', 'ya_confirm'), InlineKeyboardButton('Tidak', 'tidak_confirm')]
        ])
        await anu.reply('apakah kamu akan mengirimkan pesan broadcast ?', True, reply_markup=markup)
    else:
        await msg.reply('Harap reply sebuah pesan', True)


@Guchi.on_callback_query(filters.regex('^ya_confirm$'))
async def on_broadcast_ya(client: Client, query: CallbackQuery):
    msg = query.message
    db = Database(msg.from_user.id, client.me.id)
    if not msg.reply_to_message:
        await query.answer('Pesan tidak ditemukan', True)
        await query.message.delete()
        return
    message = msg.reply_to_message
    user_ids = db.get_pelanggan().id_pelanggan

    berhasil = 0
    dihapus = 0
    blokir = 0
    gagal = 0
    await msg.edit('Broadcast sedang berlangsung, tunggu sebentar', reply_markup = None)
    for user_id in user_ids:
        try:
            await message.copy(user_id)
            berhasil += 1
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await message.copy(user_id)
            berhasil += 1
        except UserIsBlocked:
            blokir += 1
            await db.hapus_pelanggan(user_id)
        except PeerIdInvalid:
            gagal += 1
        except InputUserDeactivated:
            dihapus += 1

    text = f"""<b>Broadcast selesai</b>
    
Jumlah pengguna: {str(len(user_ids))}
Berhasil terkirim: {str(berhasil)}
Pengguna diblokir: {str(blokir)}
Akun yang dihapus: {str(dihapus)} (<i>Telah dihapus dari database</i>)
Gagal terkirim: {str(gagal)}"""

    await msg.reply(text)
    await msg.delete()
    await message.delete()


@Guchi.on_callback_query(filters.regex('^tidak_confirm$'))
async def on_close_cbb(client: Client, query: CallbackQuery):
    try:
        await query.message.reply_to_message.delete()
    except:
        pass
    try:
        await query.message.delete()
    except:
        pass