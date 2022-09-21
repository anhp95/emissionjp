#%%
SHEET_NAME = "①　シナリオ入力、算定結果、グラフ等"

XLS_COMMUNE_CODE = [i for i in range(15, 1757)]
COMMUNE_NAME_INDEX = "F3"
COMMUNE_CODE_INDEX = "E3"

ADM_CODE = "adm_code"
CITY_CODE = "city_code"
COMMUNE_CODE = "commune_code"

OVERALL_COLS = ["commune_red_rate", "jp_red_rate"]

T1_COLS = [
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
T2_COLS = [
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
T3_COLS = [
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
]
T4_COLS = [
    "residential_solar",
    "10-50kW_solar",
    "50kW_or_more_solar_power",
    "onshore_wind_power",
    "offshore_wind_power",
    "small_medium_hydro",
    "geothermal",
    "biomass",
    "total",
]
T5_COLS = [
    "self_consumption_solar",
    "non_FIT_solar_consumption",
    "post_FIT_power_consumption",
    "biomass_heat_consumption_(commercial)",
    "solar_heat_consumption_(household)",
    "electricity_distribution_business/microgrid",
    "total_renewable_energy_&_heat_local_production_&_local_consumption",
    "local_production_local_consumption/total_energy_consumption",
]

hokkaido_url = "https://denkiyoho.hepco.co.jp/area/data/juyo_01_20220915.csv"  # https://denkiyoho.hepco.co.jp/
tohoku_url = "https://setsuden.nw.tohoku-epco.co.jp/common/demand/juyo_02_20200913.csv"
tokyo_url = "https://www.tepco.co.jp/forecast/html/images/juyo-d1-j.csv"
chubu_url = "https://powergrid.chuden.co.jp/denki_yoho_content_data/juyo_cepco003.csv"  # https://powergrid.chuden.co.jp/denkiyoho/
hokuriku_url = "https://www.rikuden.co.jp/nw/denki-yoho/csv/juyo_05_20220915.csv"
kansai_url = "https://www.kansai-td.co.jp/yamasou/juyo1_kansai.csv"
chugoku_url = "https://www.energia.co.jp/nw/jukyuu/csv.html"
shikoku_url = "https://www.yonden.co.jp/nw/denkiyoho/juyo_shikoku.csv"
kyushu_url = "https://www.kyuden.co.jp/td_power_usages/csv/juyo-hourly-20220915.csv"
okinawa_url = "https://www.okiden.co.jp/denki2/juyo_10_20220915.csv"
