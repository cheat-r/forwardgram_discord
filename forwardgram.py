import os
from telethon import TelegramClient, events
from telethon.tl.types import InputChannel
import yaml
import disnake
from disnake import Webhook
import aiohttp
import asyncio

# Crutch for attaching attaches in same message as they were sent, because Telegram doesn't do that for some reason 
wait = False
files = []

with open('config.yml', 'rb') as f:
    config = yaml.safe_load(f)

client = TelegramClient('forwardgram-discord', config['api_id'], config['api_hash'])
client.start()

# Channels parsing
channels = []
if not (False in config['channel_names']):
    print("You're using channel names in your config!\nWe recommend using channel IDs as they're rename and repeat-proof.\nYou can get it either by enabling experimental \"Show Peer IDs\" setting in desktop or, if you're on mobile (for some reason), by using modded client and enabling it there.\nMake sure to use Telegam API, not Bot API!\n") 
for d in client.iter_dialogs():
    if not (False in config['channel_names']):
        if d.entity.id in config['channel_ids']:
            channels.append(InputChannel(d.entity.id, d.entity.access_hash))
    if not (False in config['channel_names']):
        if d.name in config['channel_names']:
            if not InputChannel(d.entity.id, d.entity.access_hash) in channels:
                channels.append(InputChannel(d.entity.id, d.entity.access_hash))
            else:
                if d.entity.id in config['channel_ids']:
                    print('Your config has same channel in ID and name entries!\nWe recommend removing channel name entry to avoid any unwanted forwards if another channel changes their name to one in config.\n')
                else:
                    print('You have two (or more) channels with same name as in config!\nTo not break anything, program will be stopped.\nUse ID, rename your channel or leave channels with same name to proceed.')
                    exit()
if channels == []:
    print("No channels found.\nMake sure that you've inputted channel IDs and/or channel names in config.yml correctly.")
    exit()

# Config reload
@client.on(events.NewMessage(outgoing=True,forwards=False,pattern='!reload'))
async def handler(event):
    global config
    with open('config.yml', 'rb') as f:
        config = yaml.safe_load(f)
    await event.edit('Config reloaded.')
    await asyncio.sleep(5)
    await event.delete()

# Channel list reload (use after !reload)
@client.on(events.NewMessage(outgoing=True,forwards=False,pattern='!reparse'))
async def handler(event):
    global channels
    channels = []
    async for d in client.iter_dialogs():
        if not (False in config['channel_ids']):
            if d.entity.id in config['channel_ids']:
                channels.append(InputChannel(d.entity.id, d.entity.access_hash))
        if not (False in config['channel_names']):
            if d.name in config['channel_names']:
                if not InputChannel(d.entity.id, d.entity.access_hash) in channels:
                    channels.append(InputChannel(d.entity.id, d.entity.access_hash))
                elif not d.entity.id in config['channel_ids']:
                    print('You have two (or more) channels with same name as in config!\nTo not break anything, program will be stopped.\nUse ID, rename your channel or leave channels with same name to proceed.')
                    await event.edit('You have >=2 channels with same name! Check console for more info.')
                    await asyncio.sleep(5)
                    await event.delete()
                    exit()
    if channels == []:
        print("No channels found.\nMake sure that you've inputted channel IDs and/or channel names in config.yml correctly.")
        await event.edit('No channels found! Check console for more info.')
        await asyncio.sleep(5)
        await event.delete()
        exit()
    await event.edit('Channels reparsed.')
    await asyncio.sleep(5)
    await event.delete()

# Grabbing messages
@client.on(events.NewMessage(chats=channels))
async def handler(event):
    msg = event.message.text
    async with aiohttp.ClientSession() as session:
        global wait, files
        webhook = Webhook.from_url(config['discord_webhook_url'], session=session)
        embed = disnake.Embed()
        if config['output_channel_source'] or event.message.post_author or event.message.reply_to:
            reply = await event.message.get_reply_message()
            if reply: embed.description = f'>>> {reply.text}'+('\n' if reply.text else '')+('(Sticker)' if reply.sticker else '(Poll)' if reply.poll else '(Voice)' if reply.voice else '(Gif)' if reply.gif else '(Document)' if reply.document else '(Media)' if reply.media else '')
            if config['output_channel_source']:
                channel = await event.get_chat()
                embed.set_footer(text=f'Forwarded from {channel.title}')
            if event.message.post_author:
                embed.set_author(name=f'Sent by {event.message.post_author}')
        else: embed = None
        if event.message.media and not event.web_preview:
            media = await event.message.download_media()
            file = disnake.File(fp=media)
            os.remove(media)
            wait = True
            files.append(file)
            await asyncio.sleep(1)
            if wait == True:
                wait = False
                if msg:
                    await webhook.send(msg,embed=embed,files=files)
                else:
                    await webhook.send(embed=embed,files=files)
                files = []
        else: await webhook.send(msg,embed=embed)

print("Init complete; Starting listening for messages...\n------")
client.run_until_disconnected()
