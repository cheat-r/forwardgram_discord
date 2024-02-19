import os
from telethon import TelegramClient, events
from telethon.tl.types import InputChannel
import yaml
import disnake
from disnake import Webhook
import aiohttp
import asyncio
wait = False
files = []

with open('config.yml', 'rb') as f:
    config = yaml.safe_load(f)

client = TelegramClient("forwardgram-discord", config["api_id"], config["api_hash"])
client.start()

# From where we should forward messages
input_channels_entities = []

for d in client.iter_dialogs():
    if d.name in config["input_channel_names"]:
        input_channels_entities.append( InputChannel(d.entity.id, d.entity.access_hash) )

if input_channels_entities == []:
    print("No channels found. Please make sure that you've inputted channel name(s) in config.yml correctly.")
    exit()


# Grabbing new messages
@client.on(events.NewMessage(chats=input_channels_entities))
async def handler(event):
    #! Known flaw: italic converts to underline because of different formatting of Telegram and Discord
    parsed_response = event.message.text
    async with aiohttp.ClientSession() as session:
        global wait, files
        webhook = Webhook.from_url(config["discord_webhook_url"], session=session)
        embed = disnake.Embed()
        if config["channel_source"]:
            channel = await event.get_chat()
            embed.set_footer(text='Forwarded from '+channel.title)
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
              if parsed_response:
                await webhook.send(parsed_response,embed=embed,files=files)
              else:
                await webhook.send(embed=embed,files=files)
              files = []
        else: await webhook.send(parsed_response,embed=embed)

print("Init complete; Starting listening for messages...\n------")
client.run_until_disconnected()
