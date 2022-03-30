import pandas as pd

df = pd.read_excel(
    "data/yandex_searches/yandex_search.xlsx", sheet_name="history_all_regions"
)
df[["start", "end"]] = df["Period"].str.split("-\s", 1, expand=True)
df["start"] = pd.to_datetime(df["start"])
df["end"] = pd.to_datetime(df["end"])
df.to_excel(
    "data/yandex_searches/yandex_search.xlsx", sheet_name="history_all_regions_clean"
)

