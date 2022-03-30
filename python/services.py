from datetime import datetime
import pathlib
import shutil


def clean_data_folder():

    dirpath = pathlib.Path("./data")
    if dirpath.exists() and dirpath.is_dir():
        shutil.rmtree(dirpath)
    pathlib.Path("./data").mkdir(parents=True, exist_ok=True)


# create a sequence of offsets to scrap
def get_range(start, end, step):
    i = start
    while i < end:
        yield i
        i += step
    yield end


import pandas as pd
import pathlib


def load_json_and_combine():
    all_files = list(pathlib.Path("./data").glob("*.json"))
    all_df_list = list()
    for f in all_files:
        df = pd.read_json(f, encoding="UTF-8")
        all_df_list.append(df)

    df_all = pd.concat(all_df_list, axis=0)
    df_all = df_all.drop_duplicates(subset=["message", "user_id"])
    df_all["total_posts_of_user_id"] = df_all.groupby("user_id")["user_id"].transform(
        "count"
    )

    now = datetime.now()
    dt_string = now.strftime("%Y_%m_%d__%H:%M:%S")

    df_all.to_csv(
        f"./data_to_combine/vv_volodin_post_220_{dt_string}.csv",
        index=False,
        encoding="UTF-8",
    )


def combine_all_xlsx():
    all_files = list(pathlib.Path("./data_to_combine").glob("*.xlsx"))

    df_all_list = []

    for f in all_files:
        print(f)
        df_all_list.append(pd.read_excel(f, engine="openpyxl"))
    df_all = pd.concat(df_all_list, axis=0)
    df_all.drop_duplicates(inplace=True, subset=["user_id", "date", "message"])
    df_all.to_csv("df_all.csv", index=False, encoding="UTF-8")


# combine_all_xlsx()
