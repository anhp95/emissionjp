#%%
import pandas as pd
import geopandas as gpd
import os
import numpy as np

# from mypath import EMS_TRACKER_DIR, EMS_TRACKER_FILES, AMD2_SHP
# from const import *

from core.mypath import (
    EMS_TRACKER_DIR,
    EMS_TRACKER_FILES,
    AMD2_SHP,
)

from core.const import *

DETAIL_SECTOR = [
    "manufacture",
    "construction_mining",
    "agriculture",
    "business",
    "building",
    "passenger_car",
    "freight_car",
    "railway",
    "ship",
    "waste",
]
AGG_SECTOR = ["industry_total", "consumer_total", "transportation_total", "waste"]
AVAILABLE_YEARS = [
    1990,
    2005,
    2007,
    2008,
    2009,
    2010,
    2011,
    2012,
    2013,
    2014,
    2015,
    2016,
    2017,
    2018,
    2019,
]
LIST_EMS_TRACKER_COLS = [
    ADM_CODE,
    "agriculture",
    "building",
    "business",
    "construction_mining",
    "consumer_total",
    "freight_car",
    "industry_total",
    "manufacture",
    "passenger_car",
    "railway",
    "ship",
    "transportation_total",
    "waste",
    "total",
]


def fix_chac_zip_code(df):
    adm_col = df[ADM_CODE].values

    fixed_list = []
    for city_code in adm_col:
        if city_code.startswith("0"):
            city_code = city_code[1:]
        fixed_list.append(city_code)
    df[ADM_CODE] = fixed_list
    return df


def fix_comma(col_values):

    fixed_list = []
    for text in col_values:
        if isinstance(text, str) and text.__contains__(","):
            text = text.replace(",", "")
        fixed_list.append(text)
    return fixed_list


def correct_shp_df():

    geo_df = gpd.read_file(AMD2_SHP)
    geo_df = fix_chac_zip_code(geo_df)
    geo_df[ADM_CODE] = geo_df[ADM_CODE].astype(int)

    return geo_df


def correct_df_col_to_int(ems_df, list_cols):

    ems_df = trans_cols(ems_df)

    for col in list_cols:
        ems_df[col] = fix_comma(ems_df[col].values)
        ems_df[col] = ems_df[col].astype(int)

    return ems_df


def merge_geo_emission_by_adm(**kwargs):
    def fix_duplicate_city(l):
        d = {}
        for i in range(len(l)):
            if l[i] in d:
                d[l[i]] += 1
                l[i] = f"{l[i]}_{str(d[l[i]])}"
            else:
                d[l[i]] = 0
        return l

    # list_cols = [
    #     ADM_CODE,
    #     "agriculture",
    #     "building",
    #     "business",
    #     "construction_mining",
    #     "consumer_total",
    #     "freight_car",
    #     "industry_total",
    #     "manufacture",
    #     "passenger_car",
    #     "railway",
    #     "ship",
    #     "transportation_total",
    #     "waste",
    #     "total",
    # ]

    year = kwargs["year"]
    ems_file = os.path.join(EMS_TRACKER_DIR, f"{year}.csv")
    ems_df = pd.read_csv(ems_file)
    ems_df = correct_df_col_to_int(ems_df, LIST_EMS_TRACKER_COLS)

    geo_df = correct_shp_df()
    merged_df = geo_df.merge(ems_df, left_on=ADM_CODE, right_on=ADM_CODE)

    if len(kwargs) > 1:
        adm_code = kwargs[ADM_CODE]
        return merged_df[merged_df[ADM_CODE] == int(adm_code)]

    result = []
    result.append(["Location", "Parent", "Emission"])
    result.append(["Japan", None, 0])

    merged_df["city"] = fix_duplicate_city(merged_df["city"].values)
    df = merged_df[["city", "pref", "total"]]

    for pref in df["pref"].unique():
        result.append([pref, "Japan", 0])
    for i in range(len(df)):
        arr = np.array(df.iloc[i].to_numpy()).tolist()
        for i in range(len(arr)):
            if isinstance(arr[i], np.int32) or isinstance(arr[i], np.int64):
                arr[i] = int(arr[i])
        result.append(arr)

    return result


def merge_emssion_by_sector():

    detail_result = [["Sector"] + DETAIL_SECTOR]
    agg_result = [["Sector"] + AGG_SECTOR]

    for year in AVAILABLE_YEARS:
        ems_csv = os.path.join(EMS_TRACKER_DIR, f"{year}.csv")
        df = trans_cols(pd.read_csv(ems_csv))
        df = correct_df_col_to_int(df, LIST_EMS_TRACKER_COLS)
        detail_data = [str(year)]
        agg_data = [str(year)]
        for ds in DETAIL_SECTOR:
            detail_data.append(int(df[ds].sum()))
        detail_result.append(detail_data)
        for aggs in AGG_SECTOR:
            agg_data.append(int(df[aggs].sum()))
        agg_result.append(agg_data)

    return detail_result, agg_result


def gen_geo_emission():
    for ems_file in EMS_TRACKER_FILES:
        print(ems_file.split("\\")[-1].split(".")[0])
        year = int(ems_file.split("\\")[-1].split(".")[0])
        ems_df = pd.read_csv(ems_file)
        ems_df = correct_df_col_to_int(ems_df, LIST_EMS_TRACKER_COLS)
        geo_df = correct_shp_df()
        df = geo_df.merge(ems_df, left_on=ADM_CODE, right_on=ADM_CODE)
        df["year"] = [year] * len(df)
        df.to_file(f"../data/ems_tracker/merged/{year}.json", driver="GeoJSON")


def trans_cols(df):
    df = df.rename(
        columns={
            "都道府県コード": "pref_code",
            "都道府県": "pref_name",
            "市区町村コード": ADM_CODE,
            "市区町村": "commune_name",
            "製造業": "manufacture",
            "建設業・鉱業": "construction_mining",
            "農林水産業": "agriculture",
            "産業部門　小計": "industry_total",
            "業務": "business",
            "家庭": "building",
            "民生部門　小計": "consumer_total",
            "旅客自動車": "passenger_car",
            "貨物自動車": "freight_car",
            "鉄道": "railway",
            "船舶": "ship",
            "運輸部門　小計": "transportation_total",
            "一般廃棄物": "waste",
            "排出量合計": "total",
        }
    )

    return df


# if __name__ == "__main__":
#     df = merge_geo_emission()


# %%
