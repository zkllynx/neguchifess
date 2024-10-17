from pyrogram import Client, enums
from pyrogram.types import Message
import re
import config
from main.helpers import Database, Helper
from main.helpers.decorators import Bot


@Bot(r"^[\/]admin", regex=True, is_admin=True)
async def tambah_admin_handler(client: Client, msg: Message, db: Database = None):
    if re.search(r"^[\/]admin(\s|\n)*$", msg.text):
        return await msg.reply_text(
            text="<b>Cara penggunaan tambah admin</b>\n\n<code>/admin id_user</code>\n\nContoh :\n<code>/admin 121212021</code>",
            quote=True,
            parse_mode=enums.ParseMode.HTML
        )
    y = re.search(r"^[\/]admin(\s|\n)*(\d+)$", msg.text)
    if y:
        target = y.group(2)
        db = Database(int(target), client.me.id)
        if target in db.get_data_bot(client.me.id).ban:
            return await msg.reply_text(
                text=f"<i><a href='tg://user?id={str(target)}'>User</a> sedang dalam kondisi banned</i>\n└Tidak dapat menjadikan user admin",
                quote=True,
                parse_mode=enums.ParseMode.HTML
            )
        if await db.cek_user_didatabase():
            status = [
                'admin', 'owner', 'talent'
            ]
            member = db.get_data_pelanggan()
            if member.status in status:
                return await msg.reply_text(
                    text=f"❌<i>Terjadi kesalahan, <a href='tg://user?id={str(target)}'>user</a> adalah seorang {member.status.upper()}</i>",
                    quote=True,
                    parse_mode=enums.ParseMode.HTML
                )
            try:
                await client.send_message(
                    int(target),
                    text=f"<i>Kamu telah menjadi admin bot</i>\n└Diangkat oleh : <a href='tg://openmessage?user_id={str(config.id_admin)}'>Admin</a>",
                    parse_mode=enums.ParseMode.HTML
                )
                await db.update_admin(int(target), client.me.id)
                return await msg.reply_text(
                    text=f"<a href='tg://openmessage?user_id={str(target)}'>User</a> <i>berhasil menjadi admin bot</i>\n└Diangkat oleh : <a href='tg://openmessage?user_id={str(config.id_admin)}'>Admin</a>",
                    quote=True,
                    parse_mode=enums.ParseMode.HTML
                )
            except Exception as e:
                return await msg.reply_text(
                    text=f"❌<i>Terjadi kesalahan, sepertinya user memblokir bot</i>\n\n{e}", quote=True,
                    parse_mode=enums.ParseMode.HTML
                )
        else:
            return await msg.reply_text(
                text=f"<i><a href='tg://user?id={str(target)}'>user</a> tidak terdaftar didatabase</i>", quote=True,
                parse_mode=enums.ParseMode.HTML
            )
    else:
        return await msg.reply_text(
            text="<b>Cara penggunaan tambah admin</b>\n\n<code>/admin id_user</code>\n\nContoh :\n<code>/admin 121212021</code>",
            quote=True,
            parse_mode=enums.ParseMode.HTML
        )


