#    _____                  __   __      __  _____         __             .___
#   /     \   ____  _______/  |_/  \    /  \/  |  |  _____/  |_  ____   __| _/
#  /  \ /  \ /  _ \/  ___/\   __\   \/\/   /   |  |_/    \   __\/ __ \ / __ | 
# /    Y    (  <_> )___ \  |  |  \        /    ^   /   |  \  | \  ___// /_/ | 
# \____|__  /\____/____  > |__|   \__/\  /\____   ||___|  /__|  \___  >____ | 
#         \/           \/              \/      |__|     \/          \/     \/


# =============================================================================
# Telegram Forwarder Script 📡
# =============================================================================
# This is a Telegram message forwarder script that forwards messages from 
# specific Telegram groups or channels to another group. The script supports 
# filtering out specific text, words, usernames, and links from forwarded messages.

# How it works:
# 1. This script uses the Telethon library to interact with the Telegram API.
# 2. You need to provide your own API credentials (API_ID, API_HASH, and your phone number).
# 3. You can specify the channels/groups from which you want to forward messages.
# 4. You can set up different filters (words, usernames, links) to ignore unwanted content.
# 5. It forwards messages (with optional media) to a target group.

# Steps to configure:
# 1. Replace `YOUR_API_ID`, `YOUR_API_HASH`, and `YOUR_PHONE_NUMBER` with your values.
# 2. Add the source group or channel IDs to `source_chats` (can include usernames like 'source_chat_name').
# 3. Define custom filters for words, usernames, and links in the configuration section below.

# ============================
# Configuration Section 🔧
# ============================

from telethon import TelegramClient, events
from telethon.tl.types import MessageMediaPhoto, MessageMediaDocument
import re

# Replace these with your own values
api_id = 'YOUR_API_ID'  # Your API ID (🔑 Get it from https://my.telegram.org)
api_hash = 'YOUR_API_HASH'  # Your API Hash (🔑 Get it from https://my.telegram.org)
phone_number = 'YOUR_PHONE_NUMBER'  # Your phone number (e.g. '+123456789') 📞

# Group and channels to monitor
group_id = 'YOUR_GROUP_ID'  # Group ID to forward messages to
source_chats = ['SOURCE_CHAT_1', 'SOURCE_CHAT_2', 'SOURCE_CHAT_3', 'username_or_id']  # List of source chats (groups or channels)

# Filter configuration:
FILTER_CONFIG = {
    'words': ['unwantedword1', 'unwantedword2'],  # List of words to filter out
    'usernames': ['@username1', '@username2'],    # List of usernames to filter out
    'links': False,  # Set to True if you want to remove URLs (set to False if not)
}

# Create the Telegram client
client = TelegramClient('session_name', api_id, api_hash)

# ============================
# Message Forwarding Section 📬
# ============================

def apply_filters(message_text: str):
    """
    Apply the configured filters to the message text (words, usernames, links).
    Returns the filtered message text.
    """
    # Filter out unwanted words
    if FILTER_CONFIG['words']:
        for word in FILTER_CONFIG['words']:
            message_text = re.sub(r'\b' + re.escape(word) + r'\b', '', message_text, flags=re.IGNORECASE)

    # Filter out unwanted usernames (mentions)
    if FILTER_CONFIG['usernames']:
        for username in FILTER_CONFIG['usernames']:
            message_text = message_text.replace(username, '')

    # Filter out links (URLs)
    if FILTER_CONFIG['links']:
        message_text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', message_text)

    return message_text

async def forward_last_messages():
    """
    This function forwards the last messages from the specified source chats to the target group.
    It applies the configured filters and handles media files properly.
    """
    for channel in source_chats:
        try:
            async for message in client.iter_messages(channel, limit=1):
                caption = message.message

                # Apply filters to the caption text
                caption = apply_filters(caption)

                # Add URLs from message entities (if any)
                if message.entities:
                    for entity in message.entities:
                        if hasattr(entity, 'url'):
                            caption += f" {entity.url}"

                # Truncate long captions
                if len(caption) > 1024:
                    caption = caption[:1020] + '...'

                # Send message without media
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
    """
    This event handler listens for new messages in the specified source chats and forwards 
    them to the target group. Filters are applied to remove unwanted mentions and certain usernames.
    """
    message = event.message.message

    # Apply filters to the message text
    message = apply_filters(message)

    # Add URLs from message entities (if any)
    if event.message.entities:
        for entity in event.message.entities:
            if hasattr(entity, 'url'):
                message += f" {entity.url}"

    # Prepare the caption
    caption = message

    # Truncate long captions
    if len(caption) > 1024:
        caption = caption[:1020] + '...'

    # Send the message or media to the target group
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
    """
    Starts the message forwarding process by calling the function that forwards
    the last messages from the specified source chats.
    """
    await forward_last_messages()

client.loop.run_until_complete(main())
client.run_until_disconnected()
