#%%

import pandas as pd
import os
import json
import simplejson

from core.mypath import DATA_DIR
from core.utils import (
    trans_cols,
    merge_geo_emission_by_adm,
    update_e_file,
    get_e_realtime,
)
from core.const import *


def emission_adm_filter(**kwargs):
    if len(kwargs) > 1:
        merge_df = merge_geo_emission_by_adm(
            year=kwargs["year"], adm_code=kwargs["adm_code"]
        )
        data = json.loads(merge_df.to_json())
        return data

    merge_df = merge_geo_emission_by_adm(year=kwargs["year"])
    return {"result": merge_df}


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


def get_e_5mins():

    update_e_file()

    result = {}
    for comp_name in DICT_E_URL.keys():
        file_name = os.path.join(DATA_DIR, "electricity", f"{comp_name}.csv")
        _, m5_a = get_e_realtime(file_name)
        if comp_name == "Tohoku":
            cols = [
                "DATE",
                "TIME",
                "Actual Usage",
                "Solar Power Generation",
                "Wind Power Generation",
            ]
        elif comp_name == "Tokyo":
            cols = [
                "DATE",
                "TIME",
                "Actual Usage",
                "Solar Power Generation",
                "Solar Power Generation (Per Consumption)",
            ]
        else:
            cols = ["DATE", "TIME", "Actual Usage", "Solar Power Generation"]
        m5_a.columns = cols
        result[comp_name] = m5_a.to_dict(orient="records")

    encoded_unicode = simplejson.dumps(result, ignore_nan=True)
    return json.loads(encoded_unicode)
