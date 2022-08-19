#%%
import flask

from flask import request, jsonify
from api_emission import emission_by_year
from flask_cors import CORS

app = flask.Flask(__name__)
CORS(app)


@app.route('/', methods=['GET'])
def get_emission():
    
    year = int(request.args['year'])
    return jsonify(emission_by_year(year))
