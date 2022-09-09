#%%
import pandas as pd
import os
import json

from core.const import *
from core.mypath import *
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
    result_gg_chart_bar = [["Types"] + years]

    for col in cols:
        rec_col = [col]
        for year in years:
            rec_col.append(df[f"{col}_{year}"].values[0])
        result_gg_chart_bar.append(rec_col)

    result_rechart_line = []
    for col in cols:
        year_rec = {"id": col, "color": "hsl(72, 70%, 50%)"}
        year_rec["data"] = []
        for year in years:
            year_rec["data"].append({"x": year, "y": df[f"{col}_{year}"].values[0]})
        result_rechart_line.append(year_rec)
    return result_gg_chart_bar, result_rechart_line


def filter_by_adm(adm_code, overall_df, fig1_df, fig2_df, fig3_df, fig4_df, fig5_df):

    fig5_df = fig5_df.fillna(0)

    overall = overall_df[overall_df[ADM_CODE] == adm_code]
    f1_bar, f1_line = result_reform(fig1_df[fig1_df[ADM_CODE] == adm_code], T1_COLS)
    f2_bar, f2_line = result_reform(fig2_df[fig2_df[ADM_CODE] == adm_code], T2_COLS)
    f3_bar, f3_line = result_reform(fig3_df[fig3_df[ADM_CODE] == adm_code], T3_COLS)
    f4_bar, f4_line = result_reform(fig4_df[fig4_df[ADM_CODE] == adm_code], T4_COLS)
    f5_bar, f5_line = result_reform(fig5_df[fig5_df[ADM_CODE] == adm_code], T5_COLS)

    result = {
        "overall": overall.to_dict("records")[0],
        "result_bar": {
            "energy_consumption": f1_bar,
            "emission_energy": f2_bar,
            "emission_sector": f3_bar,
            "re_gen": f4_bar,
            "re_gen_used": f5_bar,
        },
        "result_line": {
            "energy_consumption": f1_line,
            "emission_energy": f2_line,
            "emission_sector": f3_line,
            "re_gen": f4_line,
            "re_gen_used": f5_line,
        },
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
