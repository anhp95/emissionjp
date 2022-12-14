#%%
import pandas as pd
import geopandas as gpd
import os
import numpy as np
import csv
import wget
import shutil
import urllib

# from mypath import *
# from const import *

from core.mypath import *
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
            "?????????????????????": "pref_code",
            "????????????": "pref_name",
            "?????????????????????": ADM_CODE,
            "????????????": "commune_name",
            "?????????": "manufacture",
            "??????????????????": "construction_mining",
            "???????????????": "agriculture",
            "?????????????????????": "industry_total",
            "??????": "business",
            "??????": "building",
            "?????????????????????": "consumer_total",
            "???????????????": "passenger_car",
            "???????????????": "freight_car",
            "??????": "railway",
            "??????": "ship",
            "?????????????????????": "transportation_total",
            "???????????????": "waste",
            "???????????????": "total",
        }
    )

    return df


def drop_nan(df):

    for col in df.columns:
        df = df.dropna(subset=[col])

    return df


def update_e_file():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36"
    }
    electricity_dir = os.path.join(DATA_DIR, "electricity")
    shutil.rmtree(electricity_dir)
    os.mkdir(electricity_dir)
    for name in DICT_E_URL.keys():
        file_name = os.path.join(DATA_DIR, "electricity", f"{name}.csv")
        if os.path.exists(file_name):
            os.unlink(file_name)
        # wget.download(DICT_E_URL[name], out=file_name)
        
        req = urllib.request.Request(DICT_E_URL[name], headers=headers)
        res = urllib.request.urlopen(req)
        with open(file_name, "wb") as f:
            f.write(res.read())


def get_e_realtime(csv_path):

    hours = 24
    min5s = 60 / 5 * 24
    encoding = "shift_jis"

    row_indexes = []
    with open(csv_path, encoding=encoding) as file_obj:
        reader_obj = csv.reader(file_obj)
        for i, row in enumerate(reader_obj):
            if len(row) > 0 and row[0] == "DATE":
                row_indexes.append(i)

    h_p = pd.read_csv(csv_path, skiprows=row_indexes[0], nrows=hours, encoding=encoding)
    m5_a = pd.read_csv(
        csv_path, skiprows=row_indexes[1], nrows=min5s, encoding=encoding
    )
    rt_date = m5_a.DATE.unique()[0]
    rt_hour = m5_a.dropna().TIME.values[-1]
    return h_p, m5_a, rt_date, rt_hour


# %%
