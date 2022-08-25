#%%
from core.api_emission import emission_by_year
from flask_restx import Namespace, Resource
from flask import request, jsonify

api = Namespace("overallems", description="Overall Emission")

@api.route("/overallems")
@api.param("year", "Year of the emission data")
class OverallEms(Resource):
    """
    Return Overall Emission at commune level by year
    """
    @api.doc(year="1990 to 2019")
    def get(self):
        year = request.args.get("year")
        return jsonify(emission_by_year(year))

# %%
