from main.database.clone_db import Owner
from main.guchi import Guchi
from main.helpers import Database, Helper, isUser, isAdmin
from main.helpers.decorators import Bot
import traceback
from pyrogram import Client, enums, types, filters
from pyrogram import Client, Message

from main import bots, dbclone, Clone


@Bot("setchannelpost")
async def on_setchannelpost_handler(client: Guchi, message: Message, db: Database = None):
    if client.owner_id != 0:
        owner = Clone(client.owner_id)
        clone = await owner.get_clone()
        if clone is None:
            return await message.reply("❌ <b>ERROR</b>\n\n<b>Anda Belum Melakukan Clone</b>", quote=True)
    text = message.text
    if len(text.split()) < 2:
        return await message.reply("❌ <b>ERROR</b>\n\n<b>Gunakan Perintah</b> <code>/channel 1000</code>", quote=True)
    try:
        channel1 = int(text.split()[1])
        if client.owner_id != 0:
            await owner.update_channel1(channel1)
        else:
            clone.channel_2 = channel1
        return await message.reply(f"Channel post : {channel1}", quote=True)
    except ValueError:
        return await message.reply("❌ <b>Format coin harus angka</b>\n\n<b>Contoh</b> <code>/setchannelpost -10001293184518</code>", quote=True)
    except BaseException as e:
        e = traceback.format_exc()
        print(e)
        return await message.edit("❌ <b>ERROR</b>\n\n<b>Terjadi Kesalahan</b>")

@Bot("setchannelorgrub")
async def on_setchannelorgrub_handler(client: Guchi, message: Message, db: Database = None):
    if client.owner_id != 0:
        owner = Clone(client.owner_id)
        clone = await owner.get_clone()
        if clone is None:
            return await message.reply("❌ <b>ERROR</b>\n\n<b>Anda Belum Melakukan Clone</b>", quote=True)
    text = message.text
    if len(text.split()) < 2:
        return await message.reply("❌ <b>ERROR</b>\n\n<b>Gunakan Perintah</b> <code>/channel 1000</code>", quote=True)
    try:
        channel2 = int(text.split()[1])
        if client.owner_id != 0:
            await owner.update_channel2(channel2)
        else:
            clone.channel_2 = channel2
        return await message.reply(f"Channel/grub : {channel2}", quote=True)
    except ValueError:
        return await message.reply("❌ <b>Format coin harus angka</b>\n\n<b>Contoh</b> <code>/setchannelorgroup -10031982739475</code>", quote=True)
    except BaseException as e:
        e = traceback.format_exc()
        print(e)
        return await message.edit("❌ <b>ERROR</b>\n\n<b>Terjadi Kesalahan</b>")    
    
@Bot("setchannellog")
async def on_setchannellog_handler(client: Guchi, message: Message, db: Database = None):
    if client.owner_id != 0:
        owner = Clone(client.owner_id)
        clone = await owner.get_clone()
        if clone is None:
            return await message.reply("❌ <b>ERROR</b>\n\n<b>Anda Belum Melakukan Clone</b>", quote=True)
    text = message.text
    if len(text.split()) < 2:
        return await message.reply("❌ <b>ERROR</b>\n\n<b>Gunakan Perintah</b> <code>/channel 1000</code>", quote=True)
    try:
        channellog = int(text.split()[1])
        if client.owner_id != 0:
            await owner.update_channel_log(channellog)
        else:
            clone.channel_log = channellog
        return await message.reply(f"Channel log : {channellog}", quote=True)
    except ValueError:
        return await message.reply("❌ <b>Format coin harus angka</b>\n\n<b>Contoh</b> <code>/setchannellog -1009823147583</code>", quote=True)
    except BaseException as e:
        e = traceback.format_exc()
        print(e)
        return await message.edit("❌ <b>ERROR</b>\n\n<b>Terjadi Kesalahan</b>")

@Bot("setdailysend")
async def on_setdailysend_handler(client: Guchi, message: Message, db: Database = None):
    if client.owner_id != 0:
        owner = Clone(client.owner_id)
        clone = await owner.get_clone()
        if clone is None:
            return await message.reply("❌ <b>ERROR</b>\n\n<b>Anda Belum Melakukan Clone</b>", quote=True)
    text = message.text
    if len(text.split()) < 2:
        return await message.reply("❌ <b>ERROR</b>\n\n<b>Gunakan Perintah</b> <code>/channel 1000</code>", quote=True)
    try:
        dailysend = int(text.split()[1])
        if client.owner_id != 0:
            await owner.update_batas_kirim(dailysend)
        else:
            clone.batas_kirim = dailysend
        return await message.reply(f"Daily send : {dailysend}", quote=True)
    except ValueError:
        return await message.reply("❌ <b>Format coin harus angka</b>\n\n<b>Contoh</b> <code>/setdailysend 5</code>", quote=True)
    except BaseException as e:
        e = traceback.format_exc()
        print(e)
        return await message.edit("❌ <b>ERROR</b>\n\n<b>Terjadi Kesalahan</b>")

