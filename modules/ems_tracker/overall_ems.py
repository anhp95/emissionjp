#%%
from core.ems_tracker.api_emission import emission_by_year
from flask_restx import Namespace, Resource
from flask import request, jsonify

api_overall_ems = Namespace("overall_ems", description="Overall Emission")


@api_overall_ems.route("/")
@api_overall_ems.param("year", "Year of the emission data")
class OverallEms(Resource):
    """
    Return Overall Emission at commune level by year
    """

    @api_overall_ems.doc(year="1990 to 2019")
    def get(self):
        year = request.args.get("year")
        return jsonify(emission_by_year(year))


# %%
