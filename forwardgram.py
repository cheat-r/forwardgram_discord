import os
from telethon import TelegramClient, events
from telethon.tl.types import InputChannel
import yaml
import disnake
from disnake import Webhook
import aiohttp

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
    # If the message contains a URL, parse and send Message + URL
    try:
        parsed_response = (event.message.message + '\n' + event.message.entities[0].url )
        parsed_response = ''.join(parsed_response)
    # ...or we only send Message    
    except:
        parsed_response = event.message.message

    async with aiohttp.ClientSession() as session:
        webhook = Webhook.from_url(config["discord_webhook_url"], session=session)
        if config["channel_source"]:
            channel = await event.get_chat()
            embed = disnake.Embed()
            embed.set_author(name='Forwarded from '+channel.title)
        if event.message.media:
          media = await event.message.download_media()
          file = disnake.File(fp=media)
          await webhook.send(parsed_response,file=file,embed=embed)
          os.remove(media)
        else:
          await webhook.send(parsed_response,embed=embed)

print("Init complete; Starting listening for messages...\n------")
client.run_until_disconnected()
