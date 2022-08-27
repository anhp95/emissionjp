#%%
import win32com.client
import pandas as pd

from const import *


def overall_reduction_rate(ws, commune_name):

    commune_rate_2030_index = "E8"
    commune_rate_2040_index = "E9"
    commune_rate_2050_index = "E10"

    jp_rate_2030_index = "I8"
    jp_rate_2040_index = "I9"
    jp_rate_2050_index = "I10"

    return {
        "commune_name": commune_name,
        "commune_reduction_rate_2030": ws.Range(commune_rate_2030_index).Value,
        "commune_reduction_rate_2040": ws.Range(commune_rate_2040_index).Value,
        "commune_reduction_rate_2050": ws.Range(commune_rate_2050_index).Value,
        "jp_reduction_rate_2030": ws.Range(jp_rate_2030_index).Value,
        "jp_reduction_rate_2040": ws.Range(jp_rate_2040_index).Value,
        "jp_reduction_rate_2050": ws.Range(jp_rate_2050_index).Value,
    }


def fetch_data(rows, col_indexes, col_names, ws):

    years = [2013, 2030, 2040, 2050]

    c_dict = {
        f"{name}_{y}": f"{col}{r}"
        for y, r in zip(years, rows)
        for name, col in zip(col_names, col_indexes)
    }
    data = {key: ws.Range(c_dict[key]).Value for key in c_dict}
    data["commune_name"] = ws.Range(COMMUNE_NAME_INDEX).Value
    data["commune_code"] = ws.Range(COMMUNE_CODE_INDEX).Value
    return data


def fig1_trends_energy_consumption(ws):

    rows = [78, 79, 80, 81]  # 13, 30, 40, 50
    col_indexes = ["E", "F", "G", "H", "I", "J", "K", "L", "M", "N"]
    col_names = [
        "coal",
        "gasoline",
        "gas",
        "re_heat",
        "waste",
        "hydrogen_methane",
        "grid_power",
        "self_pv_consumption_non_post_FIT",
        "private_power_generation",
        "total",
    ]

    return fetch_data(rows, col_indexes, col_names, ws)


def fig2_trends_co2_reduction(ws):
    rows = [93, 94, 95, 96]  # 13, 30, 40, 50
    col_indexes = ["E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O"]
    col_names = [
        "coal",
        "gasoline",
        "gas",
        "re_heat",
        "waste",
        "hydrogen_methane",
        "grid_power",
        "self_pv_consumption_non_post_FIT",
        "private_power_generation",
        "total",
        "total_non_graduated_FIT_inc",
    ]

    return fetch_data(rows, col_indexes, col_names, ws)


def fig3_changes_emission_by_sector_energy_type(ws):

    rows = [100, 101, 102, 103]  # 13, 30, 40, 50
    col_indexes = [
        "E",
        "F",
        "G",
        "H",
        "I",
        "J",
        "K",
        "L",
        "M",
        "N",
        "O",
        "P",
        "Q",
        "R",
        "S",
        "T",
    ]
    col_names = {
        "agriculture_forestry_fisheries",
        "construction_mining",
        "paper",
        "chemistry",
        "cement",
        "iron_making",
        "machine",
        "other_manufacturing",
        "business",
        "housing",
        "consumption_power_plant_&_refineries_&power_transmission_&_distribution_losses",
        "automobile",
        "railroad",
        "vessel",
        "aviation",
        "total_emission",
    }

    return fetch_data(rows, col_indexes, col_names, ws)


def fig4_amount_RE_generated(ws):
    rows = [108, 109, 110, 111]  # 13, 30, 40, 50
    col_indexes = [
        "E",
        "F",
        "G",
        "H",
        "I",
        "J",
        "K",
        "L",
        "M",
    ]
    col_names = {
        "residential_solar",
        "10-50kW_solar",
        "50kW_or_more_solar_power",
        "onshore_wind_power",
        "offshore_wind_power",
        "small_medium_hydro",
        "geothermal",
        "biomass",
        "total",
    }

    return fetch_data(rows, col_indexes, col_names, ws)


def fig5_RE_power_local_consumption(ws):
    rows = [117, 118, 119, 120]  # 13, 30, 40, 50
    col_indexes = [
        "E",
        "F",
        "G",
        "H",
        "I",
        "J",
        "K",
        "M",
    ]
    col_names = {
        "self_consumption_solar",
        "non_FIT_solar_consumption",
        "post_FIT_power_consumption",
        "biomass_heat_consumption_(commercial)",
        "solar_heat_consumption_(household)",
        "electricity_distribution_business/microgrid",
        "total_renewable_energy_&_heat_local_production_&_local_consumption",
        "local_production_local_consumption/total_energy_consumption",
    }

    return fetch_data(rows, col_indexes, col_names, ws)


def main():

    xl = win32com.client.gencache.EnsureDispatch("Excel.Application")
    xl.Visible = True
    wb = xl.Workbooks.Open(XLSX_FILE)

    wb.Worksheets(SHEET_NAME).Activate()
    ws = wb.ActiveSheet

    l_overall = []
    l_fig1 = []
    l_fig2 = []
    l_fig3 = []
    l_fig4 = []
    l_fig5 = []

    for commune_code in XLS_COMMUNE_CODE:

        ws.EnableCalculation = False
        ws.Range("E3").Value = commune_code
        ws.EnableCalculation = True
        ws.Calculate()

        commune_name = ws.Range("F3").Value
        print(commune_name)
        l_overall.append(overall_reduction_rate(ws, commune_name))
        l_fig1.append(fig1_trends_energy_consumption(ws))
        l_fig2.append(fig2_trends_co2_reduction(ws))
        l_fig3.append(fig3_changes_emission_by_sector_energy_type(ws))
        l_fig4.append(fig4_amount_RE_generated(ws))
        l_fig5.append(fig5_RE_power_local_consumption(ws))

    return l_overall, l_fig1, l_fig2, l_fig3, l_fig4, l_fig5


if __name__ == "__main__":

    l_overall, l_fig1, l_fig2, l_fig3, l_fig4, l_fig5 = main()

    df_overall = pd.DataFrame.from_dict(l_overall)

    df_fig1 = pd.DataFrame.from_dict(l_fig1)
    df_fig2 = pd.DataFrame.from_dict(l_fig2)
    df_fig3 = pd.DataFrame.from_dict(l_fig3)
    df_fig4 = pd.DataFrame.from_dict(l_fig4)
    df_fig5 = pd.DataFrame.from_dict(l_fig5)

    df_overall.to_csv("../../data/zeroemission/overall.csv")
    df_fig1.to_csv("../../data/zeroemission/fig1.csv")
    df_fig2.to_csv("../../data/zeroemission/fig2.csv")
    df_fig3.to_csv("../../data/zeroemission/fig3.csv")
    df_fig4.to_csv("../../data/zeroemission/fig4.csv")
    df_fig5.to_csv("../../data/zeroemission/fig5.csv")

# %%
