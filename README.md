# <img src="resources/bricksmol.gif"> Forwardgram: Discord Webhook Edition — Forward Telegram Messages to Discord

<img src="resources/itjustworks.png">

## Description
Forwardgram is a script that uses your Telegram account for parsing new messages from one or more Telegram channels and forwards them to Discord channel using webhook. All you need is your Telegram and Discord accounts!

### Dependencies
- Python 3.6+
- Telegram account with valid phone number
- Discord webhook link (if you don't know what this is, check out Discord's [guide](https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks)).

### Installing and Setup
1. Clone this repository
2. Open cloned folder in your console
3. Run Command: `python3 -m pip install -r requirements.txt`.
4. Fill out `config.yml` file.

### Running
After filling out `config.yml` run command `python3 forwardgram.py`. Simple as that!

In the first time initializing the script, you will be requried to validate your phone number using Telegram API. This happens only at the first time (per session name). Don't worry, your account will be used only for reading messages, not for sending them (or anything else)!

## Authors
There's just too many.

* voidbar - [forwardgram](https://github.com/voidbar/forwardgram) (original repository made for use only inside telegram)
* kkapuria3 - [Telegram-To-Discord-Forward-Bot](https://github.com/kkapuria3/Telegram-To-Discord-Forward-Bot) (fork for reposting to discord instead of telegram)
* Sqble - [Telegram-To-Discord-Bot-Fixed](https://github.com/Sqble/Telegram-To-Discord-Bot-Fixed) (fix of fork, but still not so usable)
* cheat_r - forwardgram_discord (complete rewrite based on Sqble's fork; if you don’t praise yourself, no one will)

Why credit them? Because I appreciate their efforts to make our lives a bit easier. If not them, I probably wouldn't have taken on this project in the first place.

## TODO
- [ ] Advanced attachments support, such as stickers, voice messages, polls, etc. (High priority)
- [ ] Adapt Telegram text formatting to Discord (Planned)
- [ ] Show replied messages and message signing
- [ ] Message editing (?)
- [ ] Implement forwarding to several Discord webhooks simultaneously (?)

## License
This repository is NOT licenced (yet). You can do whatever you want with this code, as long as you mention me and other authors, if you plan to publish your own source code.
