#%%
from flask import Blueprint
from flask_restx import Api

from .apis.overall_ems import api as ns1

bp = Blueprint("api", __name__)
api = Api(bp)

api.add_namespace(ns1)

# %%
