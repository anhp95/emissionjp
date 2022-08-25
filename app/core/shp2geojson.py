#%%
import geopandas
from app.core.mypath import AMD2_SHP, AMD2_GEOJSON

myshpfile = geopandas.read_file(AMD2_SHP)
myshpfile.to_file(AMD2_GEOJSON, driver='GeoJSON')


