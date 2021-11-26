from telethon import TelegramClient, events, sync
import asyncio
from telethon.tl import functions, types
import pandas as pd

from config import api_id, api_hash, session_name


client = TelegramClient(session_name, api_id, api_hash)
client.start()

all_dict = []


async def main():
    channel = await client.get_entity("vv_volodin")
    messages = await client.get_messages(channel, limit=None)  # pass your own args

    # then if you want to get all the messages text
    for x in messages:
        print(x.text)
        all_dict.append(x.to_dict())  # return message.text


loop = asyncio.get_event_loop()
loop.run_until_complete(main())


df = pd.DataFrame.from_records(all_dict)
df.to_csv("vv_volodin.csv", encoding="UTF-8")
