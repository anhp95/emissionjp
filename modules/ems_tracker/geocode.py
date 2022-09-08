import pandas as pd

from flask_restx import Namespace, Resource
from flask import jsonify

api_geocode = Namespace("geocode", "Geocoding API for Japan's municipality")
city_df = pd.read_csv("data/zero_ems/city.csv")


@api_geocode.route("/jp_adm2")
class JPAdm2(Resource):
    """Return Japan's cities"""

    def get(self):

        return jsonify(city_df.to_dict("records"))
