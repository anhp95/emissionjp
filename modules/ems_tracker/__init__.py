#%%
from flask import Blueprint
from flask_restx import Api

from .overall_ems import api_overall_ems
from .geocode import api_adm_code
from .electricity import api_electricity

bp_ems_tracker = Blueprint("ems_tracker", __name__)
api = Api(
    bp_ems_tracker,
    version="1.0",
    title="Emission Tracker for Japan",
    description="APIs for GHG emission tracking in Japan",
)

api.add_namespace(api_overall_ems)
api.add_namespace(api_adm_code)
api.add_namespace(api_electricity)

# %%
