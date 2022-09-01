#%%
from core.ems_tracker.api_emission import emission_by_year
from flask_restx import Namespace, Resource
from flask import request, jsonify

api_overall_ems = Namespace("overall_ems", description="Overall Emission")


@api_overall_ems.route("/")
@api_overall_ems.param("year", "Year of the emission data")
@api_overall_ems.param("adm_code", "Postal code of the municipality")
class OverallEms(Resource):
    """
    Return Overall Emission at commune level by year
    """

    @api_overall_ems.doc(year="1990 to 2019")
    @api_overall_ems.doc(adm_code="1202 is the postal code of 札幌市")
    def get(self):
        year = request.args.get("year")
        adm_code = request.args.get("adm_code")
        return jsonify(emission_by_year(year, adm_code))


# %%
