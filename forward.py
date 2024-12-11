#    _____                  __   __      __  _____         __             .___
#   /     \   ____  _______/  |_/  \    /  \/  |  |  _____/  |_  ____   __| _/
#  /  \ /  \ /  _ \/  ___/\   __\   \/\/   /   |  |_/    \   __\/ __ \ / __ | 
# /    Y    (  <_> )___ \  |  |  \        /    ^   /   |  \  | \  ___// /_/ | 
# \____|__  /\____/____  > |__|   \__/\  /\____   ||___|  /__|  \___  >____ | 
#         \/           \/              \/      |__|     \/          \/     \/


# Telegram Forwarder Script 📡

# ============================
# Configuration Section 🔧
# ============================

from telethon import TelegramClient, events
from telethon.tl.types import MessageMediaPhoto, MessageMediaDocument

# Replace these with your own values
api_id = 'YOUR_API_ID'  # Your API ID (🔑 Get it from https://my.telegram.org)
api_hash = 'YOUR_API_HASH'  # Your API Hash (🔑 Get it from https://my.telegram.org)
phone_number = 'YOUR_PHONE_NUMBER'  # Your phone number (e.g. '+123456789') 📞

# Group and channels to monitor
group_id = 'YOUR_GROUP_ID'  # Group ID to forward messages to
source_chats = ['SOURCE_CHAT_1', 'SOURCE_CHAT_2', 'SOURCE_CHAT_3', 'username_or_id']  # Updated to include any chat type (Starts with -100**)

client = TelegramClient('session_name', api_id, api_hash)

# ============================
# Message Forwarding Section 📬
# ============================

async def forward_last_messages():
    for channel in source_chats:
        try:
            async for message in client.iter_messages(channel, limit=1):
                caption = message.message

                # Filter out tags from the caption while preserving new lines
                caption = '\n'.join(' '.join(word for word in line.split() if not word.startswith('@')) for line in caption.splitlines())

                if message.entities:
                    for entity in message.entities:
                        if hasattr(entity, 'url'):
                            caption += f" {entity.url}"

                if len(caption) > 1024:
                    caption = caption[:1020] + '...'

                if message.media is None:
                    await client.send_message(group_id, caption)
                else:
                    if isinstance(message.media, (MessageMediaPhoto, MessageMediaDocument)):
                        await client.send_file(group_id, file=message.media, caption=caption)
                    else:
                        await client.send_message(group_id, caption)
        except ValueError as e:
            print(f"Error retrieving messages from channel {channel}: {e}")

# ============================
# Event Handlers Section ⚙️
# ============================

@client.on(events.NewMessage(chats=source_chats))
async def handler(event):
    message = event.message.message

    # Filter out tags from the message while preserving new lines
    message = '\n'.join(' '.join(word for word in line.split() if not word.startswith('@')) for line in message.splitlines())

    if event.message.entities:
        for entity in event.message.entities:
            if hasattr(entity, 'url'):
                message += f" {entity.url}"

    message = message.replace("@****Israel2", "🇮🇱")

    if any(text.lower() in message.lower() for text in ["@termuxisrael2", "@bitsofgoldnews"]):
        return

    caption = message

    if len(caption) > 1024:
        caption = caption[:1020] + '...'

    if event.message.media is None:
        await client.send_message(group_id, caption)
    else:
        if isinstance(event.message.media, (MessageMediaPhoto, MessageMediaDocument)):
            await client.send_file(group_id, file=event.message.media, caption=caption)
        else:
            await client.send_message(group_id, caption)

# ============================
# Main Execution Section 🚀
# ============================

print("Client is running...")
client.start(phone_number)

async def main():
    await forward_last_messages()

client.loop.run_until_complete(main())
client.run_until_disconnected()
