#%%
from flask_restx import Namespace, Resource
from flask import request, jsonify

from core.api_zero_ems import get_all_data, filter_by_adm


api_zero_ems = Namespace("zero_ems", description="Zero Emission scenario")

OVERALL_DF, FIG1_DF, FIG2_DF, FIG3_DF, FIG4_DF, FIG5_DF = get_all_data()


@api_zero_ems.route("/municipality")
@api_zero_ems.param("commune_code", "A commune of Japan")
class ZeroEmsAtMunacipality(Resource):
    """
    Return Overall Scenario at commune level
    """

    @api_zero_ems.doc(commune_code="Commune code according to Excel tool")
    def get(self):

        commune_code = int(request.args.get("commune_code"))
        zero_ems_data = filter_by_adm(
            commune_code, OVERALL_DF, FIG1_DF, FIG2_DF, FIG3_DF, FIG4_DF, FIG5_DF
        )

        return zero_ems_data


# @api_zero_ems.route("/country")
# @api_zero_ems.param("scenario_type", "Type of the scenario")
# class ZeroEmsAtJapan(Resource):
#     """
#     Return Overall Scenario at country level
#     """

#     @api_zero_ems.doc(
#         scenario_type="One of energy_comsumption, emission_energy, emission_sector or re_gen, re_gen_used"
#     )
#     def get(self):
#         scenario_type = request.args.get("scenario_type")
