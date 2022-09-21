#%%
from flask_restx import Namespace, Resource
from flask import request, jsonify

from core.api_ems_tracker import emission_adm_filter
from core.utils import merge_emssion_by_sector

api_overall_ems = Namespace("overall_ems", description="Overall Emission")


@api_overall_ems.route("/municipality")
@api_overall_ems.param("year", "Year of the emission data")
@api_overall_ems.param(
    "adm_code",
    "Municipality code of the municipality (see http://localhost:5000/ems_tracker/adm_code/jp_adm2)",
)
class OverallEmsAtMunicipality(Resource):
    """
    Return overall emission at commune level by year and adm_code
    """

    @api_overall_ems.doc(year="1990 to 2019")
    @api_overall_ems.doc(adm_code="1202 is the postal code of 札幌市")
    def get(self):
        year = request.args.get("year")
        adm_code = request.args.get("adm_code")
        return jsonify(emission_adm_filter(year=year, adm_code=adm_code))


@api_overall_ems.route("/country")
@api_overall_ems.param("year", "Year of the emission data")
class OverallEmsAtJapan(Resource):
    """
    Return overall emission of all municipality by year
    """

    @api_overall_ems.doc(year="1990 to 2019")
    def get(self):
        year = request.args.get("year")
        return jsonify(emission_adm_filter(year=year))


@api_overall_ems.route("/sector")
@api_overall_ems.param("sector_type", "1: detail sectors or 2: aggreated sectors")
class OverallEmsBySector(Resource):
    """
    Return overall emission of main sectors from 1990 to 2019 at country level
    """

    def get(self):

        sector_type = request.args.get("sector_type")
        detail_result, agg_result = merge_emssion_by_sector()
        if int(sector_type) == 1:
            return {"result": detail_result}
        return {"result": agg_result}