@Bot("setbiayasendmenfes")
async def on_setbiayasendmenfes_handler(client: Guchi, message: Message, db: Database = None):
    if client.owner_id != 0:
        owner = Clone(client.owner_id)
        clone = await owner.get_clone()
        if clone is None:
            return await message.reply("❌ <b>ERROR</b>\n\n<b>Anda Belum Melakukan Clone</b>", quote=True)
    text = message.text
    if len(text.split()) < 2:
        return await message.reply("❌ <b>ERROR</b>\n\n<b>Gunakan Perintah</b> <code>/setbiayasendmenfes 1000</code>", quote=True)
    try:
        biayasendmenfes = int(text.split()[1])
        if client.owner_id != 0:
            await owner.update_biaya_kirim(biayasendmenfes)
        else:
            clone.biaya_kirim = biayasendmenfes
        return await message.reply(f"Biaya send menfes : {biayasendmenfes}", quote=True)
    except ValueError:
        return await message.reply("❌ <b>Format coin harus angka</b>\n\n<b>Contoh</b> <code>/setbiayasendmenfes 1000</code>", quote=True)
    except BaseException as e:
        e = traceback.format_exc()
        print(e)
        return await message.edit("❌ <b>ERROR</b>\n\n<b>Terjadi Kesalahan</b>")
    
@Bot("setbiayahapusmenfes")
async def on_setbiayahapusmenfes_handler(client: Guchi, message: Message, db: Database = None):
    if client.owner_id != 0:
        owner = Clone(client.owner_id)
        clone = await owner.get_clone()
        if clone is None:
            return await message.reply("❌ <b>ERROR</b>\n\n<b>Anda Belum Melakukan Clone</b>", quote=True)
    text = message.text
    if len(text.split()) < 2:
        return await message.reply("❌ <b>ERROR</b>\n\n<b>Gunakan Perintah</b> <code>/setbiayahapusmenfes 1000</code>", quote=True)
    try:
        biayahapusmenfes = int(text.split()[1])
        if client.owner_id != 0:
            await owner.update_biaya_delete(biayahapusmenfes)
        else:
            clone.biaya_delete = biayahapusmenfes
        return await message.reply(f"Biaya hapus menfes : {biayahapusmenfes}", quote=True)
    except ValueError:
        return await message.reply("❌ <b>Format coin harus angka</b>\n\n<b>Contoh</b> <code>/setbiayadeletemenfes 1000</code> atau <code>/setbiayadeletemenfes 0</code> untuk tidak dipungut biaya", quote=True)
    except BaseException as e:
        e = traceback.format_exc()
        print(e)
        return await message.edit("❌ <b>ERROR</b>\n\n<b>Terjadi Kesalahan</b>")
    
@Bot("setbiayapinnedmenfes")
async def on_setbiayapinnedmenfes_handler(client: Guchi, message: Message, db: Database = None):
    if client.owner_id != 0:
        owner = Clone(client.owner_id)
        clone = await owner.get_clone()
        if clone is None:
            return await message.reply("❌ <b>ERROR</b>\n\n<b>Anda Belum Melakukan Clone</b>", quote=True)
    text = message.text
    if len(text.split()) < 2:
        return await message.reply("❌ <b>ERROR</b>\n\n<b>Gunakan Perintah</b> <code>/setbiayapinnedmenfes 1000</code>", quote=True)
    try:
        biayapinnedmenfes = int(text.split()[1])
        if client.owner_id != 0:
            await owner.update_biaya_pinned(biayapinnedmenfes)
        else:
            clone.biaya_pinned = biayapinnedmenfes
        return await message.reply(f"Biaya hapus menfes : {biayapinnedmenfes}", quote=True)
    except ValueError:
        return await message.reply("❌ <b>Format coin harus angka</b>\n\n<b>Contoh</b> <code>/setbiayapinnedmenfes 1000</code> atau <code>/setbiayapinnedmenfes 0</code> untuk tidak dipungut biaya", quote=True)
    except BaseException as e:
        e = traceback.format_exc()
        print(e)
        return await message.edit("❌ <b>ERROR</b>\n\n<b>Terjadi Kesalahan</b>")
    
