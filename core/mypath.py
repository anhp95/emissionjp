import os
import glob

# DATA_DIR = "../data"
DATA_DIR = "data"

AMD2_SHP = os.path.join(DATA_DIR, "shp/jp_adm2_dissolved.shp")
AMD2_GEOJSON = os.path.join(DATA_DIR, "geojson/amd2_jp.json")

EMS_TRACKER_DIR = os.path.join(DATA_DIR, "ems_tracker/raw/csv")
EMS_TRACKER_FILES = glob.glob(os.path.join(EMS_TRACKER_DIR, "*.csv"))
EMS_TRACKER_GEOJSON = os.path.join(DATA_DIR, "ems_tracker/merged/1990_2019_merged.json")

XLSX_FILE = r"D:\Emission Data\Takeuchi-sensei data\2022_8_3)タイプⅡ(トレンド延長型)　ver 2 地域シナリオ分析ツール.xlsx"
ZERO_EMS_DIR = os.path.join(DATA_DIR, "zero_ems")

ZERO_EMS_GEOJSON = os.path.join(DATA_DIR, "geojson")

OVERALL_GEOJSON = os.path.join(ZERO_EMS_GEOJSON, "zero_ems_overall.json")
FIG1_GEOJSON = os.path.join(ZERO_EMS_GEOJSON, "zero_ems_fig1.json")
FIG2_GEOJSON = os.path.join(ZERO_EMS_GEOJSON, "zero_ems_fig2.json")
FIG3_GEOJSON = os.path.join(ZERO_EMS_GEOJSON, "zero_ems_fig3.json")
FIG4_GEOJSON = os.path.join(ZERO_EMS_GEOJSON, "zero_ems_fig4.json")
FIG5_GEOJSON = os.path.join(ZERO_EMS_GEOJSON, "zero_ems_fig5.json")
