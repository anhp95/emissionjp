#%%

import pandas as pd
import os
import json
from core.ems_tracker.utils import (
    trans_cols,
    merge_geo_emission_by_city,
    merge_emssion_by_sector,
)


def emission_adm_filter(**kwargs):
    if len(kwargs) > 1:
        merge_df = merge_geo_emission_by_city(
            year=kwargs["year"], adm_code=kwargs["adm_code"]
        )
        data = json.loads(merge_df.to_json())
        return data

    merge_df = merge_geo_emission_by_city(year=kwargs["year"])
    result = merge_df.to_dict("records")
    encodedUnicode = json.dumps(result, ensure_ascii=False)
    return json.loads(encodedUnicode)


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
