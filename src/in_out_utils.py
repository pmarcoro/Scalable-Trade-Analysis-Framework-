# in_out_utils
import json
import pandas as pd

def read_comtrade_json(path_in):
    """
    Reads a UN Comtrade JSON file and returns a pandas DataFrame.
    """
    with open(path_in, "r", encoding="utf-8") as f:
        data = json.load(f)

    if isinstance(data, dict) and "dataset" in data:
        data = data["dataset"]

    return pd.json_normalize(data)
