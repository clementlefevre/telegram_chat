import pandas as pd
import pathlib


def load_json():
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
    df_all.to_csv("vv_volodin_post_220.csv", index=False, encoding="UTF-8")
    df_all.to_excel(
        "vv_volodin_post_220.xlsx", index=False, encoding="UTF-8", engine="openpyxl"
    )


load_json()
