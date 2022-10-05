#%%
import geopandas as gpd
import glob
import os


def extract_lng_lat(df):
    list_geometry = df.geometry
    list_lng_lat = []
    list_x = []
    list_y = []
    for g in list_geometry:
        list_x.append(g.x)
        list_y.append(g.y)
        list_lng_lat.append([g.x, g.y])

    df["lng_lat"] = list_lng_lat
    df["x"] = list_x
    df["y"] = list_y


def extract_out_name(shp_path):
    out_name = shp_path.split("\\")[-1].split(".")[0]
    return f"{out_name}.json"


def map_output_viz(a):
    if a <= 1:
        a = 1
    elif a > 1 and a <= 10:
        a = 2
    elif a > 10 and a <= 40:
        a = 3
    elif a > 40 and a <= 100:
        a = 4
    elif a > 100 and a <= 200:
        a = 5
    elif a > 200 and a <= 400:
        a = 6
    elif a > 400 and a <= 1000:
        a = 7
    elif a > 1000 and a <= 2000:
        a = 8
    elif a > 2000 and a <= 4000:
        a = 9
    elif a > 4000:
        a = 10

    return a


def handle_shp(shp_path):
    df = gpd.read_file(shp_path, encoding="shift_jis")
    df.rename(
        columns={
            "P03_0001": "name",
            "P03_0002": "facility",
            "P03_0003": "location",
            "P03_0008": "output",
        },
        inplace=True,
    )
    extract_lng_lat(df)

    df["output"] = df["output"] / 1e3
    df["output_viz"] = [map_output_viz(val) for val in df["output"].values]
    # Electric
    df_json = df[
        ["name", "facility", "location", "type", "output", "output_viz", "lng_lat"]
    ]

    out_file = extract_out_name(shp_path)

    with open(out_file, "wb") as fp:
        fp.write(df_json.to_json(orient="records", force_ascii=False).encode("utf8"))


if __name__ == "__main__":

    PP_DIR = r"D:\Emission Data\Power_Plant\P03-13\P03-13\SHP\all"
    list_shp = glob.glob(os.path.join(PP_DIR, "*.shp"))

    for shp in list_shp:
        handle_shp(shp)
        # df_shp = gpd.read_file(shp, encoding="shift_jis")
        # shp_file = (
        #     r"D:\Emission Data\Power_Plant\P03-13\P03-13\SHP\all\all_powerplant.shp"
        # )

    # df_csv.to_csv(geocoded_csv)
# %%

# %%
