import os
import yaml
import aiohttp
import asyncio
from telethon import TelegramClient, events
from telethon.tl.types import InputChannel
import disnake
from disnake import Webhook

# Crutch for attaching attaches in same message as they were sent, because Telegram doesn't do that for some reason 
wait = False
files = []

with open('config.yml', 'rb') as f:
    config = yaml.safe_load(f)

client = TelegramClient('forwardgram-discord', config['api_id'], config['api_hash'])
client.start()

# Channels parsing
channels = []
for d in client.iter_dialogs():
    if d.entity.id in config['channel_ids']:
        channels.append(InputChannel(d.entity.id, d.entity.access_hash))
if channels == []:
    print("No channels found.\nHave you inputted channel IDs in config correctly? Are your account following those channels?")
    exit()

#! Temporarly disabled, broken and useless rn
"""# Config reload
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
        if d.entity.id in config['channel_ids']:
            channels.append(InputChannel(d.entity.id, d.entity.access_hash))
    if channels == []:
        print("No channels found.\nMake sure that you've inputted channel IDs and/or channel names in config.yml correctly.")
        await event.edit('No channels found!')
        await asyncio.sleep(5)
        await event.delete()
    await event.edit('Channels reparsed.')
    await asyncio.sleep(5)
    await event.delete()"""

# Handling messages
@client.on(events.NewMessage(chats=channels))
async def handler(event):
    msg = event.message
    txt = msg.text
    if txt.count("__") >= 2: txt = txt.replace("__", "*")
    async with aiohttp.ClientSession() as session:
        global wait, files
        webhook = Webhook.from_url(config['channel_ids'][msg.peer_id.channel_id] if msg.peer_id.channel_id in config['channel_ids'] and config['channel_ids'][msg.peer_id.channel_id] != None else config['default_webhook'], session=session)
        embed = disnake.Embed()
        if msg.reply_to:
            reply = await msg.get_reply_message()
            embed.description = f'>>> {reply.text}'+('\n' if reply.text else '')+('(Sticker)' if reply.sticker else '(Poll)' if reply.poll else '(Voice)' if reply.voice else '(Gif)' if reply.gif else '(Document)' if reply.document else '(Media)' if reply.media else '')
        elif msg.forward:
            channel = await msg.forward.get_chat()
            embed.set_footer(text=f'Forwarded from {channel.title}' + f' ({msg.forward.post_author})' if msg.forward.post_author else '')
        else: embed = None
        channel = await event.get_chat()
        username = f'{channel.title}' + f' ({msg.post_author})' if msg.post_author else ''
        if msg.media and not event.web_preview:
            media = await msg.download_media()
            file = disnake.File(fp=media)
            wait = True
            files.append(file)
            await asyncio.sleep(1)
            if wait == True:
                wait = False
                if txt:
                    await webhook.send(txt, embed=embed, files=files, username=username)
                else:
                    await webhook.send(embed=embed, files=files, username=username)
                files = []
                os.remove(media)
        else: await webhook.send(txt, embed=embed, username=username)

print("Init complete; Starting listening for messages...\n------")
client.run_until_disconnected()
