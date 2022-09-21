from flask import Blueprint
from flask_restx import Api
from .zero_ems import api_zero_ems


bp_zero_ems = Blueprint("zero_ems", __name__)

api = Api(
    bp_zero_ems,
    version="1.0",
    title="Zero Emission Scenarios for Japan",
    description="APIs for zero emission scenarios in Japan",
)

api.add_namespace(api_zero_ems)
