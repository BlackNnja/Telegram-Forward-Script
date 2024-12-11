
# Telegram Forwarder Script 📡

This Python script allows you to forward messages from specified Telegram channels to a designated group. It uses the Telethon library to interact with the Telegram API.

When Bots Starts it will forward the Last Message from each Group / Channel , And after that it will Monitor And forward Automatically the messages to the desired Group \ Channel .

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
- Filter out tags (mentions) and preserve new lines in messages. ✂️
- Automatically append URLs from message entities. 🔗
- Handle media messages (photos and documents). 🖼️📄
- Custom filters to remove unwanted words, usernames, and links. 🔍

## Requirements
- Python 3.7 or higher 🐍
- Telethon library 📦

## Installation
Follow these steps to install and set up the Telegram Forwarder Script:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/BlackNnja/Telegram-Forward-Script.git
   cd telegram-forwarder
   ```

2. **Install the required packages**:
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

## Customizing Message Filtering ✂️

This section explains how you can customize the message filtering in the Telegram Forwarder Script to suit your needs. You can modify the script to remove specific tags, replace usernames, and filter out messages based on certain criteria.

### 1. Removing Specific Tags (Mentions)

By default, the script removes all tags (mentions) from the messages. You can customize this behavior to exclude specific usernames or tags. Here's how you can modify the filtering settings:

1. **Modify the `FILTER_CONFIG` dictionary**:
   In the script, you will find the `FILTER_CONFIG` dictionary. It allows you to customize the filtering process. To filter out specific usernames or words, update the dictionary as follows:

   ```python
   FILTER_CONFIG = {
       'words': ['spam', 'advertisement'],  # Words to filter out
       'usernames': ['@username1', '@username2'],  # Usernames to filter out
       'links': True  # Set to True to remove URLs from messages
   }
   ```

2. **Filter Words**:
   To remove specific words from messages, add them to the `words` list:
   ```python
   FILTER_CONFIG['words'] = ['unwantedword1', 'unwantedword2']
   ```

3. **Filter Usernames**:
   To remove mentions of specific usernames, add them to the `usernames` list:
   ```python
   FILTER_CONFIG['usernames'] = ['@username1', '@username2']
   ```

4. **Remove Links (URLs)**:
   To remove URLs from the messages, set the `links` value to `True`:
   ```python
   FILTER_CONFIG['links'] = True  # Set this to False to keep links
   ```

### 2. Example of Custom Filter Configuration

```python
FILTER_CONFIG = {
    'words': ['spam', 'advertisement'],    # Words to filter out
    'usernames': ['@user1', '@bot'],        # Usernames to filter out
    'links': True                           # Set to True to remove URLs
}
```

### 3. Where to Apply Filters

The `apply_filters` function in the script is responsible for applying the configured filters to each message before it is forwarded. The filters work as follows:
- **Words**: Filters out unwanted words from the message text.
- **Usernames**: Filters out mentions of specific usernames.
- **Links**: Filters out URLs using regular expressions.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

If you have any questions or need help, feel free to open an issue on the GitHub repository. Happy forwarding! 🎉
```