@Bot(r"^[\/]unadmin", regex=True, is_admin=True)
async def hapus_admin_handler(client: Client, msg: Message, db: Database = None):
    if re.search(r"^[\/]unadmin(\s|\n)*$", msg.text):
        return await msg.reply_text(
            text="<b>Cara penggunaan mencabut status admin</b>\n\n<code>/unadmin id_user</code>\n\nContoh :\n<code>/unadmin 121212021</code>",
            quote=True,
            parse_mode=enums.ParseMode.HTML
        )
    y = re.search(r"^[\/]unadmin(\s|\n)*(\d+)$", msg.text)
    if y:
        target = y.group(2)
        db = Database(int(target), client.me.id)
        if await db.cek_user_didatabase():
            status = [
                'owner', 'talent'
            ]
            member = db.get_data_pelanggan()
            if member.status in status:
                return await msg.reply_text(
                    text=f"❌<i>Terjadi kesalahan, <a href='tg://user?id={str(target)}'>user</a> adalah seorang {member.status.upper()}</i>",
                    quote=True,
                    parse_mode=enums.ParseMode.HTML
                )
            if member.status == 'admin':
                try:
                    await client.send_message(
                        int(target),
                        text=f"<i>Sayangnya owner telah mencabut jabatanmu sebagai admin</i>\n└Diturunkan oleh : <a href='tg://openmessage?user_id={str(config.id_admin)}'>Admin</a>",
                        parse_mode=enums.ParseMode.HTML
                    )
                    await db.hapus_admin(int(target), client.me.id)
                    return await msg.reply_text(
                        text=f"<a href='tg://openmessage?user_id={str(target)}'>User</a> <i>berhasil diturunkan menjadi member</i>\n└Diturunkan oleh : <a href='tg://openmessage?user_id={str(config.id_admin)}'>Admin</a>",
                        quote=True,
                        parse_mode=enums.ParseMode.HTML
                    )
                except Exception as e:
                    return await msg.reply_text(
                        text=f"❌<i>Terjadi kesalahan, sepertinya user memblokir bot</i>\n\n{e}", quote=True,
                        parse_mode=enums.ParseMode.HTML
                    )
            else:
                return await msg.reply_text(
                    text=f"<i><a href='tg://openmessage?user_id={str(target)}'>User</a> bukan seorang admin</i>",
                    quote=True,
                    parse_mode=enums.ParseMode.HTML
                )
        else:
            return await msg.reply_text(
                text=f"<i><a href='tg://user?id={str(target)}'>user</a> tidak terdaftar didatabase</i>", quote=True,
                parse_mode=enums.ParseMode.HTML
            )
    else:
        await msg.reply_text(
            text="<b>Cara penggunaan mencabut status admin</b>\n\n<code>/unadmin id_user</code>\n\nContoh :\n<code>/unadmin 121212021</code>",
            quote=True,
            parse_mode=enums.ParseMode.HTML
        )


@Bot(r"^[\/]member", regex=True, is_admin=True)
async def tambah_member_handler(client: Client, msg: Message, db: Database = None):
    if re.search(r"^[\/]member(\s|\n)*$", msg.text):
        return await msg.reply_text(
            text="<b>Cara penggunaan tambah member</b>\n\n<code>/member id_user</code>\n\nContoh :\n<code>/member 121212021</code>",
            quote=True,
            parse_mode=enums.ParseMode.HTML
        )
    y = re.search(r"^[\/]member(\s|\n)*(\d+)$", msg.text)
    if y:
        target = y.group(2)
        db = Database(int(target), client.me.id)
        if target in db.get_data_bot(client.me.id).ban:
            return await msg.reply_text(
                text=f"<i><a href='tg://user?id={str(target)}'>User</a> sedang dalam kondisi banned</i>\n└Tidak dapat menjadikan user member",
                quote=True,
                parse_mode=enums.ParseMode.HTML
            )
        if await db.cek_user_didatabase():
            status = [
                'admin', 'owner'
            ]
            member = db.get_data_pelanggan()
            if member.status in status:
                return await msg.reply_text(
                    text=f"❌<i>Terjadi kesalahan, <a href='tg://user?id={str(target)}'>user</a> adalah seorang {member.status.upper()}</i>",
                    quote=True,
                    parse_mode=enums.ParseMode.HTML
                )
            try:
                await client.send_message(
                    int(target),
                    text=f"<i>Kamu telah menjadi member bot</i>\n└Diangkat oleh : <a href='tg://openmessage?user_id={str(config.id_admin)}'>Admin</a>",
                    parse_mode=enums.ParseMode.HTML
                )
                await db.update_member(int(target), client.me.id)
                return await msg.reply_text(
                    text=f"<a href='tg://openmessage?user_id={str(target)}'>User</a> <i>berhasil menjadi member bot</i>\n└Diangkat oleh : <a href='tg://openmessage?user_id={str(config.id_admin)}'>Admin</a>",
                    quote=True,
                    parse_mode=enums.ParseMode.HTML
                )
            except Exception as e:
                return await msg.reply_text(
                    text=f"❌<i>Terjadi kesalahan, sepertinya user memblokir bot</i>\n\n{e}", quote=True,
                    parse_mode=enums.ParseMode.HTML
                )
        else:
            return await msg.reply_text(
                text=f"<i><a href='tg://user?id={str(target)}'>user</a> tidak terdaftar didatabase</i>", quote=True,
                parse_mode=enums.ParseMode.HTML
            )
    else:
        return await msg.reply_text(
            text="<b>Cara penggunaan tambah member</b>\n\n<code>/member id_user</code>\n\nContoh :\n<code>/member 121212021</code>",
            quote=True,
            parse_mode=enums.ParseMode.HTML
        )


