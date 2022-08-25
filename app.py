#%%
import flask
import os

from modules.ems_tracker import bp
from flask_cors import CORS

app = flask.Flask(__name__)
CORS(app)

app.register_blueprint(bp, url_prefix="/ems_tracker")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)

# %%