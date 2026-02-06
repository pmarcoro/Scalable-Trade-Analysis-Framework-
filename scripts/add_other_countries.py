import json
import pandas as pd
from src.in_out_utils import read_comtrade_json
from src.paths import RAW_PATH, RAW_PATH_EXP_STRUCTURE

def add_other_countries(
    flow_code: str,
    detailed_tag: str = "detailed",
    world_tag: str = "world"
):
    """
    Computes an aggregated 'Other countries' category for the Export Structure dashboard.

    File naming conventions:
        - Files containing country-level data must include: 'detailed'
        - Files containing world aggregates (ALL reporters) must include: 'world'

    The function computes:
        Other countries = World total - Sum of selected reporting countries

    The resulting dataset (selected countries + 'Other countries') is exported
    to the root raw data folder (data/raw/) so it can be automatically
    processed by the standard ETL pipeline (etl_all).

    Parameters
    flow_code : str
        "X" for exports, "M" for imports
    """

    detailed_dfs = []
    world_dfs = []


    # Read input JSON files

    for file in RAW_PATH_EXP_STRUCTURE.glob("*.json"):
        name = file.name.lower()
        df = read_comtrade_json(file)

        if detailed_tag in name:
            detailed_dfs.append(df)
        elif world_tag in name:
            world_dfs.append(df)

    if not detailed_dfs or not world_dfs:
        raise ValueError(
            "Detailed or world JSON files not found in export_structure folder. "
            "Ensure files are named using "
            f"'{detailed_tag}' and '{world_tag}'."
        )

    df_detailed = pd.concat(detailed_dfs, ignore_index=True)
    df_world = pd.concat(world_dfs, ignore_index=True)

    # Filter by trade flow

    df_detailed = df_detailed[df_detailed["flowCode"] == flow_code]
    df_world = df_world[df_world["flowCode"] == flow_code]

    # Detailed: keep only country reporters
    df_detailed = df_detailed[df_detailed["reporterCode"] >= 0]

    # World: keep only ALL reporters
    df_world = df_world[df_world["reporterCode"] == -2]

    # Rename world trade value key
    df_world = df_world.rename(
        columns={"primaryValue": "primaryValue_world"}
    )

    # Aggregate detailed countries

    df_detailed_agg = (
        df_detailed
        .groupby(["refYear", "cmdCode", "flowCode"], as_index=False)
        .agg(primaryValue_detailed=("primaryValue", "sum"))
    )

    df_merge = df_world.merge(
        df_detailed_agg,
        on=["refYear", "cmdCode", "flowCode"],
        how="left"
    )

    # Consistency check
    if not (
        df_merge["primaryValue_world"]
        >= df_merge["primaryValue_detailed"].fillna(0)
    ).all():
        print(" Warning: detailed sum exceeds world total for some HS/year")

    # Compute "Other countries"
    df_merge["primaryValue"] = (
        df_merge["primaryValue_world"]
        - df_merge["primaryValue_detailed"].fillna(0)
    ).clip(lower=0)

    # Build 'Other countries' records

    df_others = df_merge[
        ["freqCode", "refYear", "period", "cmdCode", "flowCode", "primaryValue"]
    ].copy()

    df_others["reporterCode"] = 9999
    df_others["reporterDesc"] = "Other countries"
    df_others["partnerCode"] = 0
    df_others["partnerDesc"] = "World"
    df_others["isAggregate"] = True

    if "commodity_group" in df_detailed.columns:
        df_others["commodity_group"] = df_detailed["commodity_group"].iloc[0]

    df_final = pd.concat(
        [df_detailed, df_others],
        ignore_index=True
    )

    ### Export df_final to RAW_PATH in JSON format
    output_file = RAW_PATH / f"export_structure_with_others_{flow_code}.json"

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(
            {"dataset": df_final.to_dict(orient="records")},
            f,
            ensure_ascii=False
        )

    print(f"✅ JSON saved to: {output_file}")

if __name__ == "__main__":
    add_other_countries(flow_code="X")