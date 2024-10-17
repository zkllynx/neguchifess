import asyncio

from pyrogram import Client, enums, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
import re
import config
from main.guchi import Guchi
from main.helpers import Database, Helper
from main.helpers.decorators import Bot
from main.helpers.referral import ReferralDB, add_by_referral, new_referral, invite_handler
from main.helpers import Database


@Bot("start")
async def on_start_handler(client: Client, msg: Message, db: Database = None):
    is_new = False
    helper = Helper(client, msg)
    if db and not await db.cek_user_didatabase():  # cek apakah user sudah ditambahkan didatabase
        is_new = True
        await helper.daftar_pelanggan()  # jika belum akan ditambahkan data user ke database
        await helper.send_to_channel_log(type="log_daftar")
    command = msg.text or msg.caption
    _cmd = command.split()
    if is_new and len(_cmd) > 1:
        invite_code = _cmd[1]
        await add_by_referral(client, msg, invite_code)
    await new_referral(client, msg)
    first = msg.from_user.first_name
    last = msg.from_user.last_name
    fullname = first if not last else first + ' ' + last
    username = '@OxDonquixote' if not msg.from_user.username else '@' + msg.from_user.username
    mention = msg.from_user.mention
    markup = InlineKeyboardMarkup([
        [InlineKeyboardButton('Rules', url='#')]
    ])
    await msg.reply_text(
        text=config.start_msg.format(
            id=msg.from_user.id,
            mention=mention,
            username=username,
            first_name=await helper.escapeHTML(first),
            last_name=await helper.escapeHTML(last),
            fullname=await helper.escapeHTML(fullname),
        ),
        reply_markup=markup,
        disable_web_page_preview=True,
        quote=True
    )


@Bot("status")
async def status_handler(client: Client, msg: Message, db: Database = None):
    helper = Helper(client, msg)
    db = db.get_data_pelanggan()
    ref_db = ReferralDB(msg.from_user.id)
    ref_code = await ref_db.referral()
    link_reff = f"`https://t.me/{client.me.username}?start={ref_code}`"
    pesan = '<b>ID CARD ONS</b>\n\n'
    pesan += f'🆔 <b>ID</b>                  : <code>{db.id}</code>\n\n'
    pesan += f'👮 <b>User</b>              : {db.mention}\n\n'
    pesan += f'👑 <b>Status</b>          : {db.status}\n\n'
    pesan += f'🕵️ Referral Link        : {link_reff}\n\n'
    pesan += f'💸 <b>Coin</b>              : {helper.formatrupiah(db.coin)} BZ\n\n'
    pesan += f'📆 <b>Daily Send</b>  : {db.menfess}/{config.batas_kirim}\n\n'

    poson = 'ID CARD ONS\n\n'
    poson += f'🆔 ID                  : {db.id}\n\n'
    poson += f'👮 User              : {db.mention}\n\n'
    poson += f'👑 Status          : {db.status}\n\n'
    poson += f'🕵️ Referral Link        : {link_reff}\n\n'
    poson += f'💸 Coin              : {helper.formatrupiah(db.coin)} BZ\n\n'
    poson += f'📆 Daily Send  : {db.menfess}/{config.batas_kirim}\n\n'

    caption = msg.text or msg.caption
    entities = msg.entities or msg.caption_entities

    if db.status == 'talent':
        picture = config.pic_talent

    markup = InlineKeyboardMarkup([
        [InlineKeyboardButton('Rules', url='#'), InlineKeyboardButton('help', callback_data='help'), InlineKeyboardButton('top up', callback_data='topup')]
    ])
    if db.status == 'talent':
        await client.send_photo(db.id, picture, poson, caption_entities=entities, reply_markup=markup)

    if db.status == 'member' or db.status == 'admin' or db.status == 'owner':
        await client.send_message(db.id, poson, reply_markup=markup)

    if db.status == 'non member':
        await client.send_message(db.id, pesan, reply_markup=markup)


@Bot("ubahstatus")
async def rubahstatus_handler(client: Client, msg: Message, db: Database = None):
    pesan = 'Chat @OxDonquixote jika anda ingin merubah status anda. Check status yang tersedia di <useramebotmf>'
    await msg.reply(pesan, True, enums.ParseMode.HTML)

@Bot("stats", is_admin=True)
async def statistik_handler(client: Client, msg: Message, db: Database = None):
    bot = db.get_data_bot(client.me.id)
    db_user = db.get_data_pelanggan()
    pesan = "<b>📊 STATISTIK BOT\n\n"
    pesan += f"▪️Pelanggan: {db.get_pelanggan().total_pelanggan}\n"
    pesan += f"▪️Admin: {len(bot.admin)}\n"
    pesan += f"▪️Talent: {len(bot.talent)}\n"
    pesan += f"▪️Banned: {len(bot.ban)}\n\n"
    pesan += f"🔰Status bot: {'AKTIF' if bot.bot_status else 'TIDAK AKTIF'}</b>"
    await msg.reply_text(pesan, True, enums.ParseMode.HTML)


@Bot("/reff")
async def on_reff_handler(client: Client, msg: Message, database: Database = None):
    return await invite_handler(client, msg)