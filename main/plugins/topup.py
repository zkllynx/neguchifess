from pyrogram import Client, enums, types, filters
from main.helpers import Database, Helper
from main.helpers.decorators import Bot
from main.guchi import Guchi


@Guchi.on_callback_query(filters.regex('^topup$'))
async def on_topup_inline(client: Client, query: types.CallbackQuery):
    msg = query.message
    pesan = 'Mohon diperhatikan dengan baik-baik.\n\n'
    pesan += 'harga ⦂ 1000 BZ = Rp.1000\n\n'
    pesan += 'Cara pembelian coin bz automatis⦂\n'
    pesan += '1. buka <link pembayaran>\n'
    pesan += '2. isi nominal top up\n'
    pesan += '3. isi email anda\n'
    pesan += '4. isi pesan : confes-user_id\n'
    pesan += 'contoh bila id anda 113012934: confes-113012934\n\n'
    pesan += '5. centang semua kolom\n'
    pesan += '6. pilih pembayaran\n\n'
    pesan += 'note:\n- segera hubungi @OxDonquixote bila coin tidak langsung didapatkan setelah tf\n\n'
    pesan += 'Untuk pembelian coin bz manual chat @OxDonquixote\n\n'
    pesan += 'Dengan membeli coin kalian dapat membantu kami untuk biaya perawatan server bot.\n\n'
    markup = types.InlineKeyboardMarkup([
        [types.InlineKeyboardButton('Rules', url='#'),
         types.InlineKeyboardButton('help', callback_data='help'),
         types.InlineKeyboardButton('status', callback_data='status')]
    ])

    await msg.edit(pesan, reply_markup=markup)


@Bot("topup")
async def on_topup_module_handler(client: Client, msg: types.Message, db: Database = None):
    db_user = db.get_data_pelanggan()
    pesan = 'Mohon diperhatikan dengan baik-baik.\n\n'
    pesan += 'harga ⦂ 1000 BZ = Rp.1000\n\n'
    pesan += 'Cara pembelian coin bz automatis⦂\n'
    pesan += '1. buka <link pembayaran>\n'
    pesan += '2. isi nominal top up\n'
    pesan += '3. isi email anda\n'
    pesan += '4. isi pesan : confes-user_id (seperti contoh di ss)\n'
    pesan += '5. centang semua kolom\n'
    pesan += '6. pilih pembayaran\n\n'
    pesan += 'note:\n- segera hubungi @OxDonquixote bila coin tidak langsung didapatkan setelah tf\n\n'
    pesan += 'Untuk pembelian coin bz manual chat @OxDonquixote\n\n'
    pesan += 'Dengan membeli coin kalian dapat membantu kami untuk biaya perawatan server bot.\n\n'
    gambar = "#"

    caption = msg.text or msg.caption
    entities = msg.entities or msg.caption_entities
    return await client.send_photo(db_user.id, gambar, pesan, parse_mode=enums.ParseMode.HTML,
                                   caption_entities=entities)
