#%%
import pandas as pd
import geopandas as gpd
from mypath import EMISSION_FILES, AMD2_SHP, EMISSION_GEOJSON

def fix_chac_zip_code(df):
    adm_col = df["adm_code"].values

    fixed_list = []
    for city_code in adm_col:
        if city_code.startswith("0"):
            city_code = city_code[1:]
        fixed_list.append(city_code)
    df["adm_code"] = fixed_list
    return df

def fix_comma(df_col):
    fixed_list = []
    for text in df_col:
        if text.__contains__(","):
            text = text.replace(",", "")
        fixed_list.append(text)
    return fixed_list

def correct_shp_df():
    
    geo_df = gpd.read_file(AMD2_SHP)
    geo_df = fix_chac_zip_code(geo_df)
    geo_df['adm_code'] = geo_df['adm_code'].astype(int)

    return geo_df


def correct_ems_df(ems_df):
    
    ems_df = trans_cols(ems_df)

    ems_df['adm_code'] = ems_df['adm_code'].astype(int)
    ems_df["total"] = fix_comma(ems_df["total"].values)
    ems_df["total"] = ems_df["total"].astype(int)

    return ems_df

def merge_geo_emission(ems_file):

    ems_df = pd.read_csv(ems_file)
    ems_df = correct_ems_df(ems_df)

    geo_df = correct_shp_df()
    return geo_df.merge(ems_df, left_on='adm_code', right_on='adm_code')

def merge_all_geo_emission():
    list_df = []
    for ems_file in EMISSION_FILES:
        print(ems_file.split("\\")[-1].split(".")[0])
        year = int(ems_file.split("\\")[-1].split(".")[0])
        ems_df = pd.read_csv(ems_file)
        ems_df = correct_ems_df(ems_df)
        geo_df = correct_shp_df()
        df = geo_df.merge(ems_df, left_on='adm_code', right_on='adm_code')
        df["year"] = [year]*len(df)
        list_df.append(df)
        
    merged_df = gpd.GeoDataFrame(pd.concat(list_df, ignore_index=True))
    merged_df.to_file(EMISSION_GEOJSON, driver='GeoJSON')
    return merged_df

def trans_cols(df):
    df = df.rename(columns={
        '都道府県コード': 'pref_code', 
        '都道府県': 'pref_name',
        '市区町村コード': "adm_code",
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
        "排出量合計": "total",})
    
    return df

if __name__ == '__main__':
    df = merge_geo_emission()


# %%
