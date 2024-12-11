# 📡 Telegram Forwarder Script

This is a Telegram message forwarder Python3 script created by a clever Israeli hacker 🤖🇮🇱 for the community at [t.me/israelihackers](https://t.me/israelihackers)! 

It forwards messages from specific Telegram groups, chats, or channels to another group, chat, or even your saved messages 📥. 

The script supports filtering out specific text, words, usernames, and links from forwarded messages, making it a powerful tool for managing your Telegram experience! 🚀✨

## 📋 Table of Contents
- [Features](#features)
- [Requirements](#requirements)
- [Configuration](#configuration)
- [How It Works](#how-it-works)
- [Setup Instructions](#setup-instructions)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## 🚀 Features
- Forward messages from multiple source channels, groups, or chats to a target group, chat, or saved messages.
- Filter out unwanted words, usernames, and links.
- Supports media forwarding (photos, documents).
- Handles users, chats, groups, and topics.
- Allows users to specify how many last messages to forward (up to 10).
- If the target group has topics, it will use the general topic that is numbered 2 as default.

## 🛠️ Requirements
- Python 3.7 or higher
- [Telethon](https://github.com/LonamiWebs/Telethon) library
- Telegram API credentials (API_ID, API_HASH, and phone number)

## ⚙️ Configuration
Before running the script, you need to configure it with your own values. Open `bot.py` and modify the following variables:

### API Credentials
Replace these with your own values:
```python
api_id = 'YOUR_API_ID'  # Your API ID (🔑 Get it from https://my.telegram.org)
api_hash = 'YOUR_API_HASH'  # Your API Hash (🔑 Get it from https://my.telegram.org)
phone_number = 'YOUR_PHONE_NUMBER'  # Your phone number (e.g. '+123456789') 📞
```

### Group and Channels to Monitor
```python
group_id = 'TARGET_GROUP_ID'  # Group ID to forward messages to (string format)
source_channels = ['SOURCE_CHANNEL_ID_1', 'SOURCE_CHANNEL_ID_2']  # List of source channel IDs (string format)
```

### Filter Configuration
```python
FILTER_CONFIG = {
    'words': ['unwantedword1', 'unwantedword2'],  # List of words to filter out
    'usernames': ['@username1', '@username2'],    # List of usernames to filter out
    'links': False,  # Set to True if you want to remove URLs (set to False if not)
}
```

## 🔍 How It Works
1. The script uses the Telethon library to interact with the Telegram API.
2. It forwards messages from specified source channels, groups, or chats to a target group, chat, or saved messages.
3. Filters are applied to remove unwanted content based on the configuration.
4. Media files are forwarded along with the messages when applicable.
5. Users are prompted to specify how many last messages to forward (up to 10).
6. Users must be a member of the source channels or groups to forward messages.
7. If the target group has topics, the script will use the general topic that is numbered 2 as the default.

## 📝 Setup Instructions
1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/telegram-forwarder.git
   cd telegram-forwarder
   ```

2. **Install the required packages:**
   ```bash
   pip install telethon
   ```

3. **Configure the script:**
   - Open `bot.py` and set your API credentials, target group ID, source channel IDs, and filter settings.

4. **Run the script:**
   ```bash
   python bot.py
   ```

## 📦 Usage
- The script will start running and will forward messages from the specified source channels, groups, or chats to the target group, chat, or saved messages.
- You will be prompted to enter the number of last messages to forward from each group (maximum 10).
- You can monitor the console for any errors or logs.

## 🤝 Contributing
Contributions are welcome! If you have suggestions or improvements, feel free to open an issue or submit a pull request.

## 📄 License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

Thank you for using the Telegram Forwarder Script! If you have any questions or need assistance, feel free to reach out. Happy forwarding! 🎉
