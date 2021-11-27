import logging
import time
import pandas as pd
from tqdm.rich import tqdm


from telethon.sync import TelegramClient
from rich.logging import RichHandler

from config import api_id, api_hash, session_name

from services import get_range, clean_data_folder, load_json_and_combine


logging.basicConfig(
    filename="telegram_scraper.log",
    level=logging.INFO,
    format="%(asctime)s:%(levelname)s:%(message)s",
)

logging.getLogger().addHandler(RichHandler())

missing_offset = dict()
offset_start = 0
LIMIT = 99
channel = "vv_volodin"


def save_to_json(all_dict, offset):
    df = pd.DataFrame.from_records(all_dict)
    # Write the new DataFrame to a new SQLite table
    df_id = df.from_id.apply(pd.Series)
    df_to_store = pd.concat([df[["date", "message"]], df_id[["user_id"]]], axis=1)
    df_to_store.to_json(f"./data/offset_{offset}.json", force_ascii=False)


def get_offset_message(client, offset):
    all_dict = []
    for message in client.iter_messages(
        channel, limit=LIMIT + 1, reply_to=220, add_offset=offset
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
        message_id_220 = client.get_messages(channel, ids=220)
        total_count_replies = message_id_220.to_dict()["replies"]["replies"]
        logging.info(f"Total Replies : {total_count_replies}")
        range_to_scrape = get_range(offset_start, total_count_replies, LIMIT)

        bar = tqdm(total=total_count_replies)

        for i in range_to_scrape:
            bar.update(LIMIT)
            time.sleep(1)
            try:
                message_counts = get_offset_message(client, i)

            except Exception as e:
                logging.error(f"error for offset: {i}: ")
                logging.error(e)
                missing_offset[i] = {"status": False, "count": -1}
            finally:
                df_status = pd.DataFrame.from_dict(
                    missing_offset, orient="index", columns=["status", "count"]
                )
                df_status.reset_index(inplace=True)
                df_status.columns = ["offset", "status", "count"]
                df_status.to_csv("./data/status.csv")
                if message_counts < LIMIT:
                    print("Warning limit reached !!!")
                    time.sleep(60 * 5)


if __name__ == "__main__":
    clean_data_folder()
    main()
    load_json_and_combine()

