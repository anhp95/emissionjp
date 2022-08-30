#%%
import pandas as pd
import os
import json

BASE_DIR = "data/zeroemission"


def read_csv(file_name):

    df = pd.read_csv(os.path.join(BASE_DIR, file_name))
    df = df.loc[:, ~df.columns.str.contains("^Unnamed")]

    return df


def get_all_data():

    overall_df = read_csv("overall.csv")
    fig1_df = read_csv("fig1.csv")
    fig2_df = read_csv("fig2.csv")
    fig3_df = read_csv("fig3.csv")
    fig4_df = read_csv("fig4.csv")
    fig5_df = read_csv("fig5.csv")

    return overall_df, fig1_df, fig2_df, fig3_df, fig4_df, fig5_df


def get_data_by_commune_code(
    commune_code, overall_df, fig1_df, fig2_df, fig3_df, fig4_df, fig5_df
):
    fig5_df = fig5_df.fillna(0)
    result = {
        "overall": overall_df[overall_df["commune_code"] == commune_code].to_dict(
            "records"
        )[0],
        "fig1": fig1_df[fig1_df["commune_code"] == commune_code].to_dict("records")[0],
        "fig2": fig2_df[fig2_df["commune_code"] == commune_code].to_dict("records")[0],
        "fig3": fig3_df[fig3_df["commune_code"] == commune_code].to_dict("records")[0],
        "fig4": fig4_df[fig4_df["commune_code"] == commune_code].to_dict("records")[0],
        "fig5": fig5_df[fig5_df["commune_code"] == commune_code].to_dict("records")[0],
    }
    encodedUnicode = json.dumps(result, ensure_ascii=False)
    return json.loads(encodedUnicode)


# %%
