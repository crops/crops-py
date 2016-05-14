from flask import Flask
from flask import jsonify
from flask import request
from utils.globs import config

app = Flask(__name__)

@app.route('/turff/', methods = ['GET'])
def api_list():
    '''Show TURFF API
    args: None
    returns: List of all registered routes in JSON format
    '''
    return config.get_all_routes(app)

@app.route('/turff/version', methods=['GET'])
def get_version():
    '''Show TURFF version
    args: None
    returns: TURFF version in JSON format
    '''
    return jsonify(version=config.VERSION)

if __name__ == '__main__':
    app.run(host=config.TURFF_IP, port=config.TURFF_PORT, debug=True)
