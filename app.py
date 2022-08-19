#%%
import flask
from flask import request

import geopandas as gpd
import pandas as pd
from api_emission import emission_by_year

app = flask.Flask(__name__)


@app.route('/', methods=['GET'])
def get_emission():
    year = int(request.args['year'])

    return emission_by_year(year)


# %%