@Bot(r"^[\/]unmember", regex=True, is_admin=True)
async def hapus_member_handler(client: Client, msg: Message, db: Database = None):
    if re.search(r"^[\/]unmember(\s|\n)*$", msg.text):
        return await msg.reply_text(
            text="<b>Cara penggunaan mencabut status member</b>\n\n<code>/unmember id_user</code>\n\nContoh :\n<code>/unmember 121212021</code>",
            quote=True,
            parse_mode=enums.ParseMode.HTML
        )
    y = re.search(r"^[\/]unmember(\s|\n)*(\d+)$", msg.text)
    if y:
        target = y.group(2)
        db = Database(int(target), client.me.id)
        if await db.cek_user_didatabase():
            status = [
                'admin', 'owner'
            ]
            member = db.get_data_pelanggan()
            if member.status in status:
                return await msg.reply_text(
                    text=f"❌<i>Terjadi kesalahan, <a href='tg://user?id={str(target)}'>user</a> adalah seorang {member.status.upper()}</i>",
                    quote=True,
                    parse_mode=enums.ParseMode.HTML
                )
            if member.status == 'member':
                try:
                    await client.send_message(
                        int(target),
                        text=f"<i>Sayangnya owner telah mencabut statusmu sebagai member</i>\n└Diturunkan oleh : <a href='tg://openmessage?user_id={str(config.id_admin)}'>Admin</a>",
                        parse_mode=enums.ParseMode.HTML
                    )
                    await db.hapus_member(int(target), client.me.id)
                    return await msg.reply_text(
                        text=f"<a href='tg://openmessage?user_id={str(target)}'>User</a> <i>berhasil diturunkan menjadi member</i>\n└Diturunkan oleh : <a href='tg://openmessage?user_id={str(config.id_admin)}'>Admin</a>",
                        quote=True,
                        parse_mode=enums.ParseMode.HTML
                    )
                except Exception as e:
                    return await msg.reply_text(
                        text=f"❌<i>Terjadi kesalahan, sepertinya user memblokir bot</i>\n\n{e}", quote=True,
                        parse_mode=enums.ParseMode.HTML
                    )
            else:
                return await msg.reply_text(
                    text=f"<i><a href='tg://openmessage?user_id={str(target)}'>User</a> bukan seorang member</i>",
                    quote=True,
                    parse_mode=enums.ParseMode.HTML
                )
        else:
            return await msg.reply_text(
                text=f"<i><a href='tg://user?id={str(target)}'>user</a> tidak terdaftar didatabase</i>", quote=True,
                parse_mode=enums.ParseMode.HTML
            )
    else:
        await msg.reply_text(
            text="<b>Cara penggunaan mencabut status member</b>\n\n<code>/unmember id_user</code>\n\nContoh :\n<code>/unmember 121212021</code>",
            quote=True,
            parse_mode=enums.ParseMode.HTML
        )


@Bot("list_admin")
async def list_admin_handler(client: Client, msg: Message, db: Database = None):
    helper = Helper(client, msg)
    db = Database(helper.user_id, client.me.id).get_data_bot(client.me.id)
    pesan = "<b>Owner bot</b>\n"
    pesan += "• ID: " + str(config.id_admin) + " | <a href='tg://user?id=" + str(
        config.id_admin) + "'>Owner bot</a>\n\n"
    if len(db.admin) > 0:
        pesan += "<b>Daftar Admin bot</b>\n"
        ind = 1
        for i in db.admin:
            pesan += "• ID: " + str(i) + " | <a href='tg://user?id=" + str(i) + "'>Admin " + str(ind) + "</a>\n"
            ind += 1
    await helper.message.reply_text(pesan, True, enums.ParseMode.HTML)
