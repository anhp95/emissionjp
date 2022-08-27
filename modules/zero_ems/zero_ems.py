#%%
from flask_restx import Namespace, Resource
from flask import request, jsonify

api_zero_ems = Namespace("zero_ems", description="Zero Emission scenario")

@api_zero_ems.route("/")
@api_zero_ems.param("commune", "A commune of Japan")
class ZeroEms(Resource):
    """
    Return Overall Emission at commune level by year
    """
    @api_zero_ems.doc(commune="E.g., Nagoya")
    def get(self):
        commune = request.args.get("commune")
        return {"commune": commune}

# %%
