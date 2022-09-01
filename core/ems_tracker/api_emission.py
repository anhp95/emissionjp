#%%

import pandas as pd
import os
import json
from core.ems_tracker.utils import trans_cols, merge_geo_emission_by_city


def emission_by_year(year, adm_code):

    merge_df = merge_geo_emission_by_city(year, adm_code)
    data = json.loads(merge_df.to_json())
    return data


def agg_by_pref(ems_file):

    df = pd.read_csv(ems_file)
    df = trans_cols(df)

    emission_cols = [
        "manufature",
        "construction_mining",
        "agriculture",
        "industry_total",
        "business",
        "building",
        "consumer_total",
        "passenger_car",
        "freight_car",
        "railway",
        "ship",
        "transportation_total",
        "waste",
        "total",
    ]
    df = df.replace(",", "", regex=True)

    for col in emission_cols:
        df[col] = df[col].astype(float)

    pref_df = df.groupby("pref_name", as_index=False).agg(
        {cols: "sum" for cols in emission_cols}
    )
    # df.sort_values('2')

    return pref_df


# %%
