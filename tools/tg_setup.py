"""One-shot: create the Telegram channel + discussion group for Crypto Momentum Lab.

Channels and groups can only be created by a user account, not a bot, so this
logs in as you (Telethon, MTProto). First run asks for the phone and the code
Telegram sends you; the session is saved next to this file and reused.

    export TG_API_ID=... TG_API_HASH=...     # from https://my.telegram.org -> API development tools
    .venv/bin/python tools/tg_setup.py

Optional: BOT_USERNAME=momentum_bot to add your bot as admin of both.
"""
from __future__ import annotations

import asyncio
import os
import sys
from pathlib import Path

from telethon import TelegramClient, functions, types
from telethon.errors import UsernameOccupiedError, UsernameInvalidError

ROOT = Path(__file__).resolve().parent.parent
LOGO = ROOT / "branding" / "logo.png"
SESSION = ROOT / "tools" / "tg_owner"

CHANNEL_TITLE = "Crypto Momentum Lab"
CHANNEL_USERNAMES = ["cryptomomentumlab", "momentumlab_crypto", "crypto_momentum_lab"]
CHANNEL_ABOUT = (
    "Моментум топовых криптовалют на одной шкале и бэктест ротации BTC ↔ альты. "
    "Сигналы, исследования, открытый код. Не инвестиционная рекомендация."
)
GROUP_TITLE = "Crypto Momentum Lab · Chat"
GROUP_USERNAMES = ["cryptomomentumlab_chat", "momentumlab_chat", "crypto_momentum_chat"]
GROUP_ABOUT = "Обсуждение Crypto Momentum Lab: метод, сигналы, код. Без рекламы и без гарантий доходности."

PINNED = (
    "**Crypto Momentum Lab**\n\n"
    "Сравниваем силу тренда крупных криптовалют на одной шкале, в процентах годовых, "
    "и проверяем на истории правило ротации BTC ↔ альткоины.\n\n"
    "Что здесь будет:\n"
    "• ежедневный срез моментума и смена слотов стратегии\n"
    "• разборы метода и честные бэктесты, включая то, что их завышает\n"
    "• код и изменения, всё открыто\n\n"
    "Дашборд: по запросу в чате. Код: github.com/Acnologiak/CryptoMomentumLab\n\n"
    "Это исследовательский инструмент, не инвестиционная рекомендация. "
    "Прошлые результаты не гарантируют будущих."
)


async def try_username(client, entity, candidates):
    for name in candidates:
        try:
            await client(functions.channels.UpdateUsernameRequest(channel=entity, username=name))
            return name
        except (UsernameOccupiedError, UsernameInvalidError):
            continue
    return None


async def main():
    api_id, api_hash = os.environ.get("TG_API_ID"), os.environ.get("TG_API_HASH")
    if not api_id or not api_hash:
        sys.exit("set TG_API_ID and TG_API_HASH (https://my.telegram.org)")

    async with TelegramClient(str(SESSION), int(api_id), api_hash) as client:
        me = await client.get_me()
        print("logged in as", me.first_name, me.username or me.id)

        ch = (await client(functions.channels.CreateChannelRequest(
            title=CHANNEL_TITLE, about=CHANNEL_ABOUT, broadcast=True, megagroup=False))).chats[0]
        print("channel created:", ch.id)
        gr = (await client(functions.channels.CreateChannelRequest(
            title=GROUP_TITLE, about=GROUP_ABOUT, broadcast=False, megagroup=True))).chats[0]
        print("group created:", gr.id)

        if LOGO.exists():
            photo = await client.upload_file(str(LOGO))
            for ent in (ch, gr):
                await client(functions.channels.EditPhotoRequest(
                    channel=ent, photo=types.InputChatUploadedPhoto(file=photo)))
            print("avatars set")

        ch_name = await try_username(client, ch, CHANNEL_USERNAMES)
        gr_name = await try_username(client, gr, GROUP_USERNAMES)

        # discussion group under the channel (comments)
        await client(functions.channels.SetDiscussionGroupRequest(broadcast=ch, group=gr))
        print("discussion linked")

        msg = await client.send_message(ch, PINNED, link_preview=False)
        await client.pin_message(ch, msg)

        bot = os.environ.get("BOT_USERNAME")
        if bot:
            rights = types.ChatAdminRights(post_messages=True, edit_messages=True,
                                           delete_messages=True, pin_messages=True,
                                           invite_users=True, manage_call=False)
            for ent in (ch, gr):
                await client(functions.channels.EditAdminRequest(
                    channel=ent, user_id=bot, admin_rights=rights, rank="bot"))
            print("bot added as admin:", bot)

        for label, ent, name in (("channel", ch, ch_name), ("group", gr, gr_name)):
            if name:
                print(f"{label}: https://t.me/{name}")
            else:
                inv = await client(functions.messages.ExportChatInviteRequest(peer=ent))
                print(f"{label}: no free username, invite link {inv.link}")


if __name__ == "__main__":
    asyncio.run(main())
