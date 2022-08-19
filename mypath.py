import os
import glob

AMD2_SHP = "./data/shp/jp_adm2_dissolved.shp"
AMD2_GEOJSON = "./data/geojson/amd2_jp.json"

EMISSION_DIR = "./data/emission/raw/csv"
EMISSION_FILES = glob.glob(os.path.join(EMISSION_DIR, "*.csv"))

EMISSION_GEOJSON = "./data/emission/merged/1990_2019_merged.json"
