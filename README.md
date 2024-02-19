# <img src="resources/bricksmol.gif"> Forwardgram: Discord Webhook Edition — Forward Telegram Messages to Discord

<img src="resources/itjustworks.png">

## Description
Forwardgram is a script that uses your Telegram account for parsing new messages from one or more Telegram channels and forwards them to Discord channel using webhook. There's nothing you need to register (besides your own accounts)! Simple setup! Everything works out of a box!

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

In the first time initializing the script, you will be requried to validate your phone number using telegram API. This happens only at the first time (per session name).

## Authors
There's just too many.

* voidbar - [forwardgram](https://github.com/voidbar/forwardgram) (OG repo)
* kkapuria3 - [Telegram-To-Discord-Forward-Bot](https://github.com/kkapuria3/Telegram-To-Discord-Forward-Bot) (fork for reposting to discord instead of telegram)
* Sqble - [Telegram-To-Discord-Bot-Fixed](https://github.com/Sqble/Telegram-To-Discord-Bot-Fixed) (fork of fork?)
* cheat_r - forwardgram_discord-webhook (complete rewrite based on Sqble's fork)

## TODO
- [ ] Adapt Telegram text formatting to Discord
- [ ] Implement forwarding to several Discord webhooks simultaneously

## License
IDK and IDC, do whatewer you want with this. It's your account, after all.
