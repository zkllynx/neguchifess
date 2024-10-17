import re
from config import kata_terlarang
from main.database.clone_db import Clone

dbclone = Clone(0)
bots = []
main_bot: int = 0

def is_bad(text):
    pattern = re.compile(r'\b(?:%s)\b' % kata_terlarang, re.IGNORECASE)
    match = re.search(pattern, text)
    return match is not None

def set_main_bot(bot_id: int):
    global main_bot
    main_bot = bot_id

