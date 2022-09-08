#%%
import pandas as pd
import os
import json

from core.const import *
from core.mypath import ZERO_EMS_DIR
from core.utils import correct_shp_df, correct_df_col_to_int

# from const import *
# from mypath import *
# from utils import correct_shp_df, correct_df_col_to_int


def read_zero_ems_csv(file_name):

    error_commune_code = 486
    df = pd.read_csv(os.path.join(ZERO_EMS_DIR, "raw", file_name))
    df = df.loc[:, ~df.columns.str.contains("^Unnamed")]
    df = df.loc[df[COMMUNE_CODE] != error_commune_code]

    commune_df = pd.read_csv(os.path.join(ZERO_EMS_DIR, "city.csv"))
    df[ADM_CODE] = commune_df[CITY_CODE].values

    df = correct_df_col_to_int(df, [ADM_CODE])

    return df


def get_all_data():

    overall_df = read_zero_ems_csv("overall.csv")

    fig1_df = read_zero_ems_csv("fig1.csv")
    fig2_df = read_zero_ems_csv("fig2.csv")
    fig3_df = read_zero_ems_csv("fig3.csv")
    fig4_df = read_zero_ems_csv("fig4.csv")
    fig5_df = read_zero_ems_csv("fig5.csv")

    return overall_df, fig1_df, fig2_df, fig3_df, fig4_df, fig5_df


def result_reform(df, cols):

    years = ["2013", "2030", "2040", "2050"]
    result = [["Types"] + years]

    for col in cols:
        rec_col = [col]
        for year in years:
            rec_col.append(df[f"{col}_{year}"].values[0])
        result.append(rec_col)
    return result


def filter_by_adm(adm_code, overall_df, fig1_df, fig2_df, fig3_df, fig4_df, fig5_df):

    fig5_df = fig5_df.fillna(0)

    commune_overall_df = overall_df[overall_df[ADM_CODE] == adm_code]
    commune_fig1_df = fig1_df[fig1_df[ADM_CODE] == adm_code]
    commune_fig2_df = fig2_df[fig2_df[ADM_CODE] == adm_code]
    commune_fig3_df = fig3_df[fig3_df[ADM_CODE] == adm_code]
    commune_fig4_df = fig4_df[fig4_df[ADM_CODE] == adm_code]
    commune_fig5_df = fig5_df[fig5_df[ADM_CODE] == adm_code]

    result = {
        "overall": commune_overall_df.to_dict("records")[0],
        "energy_consumption": result_reform(commune_fig1_df, T1_COLS),
        "emission_energy": result_reform(commune_fig2_df, T2_COLS),
        "emission_sector": result_reform(commune_fig3_df, T3_COLS),
        "re_gen": result_reform(commune_fig4_df, T4_COLS),
        "re_gen_used": result_reform(commune_fig5_df, T5_COLS),
    }
    encodedUnicode = json.dumps(result, ensure_ascii=False)
    return json.loads(encodedUnicode)


def gen_geo_zero_ems():
    overall_df, fig1_df, fig2_df, fig3_df, fig4_df, fig5_df = get_all_data()

    geo_df = correct_shp_df()

    geo_overall_df = geo_df.merge(
        overall_df,
        left_on=ADM_CODE,
        right_on=ADM_CODE,
    ).to_file(OVERALL_GEOJSON, driver="GeoJSON")
    geo_fig1_df = geo_df.merge(fig1_df, left_on=ADM_CODE, right_on=ADM_CODE).to_file(
        FIG1_GEOJSON, driver="GeoJSON"
    )
    geo_fig2_df = geo_df.merge(fig2_df, left_on=ADM_CODE, right_on=ADM_CODE).to_file(
        FIG2_GEOJSON, driver="GeoJSON"
    )
    geo_fig3_df = geo_df.merge(fig3_df, left_on=ADM_CODE, right_on=ADM_CODE).to_file(
        FIG3_GEOJSON, driver="GeoJSON"
    )
    geo_fig4_df = geo_df.merge(fig4_df, left_on=ADM_CODE, right_on=ADM_CODE).to_file(
        FIG4_GEOJSON, driver="GeoJSON"
    )
    geo_fig5_df = geo_df.merge(fig5_df, left_on=ADM_CODE, right_on=ADM_CODE).to_file(
        FIG5_GEOJSON, driver="GeoJSON"
    )

    return (
        geo_overall_df,
        geo_fig1_df,
        geo_fig2_df,
        geo_fig3_df,
        geo_fig4_df,
        geo_fig5_df,
    )


def filter_by_scenario_type(
    scenario_type, overall_df, fig1_df, fig2_df, fig3_df, fig4_df, fig5_df
):

    pass


# %%
