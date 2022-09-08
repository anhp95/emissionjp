#%%
import geopandas
from core.mypath import AMD2_SHP

jp_df = geopandas.read_file(AMD2_SHP)
# myshpfile.to_file(AMD2_GEOJSON, driver="GeoJSON")

# %%
