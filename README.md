# Telegram Forwarder Script 📡

This script allows you to forward messages from specified Telegram channels to a designated group. It uses the Telethon library to interact with the Telegram API.

## Table of Contents
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Custom Filter Configuration](#custom-filter-configuration)
- [License](#license)

## Features
- Forward messages from multiple channels to a group. 📬
- Filter out tags and preserve new lines in messages. ✂️
- Automatically append URLs from message entities. 🔗
- Handle media messages (photos and documents). 🖼️📄
- Custom filters to add on lines 76 - 78. 🔍

## Requirements
- Python 3.7 or higher 🐍
- Telethon library 📦

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/telegram-forwarder.git
   cd telegram-forwarder
   ```

2. Install the required packages:
   ```bash
   pip install telethon
   ```

## Configuration
Before running the script, you need to configure it with your Telegram API credentials and the channels you want to monitor.

1. **API Credentials**: 
   - Create a new application on [my.telegram.org](https://my.telegram.org) to get your `api_id` and `api_hash`. 🔑
   - Replace the following values in `bot.py`:
     ```python
     api_id = 'YOUR_API_ID'  # Your API ID
     api_hash = 'YOUR_API_HASH'  # Your API Hash
     phone_number = 'YOUR_PHONE_NUMBER'  # Your phone number
     ```

2. **Group and Channels**:
   - Set the `group_id` to the ID of the group where you want to forward messages. 🏷️
   - Update the `source_chats` list with the IDs or usernames of the channels you want to monitor:
     ```python
     source_chats = [CHANNEL_ID_1, CHANNEL_ID_2, 'username_or_id']
     ```

## Usage
1. Run the script:
   ```bash
   python bot.py
   ```

2. The script will start running and will forward messages from the specified channels to the designated group. 🚀


