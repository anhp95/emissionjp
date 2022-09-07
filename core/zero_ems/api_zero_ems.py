#%%
import pandas as pd
import os
import json

from core.zero_ems.const import *

# from const import *

BASE_DIR = "data/zeroemission"
# BASE_DIR = "../../data/zeroemission"

ADM_CODE = "adm_code"
CITY_CODE = "city_code"
COMMUNE_CODE = "commune_code"


def read_csv(file_name):

    df = pd.read_csv(os.path.join(BASE_DIR, file_name))
    df = df.loc[:, ~df.columns.str.contains("^Unnamed")]

    return df


def get_all_data():

    commune_df = read_csv("city.csv")

    overall_df = read_csv("overall.csv")
    overall_df[ADM_CODE] = commune_df[CITY_CODE]

    fig1_df = read_csv("fig1.csv")
    fig1_df[ADM_CODE] = commune_df[CITY_CODE]

    fig2_df = read_csv("fig2.csv")
    fig2_df[ADM_CODE] = commune_df[CITY_CODE]

    fig3_df = read_csv("fig3.csv")
    fig3_df[ADM_CODE] = commune_df[CITY_CODE]

    fig4_df = read_csv("fig4.csv")
    fig4_df[ADM_CODE] = commune_df[CITY_CODE]

    fig5_df = read_csv("fig5.csv")
    fig5_df[ADM_CODE] = commune_df[CITY_CODE]

    return overall_df, fig1_df, fig2_df, fig3_df, fig4_df, fig5_df


def result_reform(df, cols):

    # emission_by_energy_type = [["Years"] + T2_COLS]
    # emission_by_sector = [["Years"] + T3_COLS]
    # RE_generated = [["Years"] + T4_COLS]
    # RE_gp = [["Years"] + T5_COLS]

    result = [["Years"] + cols]
    years = [2013, 2030, 2050]

    for year in years:
        rec_year = [year]
        for col in cols:
            rec_year.append(df[f"{col}_{year}"].values[0])
        result.append(rec_year)
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
        "emission_by_energy_type": result_reform(commune_fig2_df, T2_COLS),
        "emission_by_sector": result_reform(commune_fig3_df, T3_COLS),
        "RE_generated": result_reform(commune_fig4_df, T4_COLS),
        "RE_generated/production": result_reform(commune_fig5_df, T5_COLS),
    }
    encodedUnicode = json.dumps(result, ensure_ascii=False)
    return json.loads(encodedUnicode)


# %%
