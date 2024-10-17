from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import config
import re
import random
from pyrogram import Client, enums, types
from main.helpers import Database
from config import daget, claimed
from main.database.referral import ReferralDB


async def new_referral(client: Client, msg: types.Message):
    ref_db = ReferralDB(msg.from_user.id)
    ref_code = await ref_db.referral()
    return ref_code


async def invite_handler(client: Client, msg: types.Message):
    first = msg.from_user.first_name
    last = msg.from_user.last_name
    ref_db = ReferralDB(msg.from_user.id)
    ref_code = await ref_db.referral()
    db_ref = await ref_db.get_referral()
    link_reff = f"https://t.me/{client.me.username}?start={ref_code}"
    invite_text = f"""Link Referral anda: {link_reff}

Invite 1 orang untuk mendapatkan 2 daily send
Invite 3 orang untuk mendapatkan 50 Coin BZ
Invite 5 orang untuk mendapatkan 2 daily send
Invite 10 orang untuk mendapatkan 400 Coin
Invite 11 reset menjadi 1 atau mendapatkan 2daily send

Total user yang berhasil anda invited: {db_ref.invited}"""

    markup = InlineKeyboardMarkup([
        [InlineKeyboardButton(
            "🔁 Share Link", url=f"https://telegram.me/share/url?url={link_reff}"
        )]
    ])
    await msg.reply_text(
        text=invite_text,
        reply_markup=markup,
        disable_web_page_preview=True,
        quote=True
    )


async def add_by_referral(client: Client, msg: types.Message, code: str):
    if not re.match(r"^INV\d+$", code):
        return False
    user_id = int(code[3:])
    ref_db = ReferralDB(user_id)
    ref_data = await ref_db.get_referral()
    if not ref_data:
        return False
    total_invited = ref_data.invited
    is_coin = False
    coin = 0
    daily_send = 0
    if total_invited == 0:
        # dapet daily send 2
        daily_send = 2
        pass
    elif total_invited == 2:
        # dapet koin +50
        is_coin = True
        coin = 50
        pass
    elif total_invited == 4:
        # dapet daily send
        daily_send = 2
        pass
    elif total_invited == 9:
        # dapet koin +400
        is_coin = True
        coin = 400
        pass
    elif total_invited >= 10:
        # reset total invited dan dapet daily send
        await ref_db.reset_referral()
        daily_send = 2
    else:
        # tidak dapat apa-apa
        await ref_db.add_referral(1)
        return False

    db = Database(user_id).get_data_pelanggan()
    added = await ref_db.add_referral(1)
    reward = f"""Daily Send +{daily_send}""" if not is_coin else f"""+{coin} Coin"""
    if not is_coin:
        if daily_send > 0:
            await Database(user_id).reset_menfess()
    else:
        new_coin = db.coin + coin if is_coin else db['coin']
        await Database(user_id).update_coin(new_coin)
    if added:
        await client.send_message(
            chat_id=user_id,
            text=f"🎉 Anda mendapatkan {reward} dari referal anda!"
        )
    return added