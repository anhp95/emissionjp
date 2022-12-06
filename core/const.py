#%%
from datetime import date

SHEET_NAME = "①　シナリオ入力、算定結果、グラフ等"

XLS_COMMUNE_CODE = [i for i in range(15, 1757)]
COMMUNE_NAME_INDEX = "F3"
COMMUNE_CODE_INDEX = "E3"

ADM_CODE = "adm_code"
CITY_CODE = "city_code"
COMMUNE_CODE = "commune_code"

OVERALL_COLS = ["commune_red_rate", "jp_red_rate"]

# T1_COLS = [
#     "coal",
#     "gasoline",
#     "gas",
#     "re_heat",
#     "waste",
#     "hydrogen_methane",
#     "grid_power",
#     "self_pv_consumption_non_post_FIT",
#     "private_power_generation",
#     "total",
# ]
# T2_COLS = [
#     "coal",
#     "gasoline",
#     "gas",
#     "re_heat",
#     "waste",
#     "hydrogen_methane",
#     "grid_power",
#     "self_pv_consumption_non_post_FIT",
#     "private_power_generation",
#     "total",
#     "total_non_graduated_FIT_inc",
# ]
# T3_COLS = [
#     "agriculture_forestry_fisheries",
#     "construction_mining",
#     "paper",
#     "chemistry",
#     "cement",
#     "iron_making",
#     "machine",
#     "other_manufacturing",
#     "business",
#     "housing",
#     "consumption_power_plant_&_refineries_&power_transmission_&_distribution_losses",
#     "automobile",
#     "railroad",
#     "vessel",
#     "aviation",
#     "total_emission",
# ]
# T4_COLS = [
#     "residential_solar",
#     "10-50kW_solar",
#     "50kW_or_more_solar_power",
#     "onshore_wind_power",
#     "offshore_wind_power",
#     "small_medium_hydro",
#     "geothermal",
#     "biomass",
#     "total",
# ]
# T5_COLS = [
#     "self_consumption_solar",
#     "non_FIT_solar_consumption",
#     "post_FIT_power_consumption",
#     "biomass_heat_consumption_(commercial)",
#     "solar_heat_consumption_(household)",
#     "electricity_distribution_business/microgrid",
#     "total_renewable_energy_&_heat_local_production_&_local_consumption",
#     "local_production_local_consumption/total_energy_consumption",
# ]

T1_COLS = [
    "石炭",
    "石油",
    "天然ガス/都市ガス",
    "再エネ熱",
    "未活用 廃棄物等",
    "水素・メタン等",
    "系統電力",
    "PV自家消費・非FIT・卒FIT",
    "自家発電・熱、熱供給",
    "合計",
]
T2_COLS = [
    "石炭",
    "石油",
    "天然ガス/都市ガス",
    "再エネ熱",
    "未活用 廃棄物等",
    "水素・メタン等",
    "系統電力",
    "PV自家消費・非FIT・卒FIT",
    "自家発電・熱、熱供給",
    "合計",
    "非・卒FITによる削減含む",
]
T3_COLS = [
    "農林水産業",
    "建設・鉱業",
    "紙パ",
    "化学",
    "セメント",
    "製鉄",
    "機械",
    "その他製造業",
    "業務",
    "家庭",
    "発電所・製油所所内消費、送配電ロス",
    "自動車",
    "鉄道",
    "船舶",
    "航空",
    "排出量計",
]
T4_COLS = [
    "住宅用太陽光",
    "10-50kW太陽光",
    "50kW以上太陽光",
    "陸上風力",
    "洋上風力",
    "中小水力",
    "地熱",
    "バイオマス",
    "計",
]
T5_COLS = [
    "太陽光自家消費",
    "非FIT太陽光消費",
    "卒FIT電力消費",
    "バイオマス熱消費(業務)",
    "太陽熱消費(家庭)",
    "配電事業/マイクログリッド",
    "再エネ電力・熱地産地消計",
    "地産地消計/総エネルギー消費",
]


def get_today_str():
    return str(date.today()).replace("-", "")


TODAY = get_today_str()
HOKKAIDO_URL = f"https://denkiyoho.hepco.co.jp/area/data/juyo_01_{TODAY}.csv"  # https://denkiyoho.hepco.co.jp/
TOHOKU_URL = f"https://setsuden.nw.tohoku-epco.co.jp/common/demand/juyo_02_{TODAY}.csv"
TOKYO_URL = "https://www.tepco.co.jp/forecast/html/images/juyo-d1-j.csv"
CHUBU_URL = "https://powergrid.chuden.co.jp/denki_yoho_content_data/juyo_cepco003.csv"  # https://powergrid.chuden.co.jp/denkiyoho/
HOKURIKU = f"https://www.rikuden.co.jp/nw/denki-yoho/csv/juyo_05_{TODAY}.csv"
KANSAI_URL = "https://www.kansai-td.co.jp/yamasou/juyo1_kansai.csv"
CHUGOKU_URL = f"https://www.energia.co.jp/nw/jukyuu/sys/juyo_07_{TODAY}.csv"
SHIKOKU_URL = "https://www.yonden.co.jp/nw/denkiyoho/juyo_shikoku.csv"
KYUSHU_URL = f"https://www.kyuden.co.jp/td_power_usages/csv/juyo-hourly-{TODAY}.csv"
OKINAWA_URL = f"https://www.okiden.co.jp/denki2/juyo_10_{TODAY}.csv"

DICT_E_URL = {
    f"Hokkaido_{TODAY}": HOKKAIDO_URL,
    f"Tohoku_{TODAY}": TOHOKU_URL,
    f"Tokyo_{TODAY}": TOKYO_URL,
    f"Chubu_{TODAY}": CHUBU_URL,
    f"Hokuriku_{TODAY}": HOKURIKU,
    f"Kansai_{TODAY}": KANSAI_URL,
    f"Chugoku_{TODAY}": CHUGOKU_URL,
    f"Shikoku_{TODAY}": SHIKOKU_URL,
    f"Kyushu_{TODAY}": KYUSHU_URL,
    f"Okinawa_{TODAY}": OKINAWA_URL,
}
# %%
