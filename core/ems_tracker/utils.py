#%%
import pandas as pd
import geopandas as gpd
import os
import glob

# from mypath import EMISSION_DIR, EMISSION_FILES, AMD2_SHP, EMISSION_GEOJSON

from core.ems_tracker.mypath import (
    EMISSION_DIR,
    EMISSION_FILES,
    AMD2_SHP,
    EMISSION_GEOJSON,
)


def fix_chac_zip_code(df):
    adm_col = df["adm_code"].values

    fixed_list = []
    for city_code in adm_col:
        if city_code.startswith("0"):
            city_code = city_code[1:]
        fixed_list.append(city_code)
    df["adm_code"] = fixed_list
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
    geo_df["adm_code"] = geo_df["adm_code"].astype(int)

    return geo_df


def correct_df_col_to_int(ems_df):

    ems_df = trans_cols(ems_df)
    list_cols = [
        "adm_code",
        "agriculture",
        "building",
        "business",
        "construction_mining",
        "consumer_total",
        "freight_car",
        "industry_total",
        "manufature",
        "passenger_car",
        "railway",
        "ship",
        "transportation_total",
        "waste",
        "total",
    ]

    for col in list_cols:
        ems_df[col] = fix_comma(ems_df[col].values)
        ems_df[col] = ems_df[col].astype(int)

    return ems_df


def merge_geo_emission_by_city(**kwargs):

    year = kwargs["year"]
    ems_file = os.path.join(EMISSION_DIR, f"{year}.csv")
    ems_df = pd.read_csv(ems_file)
    ems_df = correct_df_col_to_int(ems_df)

    geo_df = correct_shp_df()
    merged_df = geo_df.merge(ems_df, left_on="adm_code", right_on="adm_code")

    if len(kwargs) > 1:
        adm_code = kwargs["adm_code"]
        return merged_df[merged_df["adm_code"] == int(adm_code)]

    return merged_df[
        [
            "city",
            "pref",
            "industry_total",
            "consumer_total",
            "transportation_total",
            "waste",
            "total",
        ]
    ]


def merge_emssion_by_sector():
    data = [
        ["Director (Year)", "Rotten Tomatoes", "IMDB"],
        ["Alfred Hitchcock (1935)", 8.4, 7.9],
        ["Ralph Thomas (1959)", 6.9, 6.5],
        ["Don Sharp (1978)", 6.5, 6.4],
        ["James Hawes (2008)", 4.4, 6.2],
    ]
    return data

    # list_ems_csv = glob.glob(os.path.join(EMISSION_DIR, "*.csv"))

    # for ems_csv in list_ems_csv:
    #     df = pd.read_csv(ems_csv)


def merge_all_geo_emission():
    list_df = []
    for ems_file in EMISSION_FILES:
        print(ems_file.split("\\")[-1].split(".")[0])
        year = int(ems_file.split("\\")[-1].split(".")[0])
        ems_df = pd.read_csv(ems_file)
        ems_df = correct_df_col_to_int(ems_df)
        geo_df = correct_shp_df()
        df = geo_df.merge(ems_df, left_on="adm_code", right_on="adm_code")
        df["year"] = [year] * len(df)
        list_df.append(df)

    merged_df = gpd.GeoDataFrame(pd.concat(list_df, ignore_index=True))
    # merged_df.to_file(EMISSION_GEOJSON, driver="GeoJSON")
    return merged_df


def trans_cols(df):
    df = df.rename(
        columns={
            "都道府県コード": "pref_code",
            "都道府県": "pref_name",
            "市区町村コード": "adm_code",
            "市区町村": "municipality",
            "製造業": "manufature",
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
