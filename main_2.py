from sqlite3.dbapi2 import Time
from telethon.sync import TelegramClient
import time
import sqlite3


import pandas as pd

from config import api_id, api_hash, session_name

con = sqlite3.connect("telegram_vv_volodin.sqlite")

missing_offset = dict()
offset_start = 371100
LIMIT = 99


def myRange(start, end, step):
    i = start
    while i < end:
        yield i
        i += step
    yield end


def save_to_json(dicto):
    df = pd.DataFrame.from_records([dicto.to_dict()])
    # Write the new DataFrame to a new SQLite table
    df_id = df.from_id.apply(pd.Series)
    df_to_store = pd.concat([df[["date", "message"]], df_id[["user_id"]]], axis=1)
    df_to_store.to_sql("replies", con, if_exists="append")
    """ with open(f"vv_volodin_{i}.json", "w", encoding="utf-8", errors="ignore") as file:
        df[["from_id", "date", "message"]].to_json(file, force_ascii=False) """


def save_to_json(all_dict, offset):
    df = pd.DataFrame.from_records(all_dict)
    # Write the new DataFrame to a new SQLite table
    df_id = df.from_id.apply(pd.Series)
    df_to_store = pd.concat([df[["date", "message"]], df_id[["user_id"]]], axis=1)
    df_to_store.to_json(f"./data/offset_{offset}.json", force_ascii=False)


def get_offset_message(client, offset):
    all_dict = []
    for message in client.iter_messages(
        "vv_volodin", limit=LIMIT + 1, reply_to=220, add_offset=offset
    ):
        all_dict.append(message.to_dict())

    messages_count = len(all_dict)
    if messages_count >= LIMIT:
        save_to_json(all_dict, offset)
        missing_offset[offset] = {"status": True, "count": messages_count}
    else:
        missing_offset[offset] = {"status": False, "count": messages_count}

    return messages_count


def main():
    with TelegramClient(session_name, api_id, api_hash) as client:

        for i in myRange(offset_start, 562593, LIMIT):
            print(i)
            try:
                message_counts = get_offset_message(client, i)
                # time.sleep(2)
            except Exception as e:
                print(f"for : {i}: ", e)
                missing_offset[i] = {"status": False, "count": -1}
            finally:
                df_status = pd.DataFrame.from_dict(
                    missing_offset, orient="index", columns=["status", "count"]
                )
                df_status.reset_index(inplace=True)
                df_status.columns = ["offset", "status", "count"]
                df_status.to_csv("status.csv")
                if message_counts < LIMIT:
                    time.sleep(60 * 5)


if __name__ == "__main__":
    main()

