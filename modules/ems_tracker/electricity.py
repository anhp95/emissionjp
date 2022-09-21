#%%
from flask_restx import Namespace, Resource
from flask import request, jsonify

from core.api_ems_tracker import get_e_5mins

api_electricity = Namespace(
    "electricity", description="Electricity Generation and Consumption"
)


@api_electricity.route("/5mins")
class OverallEmsAtMunicipality(Resource):
    """
    Return electricity generation and consumption per each 5 minutes
    """

    @api_electricity.doc(
        year="Electricity Generation and Consumption per each 5 minutes"
    )
    def get(self):
        return get_e_5mins()


# %%
