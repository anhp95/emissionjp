import os
import glob

DATA_DIR = "data"

AMD2_SHP = os.path.join(DATA_DIR, "shp/jp_adm2_dissolved.shp")
AMD2_GEOJSON = os.path.join(DATA_DIR, "geojson/amd2_jp.json")

EMISSION_DIR = os.path.join(DATA_DIR, "emission/raw/csv")
EMISSION_FILES = glob.glob(os.path.join(EMISSION_DIR, "*.csv"))

EMISSION_GEOJSON = os.path.join(DATA_DIR, "emission/merged/1990_2019_merged.json")
