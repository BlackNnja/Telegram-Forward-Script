#    _____                  __   __      __  _____         __             .___
#   /     \   ____  _______/  |_/  \    /  \/  |  |  _____/  |_  ____   __| _/
#  /  \ /  \ /  _ \/  ___/\   __\   \/\/   /   |  |_/    \   __\/ __ \ / __ | 
# /    Y    (  <_> )___ \  |  |  \        /    ^   /   |  \  | \  ___// /_/ | 
# \____|__  /\____/____  > |__|   \__/\  /\____   ||___|  /__|  \___  >____ | 
#         \/           \/              \/      |__|     \/          

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
    'keywords': ['@username1', 'Any Text',],    # List of usernames to filter out
}
# Max message length (Telegram's maximum for text messages)
MAX_MESSAGE_LENGTH = 4096  # Characters limit for Telegram messages
MAX_CAPTION_LENGTH = 1024  # Telegram's maximum caption length for media messages

# Create the Telegram client
client = TelegramClient('session_name', api_id, api_hash)

# ============================
# Utility Functions
# ============================

def apply_filters(message_text: str, entities=None):
    """
    Apply the configured filters to the message text and embedded links.
    Returns the filtered message text.
    """
    if not message_text:
        return ''

    # Filter embedded links (e.g., in words)
    if entities:
        for entity in entities:
            if hasattr(entity, 'url'):
                for keyword in FILTER_CONFIG['keywords']:
                    if keyword.lower() in entity.url.lower():
                        message_text = re.sub(re.escape(entity.url), '', message_text, flags=re.IGNORECASE)

    # Filter unwanted keywords from plain text (case-insensitive)
    if FILTER_CONFIG['keywords']:
        for keyword in FILTER_CONFIG['keywords']:
            message_text = re.sub(re.escape(keyword), '', message_text, flags=re.IGNORECASE)

    return message_text.strip()

def embed_links_in_text(text, entities):
    """
    Embed links properly in the message text at the correct places.
    """
    if not entities:
        return text

    # Go through entities and replace URLs in text with the correct link format
    result_text = text
    offset_shift = 0  # To track the position shift due to embedded links

    for entity in entities:
        if hasattr(entity, 'url'):
            link_text = text[entity.offset:entity.offset + entity.length]
            formatted_link = f"[{link_text}]({entity.url})"
            result_text = result_text[:entity.offset + offset_shift] + formatted_link + result_text[entity.offset + entity.length + offset_shift:]
            offset_shift += len(formatted_link) - len(link_text)  # Update the shift for the next links

    return result_text

def split_message(text):
    """
    Split the message into chunks if it exceeds the maximum allowed length.
    """
    if len(text) <= MAX_MESSAGE_LENGTH:
        return [text]

    # Split the text into chunks of MAX_MESSAGE_LENGTH length
    return [text[i:i+MAX_MESSAGE_LENGTH] for i in range(0, len(text), MAX_MESSAGE_LENGTH)]

def split_caption(caption):
    """
    Split the caption into chunks if it exceeds the maximum allowed caption length.
    """
    if len(caption) <= MAX_CAPTION_LENGTH:
        return [caption]

    # Split the caption into chunks of MAX_CAPTION_LENGTH length
    return [caption[i:i+MAX_CAPTION_LENGTH] for i in range(0, len(caption), MAX_CAPTION_LENGTH)]

# ============================
# Message Forwarding
# ============================

async def forward_last_messages(num_messages):
    """
    Forward the last messages from the specified source chats to the target group.
    """
    print("🔄 Bot is forwarding the last messages. Please wait...")
    for channel in source_chats:
        try:
            entity = await client.get_entity(channel)
            async for message in client.iter_messages(entity, limit=num_messages):
                await forward_message(message)
        except Exception as e:
            print(f"Error with channel {channel}: {e}")

    print("✅ Forwarding complete. Bot is now listening for new messages.")

async def forward_message(message):
    """
    Forward a single message after applying filters and preserving embedded links.
    """
    try:
        # Filter the message text
        caption = apply_filters(message.message, message.entities)

        # Embed the links back into the message content at the correct positions
        caption = embed_links_in_text(caption, message.entities)

        # Split the message if it's too long
        message_parts = split_message(caption)

        # Handle the media (if any)
        if message.media is None:
            sent_message = await client.send_message(group_id, message_parts[0], parse_mode='md')
            for part in message_parts[1:]:
                await client.send_message(group_id, part, reply_to=sent_message.id, parse_mode='md')
        else:
            if isinstance(message.media, (MessageMediaPhoto, MessageMediaDocument)):
                # Split the caption if it's too long
                caption_parts = split_caption(caption)

                # Send the media with the first part of the caption
                sent_message = await client.send_file(group_id, file=message.media, caption=caption_parts[0], parse_mode='md')

                # Reply with the remaining caption parts, indicating it's a continuation
                for part in caption_parts[1:]:
                    await client.send_message(group_id, part, reply_to=sent_message.id, parse_mode='md')

                    # Send a message indicating this is a continuation of the previous post
                    continuation_message = f"📝 Continuation of the previous post..."
                    await client.send_message(group_id, continuation_message, reply_to=sent_message.id)

            else:
                sent_message = await client.send_message(group_id, message_parts[0], parse_mode='md')
                for part in message_parts[1:]:
                    await client.send_message(group_id, part, reply_to=sent_message.id, parse_mode='md')

    except Exception as e:
        print(f"Error forwarding message: {e}")

# ============================
# Event Handlers
# ============================

@client.on(events.NewMessage(chats=source_chats))
async def handler(event):
    """
    Handles new messages from the source chats and forwards them after applying filters.
    """
    await forward_message(event.message)

# ============================
# Main Execution
# ============================

async def main():
    """
    Start the message forwarding process and allow dynamic addition of filters.
    """
    while True:
        print("\nOptions:")
        print("1. Add a filter keyword")
        print("2. View current filters")
        print("3. Forward last messages")
        print("4. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            keyword = input("Enter a keyword, URL, or username to filter: ").strip()
            if keyword:
                FILTER_CONFIG['keywords'].append(keyword)
                print(f"Keyword '{keyword}' added to the filter list.")

        elif choice == "2":
            print("Current Filters:", FILTER_CONFIG['keywords'])

        elif choice == "3":
            try:
                num_messages = int(input("Enter the number of last messages to forward from each group (max 10): "))
                num_messages = min(num_messages, 10)  # Ensure it does not exceed 10
                print("🔄 Bot is starting...")
                await forward_last_messages(num_messages)
                print("✅ Bot is now listening for new messages.")
            except ValueError:
                print("Invalid number. Please enter a valid integer.")

        elif choice == "4":
            print("Exiting...")
            break

        else:
            print("Invalid option. Please choose a valid number.")

# Run the main function
print("Client is running...")
client.start(phone_number)
client.loop.run_until_complete(main())
