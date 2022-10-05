#%%

import pandas as pd
import os
import json
import simplejson
import numpy as np

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
    for name in DICT_E_URL.keys():
        comp_name = name.split("_")[0]
        result[comp_name] = {}

        file_name = os.path.join(DATA_DIR, "electricity", f"{name}.csv")
        h_p, m5_a, rt_date, rt_hour = get_e_realtime(file_name)

        if comp_name == "Tohoku":
            m5_cols = [
                "DATE",
                "TIME",
                "Actual Usage",
                "Solar Power Generation",
                "Wind Power Generation",
            ]
        elif comp_name == "Tokyo":
            m5_cols = [
                "DATE",
                "TIME",
                "Actual Usage",
                "Solar Power Generation",
                "Solar Power Consumption",
            ]
        else:
            m5_cols = ["DATE", "TIME", "Actual Usage", "Solar Power Generation"]

        if comp_name == "Kyushu":
            h_cols = [
                "DATE",
                "TIME",
                "Actual Usage (10MW)",
                "Forecast (10MW)",
                "Usage rate (%)",
                "Reserve rate (%)",
                "Estimated supply capacity (10MW)",
            ]
        else:
            h_cols = [
                "DATE",
                "TIME",
                "Actual Usage (10MW)",
                "Forecast (10MW)",
                "Usage rate (%)",
                "Estimated supply capacity (10MW)",
            ]

        h_p.columns = h_cols
        m5_a.columns = m5_cols

        m5_h_df = pd.DataFrame(np.repeat(h_p.values, 12, axis=0), columns=h_p.columns)

        # m5_a["Actual Usage (10MW)"] = m5_h_df["Actual Usage (10MW)"].values
        m5_a["Forecast (10MW)"] = m5_h_df["Forecast (10MW)"].values
        m5_a["Estimated supply capacity (10MW)"] = m5_h_df[
            "Estimated supply capacity (10MW)"
        ].values

        result[comp_name]["date"] = rt_date
        result[comp_name]["hour"] = rt_hour
        result[comp_name]["data"] = m5_a.to_dict(orient="records")

    encoded_unicode = simplejson.dumps(result, ignore_nan=True)
    return json.loads(encoded_unicode)
