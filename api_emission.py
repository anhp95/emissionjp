#%%

import pandas as pd
import os
from mypath import EMISSION_DIR
from utils import trans_cols, merge_geo_emission


def emission_by_year(year):
    ems_file = os.path.join(EMISSION_DIR, f"{year}.csv")
    merge_df = merge_geo_emission(ems_file)

    # return merge_df.to_json()
    return merge_df


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
