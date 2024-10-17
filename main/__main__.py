import asyncio
import traceback
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from main.guchi import Guchi, data
from main import dbclone, bots, set_main_bot
from main.helpers import Database
from main.database.referral import reset_referrals
import pytz
from pyrogram import idle

loop = asyncio.get_event_loop()


async def reset_menfess():
    db = Database(data[0])
    x = await db.reset_menfess()
    await Guchi().kirim_pesan(x=str(x))
    print('PESAN PROMOTE BERHASIL DIRESET')


async def reset_reff_invited():
    # check the current hours if 00:00 then reset the referral
    tz = pytz.timezone('Asia/Jakarta')
    now = datetime.now(tz)
    if now.hour == 0 and now.minute == 0:
        print("reset_reff_invited")
        reset_referrals()


async def main():
    global bots
    all_clone = await dbclone.full_clone()
    try:
        scheduler = AsyncIOScheduler(timezone="Asia/Jakarta")
        scheduler.add_job(reset_menfess, trigger="cron", hour=1, minute=0)
        scheduler.add_job(reset_reff_invited, trigger="interval", minutes=5)
        scheduler.start()
        _, jieh = await Guchi(0, memory=False).start()
        set_main_bot(jieh.me.id)
        bots.append(jieh)
        for clone in all_clone:
            try:
                if not clone.status:
                    continue
                sts, jiehbot = await Guchi(owner_id=clone.user_id, token=clone.token, memory=False, owner=clone).start()
                if not sts:
                    continue
                bots.append(jiehbot)
            except BaseException as e:
                print(e)
        await idle()
    except KeyboardInterrupt:
        await Guchi().stop()
    except Exception as e:
        print(traceback.format_exc())


if __name__ == '__main__':
    loop.run_until_complete(main())
