# <img src="resources/bricksmol.gif"> Forwardgram: Discord Webhook Edition — Forward Telegram Messages to Discord

## Description
Forwardgram is a script that uses your Telegram account for parsing new messages from one or more Telegram channels and forwards them to Discord channel using webhook. All you need is your Telegram and Discord accounts!

### Dependencies
- Python 3.8+ and libraries from `requirements.txt`
- Telegram account with valid phone number
- Discord webhook link

### Installing and Setup
1. Clone this repository
2. Install required libraries (simpliest way is to open cloned folder in console and running `python3 -m pip install -r requirements.txt` if you're on Windows, afaik it won't work on Linux and requires to create venv)
3. Fill out `config.yml` file
4. Run `python3 forwardgram.py`!

### Running and using
In the first time initializing the script, you will be requried to validate your phone number using Telegram API. This happens only at first time per session name. Don't worry, your account will be used only for reading messages, not for sending them (or anything else)!

If any errors occur, it means that you have filled something wrong in config. If not, please report it through Issues!

### Commands
Temporarly disabled, as they're broken right now.

## TODO
- [ ] Advanced attachments support, such as stickers, voice messages, polls, etc. (High priority)
- [ ] Adapt Telegram text formatting to Discord (Planned)
- [ ] Show replies to messages from other chats
- [ ] Message editing (?)
- [x] Implement forwarding to several Discord webhooks simultaneously

## License
This repository is NOT licenced (yet). You can do whatever you want with this code, as long as you mention me and other authors, if you plan to publish your own source code.
