#%%
import flask

from modules.ems_tracker import bp
from flask_cors import CORS

app = flask.Flask(__name__)
CORS(app)

app.register_blueprint(bp, url_prefix="/ems_tracker")
app.run(debug=True, port=5001)

# %%