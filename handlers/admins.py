from asyncio import QueueEmpty

from pyrogram import Client
from pyrogram.types import Message

from callsmusic import callsmusic, queues

from helpers.filters import command, other_filters
from helpers.decorators import errors, authorized_users_only


@Client.on_message(command("pause") & other_filters)
@errors
@authorized_users_only
async def pause(_, message: Message):
    if callsmusic.pause(message.chat.id):
        await message.reply_text("Lagu-mu Sudah Di-Pause/Dihentikan!")
    else:
        await message.reply_text("Aku Sudah Memberhentikan Lagu!")


@Client.on_message(command("resume") & other_filters)
@errors
@authorized_users_only
async def resume(_, message: Message):
    if callsmusic.resume(message.chat.id):
        await message.reply_text("Okeyy, Lagumu Sudah Di-Mulai!")
    else:
        await message.reply_text("Aku Tidak Bisa Memberhentikan Paksa Lagu!")


@Client.on_message(command("stop") & other_filters)
@errors
@authorized_users_only
async def stop(_, message: Message):
    if message.chat.id not in callsmusic.active_chats:
        await message.reply_text("Aku Tidak Bisa Memaksakan Berhentikan Lagu!")
    else:
        try:
            queues.clear(message.chat.id)
        except QueueEmpty:
            pass

        await callsmusic.stop(message.chat.id)
        await message.reply_text("Aku Sudah Keluar Dari Voice Call, Leave To Voice Call!")


@Client.on_message(command("skip") & other_filters)
@errors
@authorized_users_only
async def skip(_, message: Message):
    if message.chat.id not in callsmusic.active_chats:
        await message.reply_text("Maaf Tidak Bisa Diskip Paksa!")
    else:
        queues.task_done(message.chat.id)

        if queues.is_empty(message.chat.id):
            await callsmusic.stop(message.chat.id)
        else:
            await callsmusic.set_stream(
                message.chat.id, queues.get(message.chat.id)["file"]
            )

        await message.reply_text("Lagu Kamu Sudah Diskip, Next Lanjut Lagu Berikutnya!")


@Client.on_message(command("mute") & other_filters)
@errors
@authorized_users_only
async def mute(_, message: Message):
    result = callsmusic.mute(message.chat.id)

    if result == 0:
        await message.reply_text("Mute Aku!")
    elif result == 1:
        await message.reply_text("Sukses Mute Aku!")
    elif result == 2:
        await message.reply_text("Tidak Ada Chat!")


@Client.on_message(command("unmute") & other_filters)
@errors
@authorized_users_only
async def unmute(_, message: Message):
    result = callsmusic.unmute(message.chat.id)

    if result == 0:
        await message.reply_text("Unmute Aku!")
    elif result == 1:
        await message.reply_text("Sukses Un-Mute Aku!")
    elif result == 2:
        await message.reply_text("Tidak Ada Chat!")
