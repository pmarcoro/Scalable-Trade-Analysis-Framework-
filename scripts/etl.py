import pandas as pd
from pathlib import Path

import pandas as pd
from src.in_out_utils import read_comtrade_json
from src.paths import RAW_PATH, PROCESSED_PATH

def read_comtrade_json(path_in):
    """
    Reads a UN Comtrade JSON file and returns a pandas DataFrame.
    Assumes a valid JSON structure (list or dict with 'dataset').
    """
    import json
    with open(path_in, "r", encoding="utf-8") as f:
        data = json.load(f)

    if isinstance(data, dict) and "dataset" in data:
        data = data["dataset"]

    return pd.json_normalize(data)


def clean_data(df):
    """Cleans and standardizes columns"""
    # Renaming columns
    cols = {
        "refYear": "year",
        "cmdCode": "hs4",
        "primaryValue": "trade_value_usd"
    }
    df = df.rename(columns={key: value for key, value in cols.items() if key in df.columns})

    # Selecting columns to keep
    keep = [
        "freqCode", "year", "period", "hs4", "reporterCode",
        "flowCode", "partnerCode", "hs_code", "aggrLevel",
        "qtyUnitCode", "qty", "cifvalue", "fobvalue",
        "trade_value_usd", "isAggregate"
    ]
    df = df[[column for column in keep if column in df.columns]]

    # Basic cleaning
    if "trade_value_usd" in df.columns:
        df = df.dropna(subset=["trade_value_usd"])
    return df



def etl_all():
    """Reads all JSON files, cleans, tags, and exports a single parquet file"""

    all_dfs = []

    for file in RAW_PATH.glob("*.json"):
        print(f"Processing {file.name}")
        df = read_comtrade_json(file)
        df = clean_data(df)

        all_dfs.append(df)

    if all_dfs:
        combined_df = pd.concat(all_dfs, ignore_index=True)

        # Save combined parquet
        PROCESSED_PATH.mkdir(parents=True, exist_ok=True)
        combined_df.to_parquet(PROCESSED_PATH / "trade_data.parquet", index=False)
        print(f"✅ All JSON files combined and saved as '{PROCESSED_PATH / 'trade_data.parquet'}'")
    else:
        print("⚠️ No JSON files found in the raw path.")


if __name__ == "__main__":
    etl_all()
