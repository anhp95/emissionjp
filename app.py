#%%
from nturl2path import url2pathname
import flask
import os

from modules.ems_tracker import bp_ems_tracker
from modules.zero_ems import bp_zero_ems

from flask_cors import CORS

app = flask.Flask(__name__)

CORS(app)

app.register_blueprint(bp_ems_tracker, url_prefix="/ems_tracker")
app.register_blueprint(bp_zero_ems, url_prefix="/zero_ems")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
