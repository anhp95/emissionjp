#%%
from flask_restx import Namespace, Resource
from flask import request, jsonify

from core.zero_ems.api_zero_ems import get_all_data, get_data_by_commune_code


api_zero_ems = Namespace("zero_ems", description="Zero Emission scenario")

OVERALL_DF, FIG1_DF, FIG2_DF, FIG3_DF, FIG4_DF, FIG5_DF = get_all_data()


@api_zero_ems.route("/")
@api_zero_ems.param("commune_code", "A commune of Japan")
class ZeroEms(Resource):
    """
    Return Overall Emission at commune level by year
    """

    @api_zero_ems.doc(commune_code="Commune code according to Excel tool")
    def get(self):

        commune_code = request.args.get("commune_code")
        zero_ems_data = get_data_by_commune_code(
            commune_code, OVERALL_DF, FIG1_DF, FIG2_DF, FIG3_DF, FIG4_DF, FIG5_DF
        )

        return zero_ems_data


# %%
