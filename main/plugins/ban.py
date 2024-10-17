from main.helpers import Database, Helper
from main.helpers.decorators import Bot
import config
import re
from pyrogram import Client, enums, types


@Bot(r"^[\/]ban(\s|\n)*(\d+)", regex=True, is_admin=True)
async def on_ban_handler(client: Client, msg: types.Message, db: Database = None):
    # if re.search(r"^[\/]ban(\s|\n)*$", msg.text):
    #     return await msg.reply_text(
    #         text="<b>Cara penggunaan ban user</b>\n\n<code>/ban id_user alasan ban</code>\n<code>/ban id_user</code>\n\nContoh :\n<code>/ban 121212021</code>\n<code>/ban 12121 share porn</code>", quote=True,
    #         parse_mode=enums.ParseMode.HTML
    #     )
    member = db.get_data_pelanggan()
    if member.status != 'admin' and member.status != 'owner':
        return
    target = msg.matches[0].group(2)
    db = Database(int(target), client.me.id)
    if await db.cek_user_didatabase():
        status = [
            'admin', 'owner', 'talent', 'daddy sugar', 'proplayer',
            'teman curhat', 'girlfriend rent', 'boyfriend rent'
        ]
        member = db.get_data_pelanggan()
        if member.status == 'admin' in status:
            return await msg.reply_text(
                text=f"❌<i>Terjadi kesalahan, <a href='tg://user?id={str(target)}'>user</a> adalah seorang {member.status.upper()} tidak dapat dibanned</i>", quote=True,
                parse_mode=enums.ParseMode.HTML
            )
        update = ''
        if member.status == 'banned':
            update = 'Alasan berhasil diupdate'

        text_split = msg.text.split(None, 2)
        alasan = "-" if not len(text_split) > 2 else text_split[2]
        await db.banned_user(int(target), client.me.id, alasan)
        return await msg.reply_text(
            text=f"<a href='tg://openmessage?user_id={str(target)}'>User</a> <i>berhasil dibanned</i>\n└Dibanned oleh : <a href='tg://openmessage?user_id={str(config.id_admin)}'>Admin</a>\n\nAlasan: {str(alasan)}\n\n{update}", quote=True,
            parse_mode=enums.ParseMode.HTML
        )
    else:
        return await msg.reply_text(
            text=f"<i><a href='tg://user?id={str(target)}'>user</a> tidak terdaftar didatabase</i>", quote=True,
            parse_mode=enums.ParseMode.HTML
        )


@Bot(r"^[\/]unban(\s|\n)*(\d+)", regex=True)
async def on_unban_handler(client: Client, msg: types.Message, db: Database = None):
    # if re.search(r"^[\/]unban(\s|\n)*$", msg.text):
    #     return await msg.reply_text(
    #         text="<b>Cara penggunaan unban user</b>\n\n<code>/unban id_user</code>\n\nContoh :\n<code>/unban 121212021</code>", quote=True,
    #         parse_mode=enums.ParseMode.HTML
    #     )
    member = db.get_data_pelanggan()
    if member.status != 'admin' and member.status != 'owner':
        return
    target = msg.matches[0].group(2)
    db = Database(int(target), client.me.id)
    if await db.cek_user_didatabase():
        if target in db.get_data_bot(client.me.id).ban:
            await db.unban_user(int(target), client.me.id)
            return await msg.reply_text(
                text=f"<a href='tg://openmessage?user_id={str(target)}'>User</a> <i>berhasil diunbanned</i>\n└Diunbanned oleh : <a href='tg://openmessage?user_id={str(config.id_admin)}'>Admin</a>", quote=True,
                parse_mode=enums.ParseMode.HTML
            )
        else:
            return await msg.reply_text(
                text=f"<i><a href='tg://user?id={str(target)}'>user</a> sedang tidak dalam kondisi banned</i>", quote=True,
                parse_mode=enums.ParseMode.HTML
            )
    else:
        return await msg.reply_text(
            text=f"<i><a href='tg://user?id={str(target)}'>user</a> tidak terdaftar didatabase</i>", quote=True,
            parse_mode=enums.ParseMode.HTML
        )


@Bot("listban")
async def on_unban_handler(client: Client, msg: types.Message, db: Database = None):
    helper = Helper(client, msg)
    db = Database(helper.user_id, client.me.id).get_data_bot(client.me.id)
    if len(db.ban) == 0:
        return await helper.message.reply_text('<i>Tidak ada user dibanned saat ini</i>', True, enums.ParseMode.HTML)
    else:
        pesan = "<b>Daftar banned</b>\n"
        ind = 1
        for i in db.ban:
            pesan += "• ID: " + str(i) + " | <a href='tg://openmessage?user_id=" + str(i) + "'>( " + str(ind) + " )</a>\n"
            ind += 1
    await helper.message.reply_text(pesan, True, enums.ParseMode.HTML)